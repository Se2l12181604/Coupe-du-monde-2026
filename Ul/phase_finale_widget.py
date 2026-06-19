from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from UI.groupe_widget import CardContainer
from phase_finale import determiner_les_32, generer_seiziemes
from exportation import exporter_tournoi_excel_csv


class PhaseFinaleWidget(BoxLayout): # Changé en BoxLayout pour intégrer les sous-onglets des tours

    def __init__(self, main_app_tabs, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=10, **kwargs)
        self.main_app_tabs = main_app_tabs
        
        # Structure pour stocker les scores et qualifiés de CHAQUE tour
        # "1/16": { match_id: {"eq1": Name, "eq2": Name, "score1": Text, "score2": Text, "qualifie": Name} }
        self.donnees_tournoi = {
            "1/16": {}, "1/8": {}, "1/4": {}, "1/2": {}, "Finale": {}
        }

        # --- BARRE D'ACTIONS GLOBALE (Export + Effacer) ---
        barre_actions = BoxLayout(orientation="horizontal", size_hint_y=None, height=45, spacing=15, padding=[15, 5, 15, 5])
        
        self.btn_export = Button(
            text="Exporter vers Excel (.csv)",
            background_color=(0.18, 0.67, 0.38, 1),
            font_size="14sp",
            bold=True
        )
        self.btn_export.bind(on_release=self.declencher_export)
        
        self.btn_effacer_all = Button(
            text="Réinitialiser Toute la Phase Finale",
            background_color=(0.9, 0.3, 0.2, 1),
            font_size="14sp",
            bold=True
        )
        self.btn_effacer_all.bind(on_release=self.effacer_toute_la_phase_finale)

        barre_actions.add_widget(self.btn_export)
        barre_actions.add_widget(self.btn_effacer_all)
        self.add_widget(barre_actions)

        # --- ZONE DE STATUS ---
        self.lbl_status = Label(text="", size_hint_y=None, height=25, font_size="12sp", color=(0.7, 0.7, 0.7, 1))
        self.add_widget(self.lbl_status)

        # --- SYSTEME D'ONGLETS POUR LES TOURS ---
        self.tabs_tours = TabbedPanel(do_default_tab=False)
        
        self.onglet_16 = TabbedPanelItem(text="1/16")
        self.onglet_8  = TabbedPanelItem(text="1/8")
        self.onglet_4  = TabbedPanelItem(text="1/4")
        self.onglet_2  = TabbedPanelItem(text="1/2")
        self.onglet_1  = TabbedPanelItem(text="Finale")

        self.tabs_tours.add_widget(self.onglet_16)
        self.tabs_tours.add_widget(self.onglet_8)
        self.tabs_tours.add_widget(self.onglet_4)
        self.tabs_tours.add_widget(self.onglet_2)
        self.tabs_tours.add_widget(self.onglet_1)
        
        self.add_widget(self.tabs_tours)

        # Liaison du changement de sous-onglet pour recalculer les tours suivants
        self.tabs_tours.bind(current_tab=self.sur_changement_tour)

    def declencher_export(self, instance):
        tous_les_classements = {lettre: w.obtenir_resultats_groupe() for lettre, w in self.main_app_tabs.onglets_groupes.items()}
        self.lbl_status.text = exporter_tournoi_excel_csv(tous_les_classements)

    def effacer_toute_la_phase_finale(self, instance):
        """Remet à zéro l'ensemble de l'arbre."""
        self.donnees_tournoi = {"1/16": {}, "1/8": {}, "1/4": {}, "1/2": {}, "Finale": {}}
        self.rafraichir_arbre()
        self.lbl_status.text = "Toute la phase finale a été vidée !"

    def sur_changement_tour(self, instance, value):
        """Dès qu'on change de sous-onglet, on recalcule le tour sélectionné basé sur le précédent."""
        self.recalculer_tournoi()

    def rafraichir_arbre(self):
        """Appelé par main.py lors du clic sur l'onglet principal 'PHASE FINALE'."""
        self.recalculer_tournoi()

    def recalculer_tournoi(self):
        """Gère la cascade complète des qualifications de tour en tour."""
        # 1. Récupération initiale depuis les groupes (1/16)
        tous_les_classements = {lettre: w.obtenir_resultats_groupe() for lettre, w in self.main_app_tabs.onglets_groupes.items()}
        try:
            les_32, _ = determiner_les_32(tous_les_classements)
            affiches_16 = generer_seiziemes(les_32)
            
            # Initialise ou conserve les structures de match pour les 1/16
            for m in affiches_16:
                m_id = m["id"]
                if m_id not in self.donnees_tournoi["1/16"]:
                    self.donnees_tournoi["1/16"][m_id] = {"eq1": m["eq1"], "eq2": m["eq2"], "score1": "", "score2": "", "qualifie": None}
        except Exception as e:
            self.generer_ecran_attente(self.onglet_16, str(e))
            return

        # 2. Génération en cascade des tours suivants (1/8, 1/4, 1/2, Finale)
        self.propager_qualifies("1/16", "1/8", nb_matchs_cible=16)
        self.propager_qualifies("1/8", "1/4", nb_matchs_cible=8)
        self.propager_qualifies("1/4", "1/2", nb_matchs_cible=4)
        self.propager_qualifies("1/2", "Finale", nb_matchs_cible=2)

        # 3. Dessiner le contenu visuel du sous-onglet actuellement ouvert
        dict_onglets = {"1/16": self.onglet_16, "1/8": self.onglet_8, "1/4": self.onglet_4, "1/2": self.onglet_2, "Finale": self.onglet_1}
        tour_actif = [tour for tour, obj in dict_onglets.items() if obj == self.tabs_tours.current_tab][0]
        
        self.construire_vue_tour(tour_actif, dict_onglets[tour_actif])

    def propager_qualifies(self, tour_precedent, tour_suivant, nb_matchs_cible):
        """Prend les vainqueurs du tour précédent et les assemble 2 par 2 pour le tour suivant."""
        matchs_prec = self.donnees_tournoi[tour_precedent]
        id_matchs_prec = sorted(list(matchs_prec.keys()))
        
        # Vérifie si le tour précédent a tous ses qualifiés
        qualifies = [matchs_prec[m_id]["qualifie"] for m_id in id_matchs_prec if matchs_prec[m_id]["qualifie"] is not None]
        
        if len(qualifies) < len(id_matchs_prec):
            self.donnees_tournoi[tour_suivant] = {} # Pas assez de qualifiés pour générer le tour suivant
            return

        # On couple le Match 1 avec Match 2, Match 3 avec Match 4, etc.
        nouveau_tour = {}
        for i in range(0, len(qualifies), 2):
            match_id_suivant = (i // 2) + 1
            eq1 = qualifies[i]
            eq2 = qualifies[i+1] if i+1 < len(qualifies) else "En attente..."
            
            # Conserve les scores déjà tapés si les équipes n'ont pas changé
            ancien_match = self.donnees_tournoi[tour_suivant].get(match_id_suivant, {})
            score1 = ancien_match.get("score1", "") if ancien_match.get("eq1") == eq1 else ""
            score2 = ancien_match.get("score2", "") if ancien_match.get("eq2") == eq2 else ""
            qualifie = ancien_match.get("qualifie") if score1 != "" and score2 != "" else None
            
            nouveau_tour[match_id_suivant] = {"eq1": eq1, "eq2": eq2, "score1": score1, "score2": score2, "qualifie": qualifie}
            
        self.donnees_tournoi[tour_suivant] = nouveau_tour

    def construire_vue_tour(self, nom_tour, objet_onglet):
        """Dessine dynamiquement les grilles de matchs pour l'onglet demandé."""
        objet_onglet.clear_widgets()
        
        matchs = self.donnees_tournoi[nom_tour]
        if not matchs:
            self.generer_ecran_attente(objet_onglet, "En attente des qualifications du tour précédent.")
            return

        scroll = ScrollView()
        grid = GridLayout(cols=2, spacing=20, size_hint_y=None, padding=20)
        grid.bind(minimum_height=grid.setter("height"))

        for m_id, data in matchs.items():
            carte = CardContainer(orientation="vertical", size_hint_y=None, height=125, padding=10, spacing=5)
            
            lbl_id = Label(text=f"[color=7F8C8D]{nom_tour} — Match {m_id}[/color]", markup=True, size_hint_y=None, height=15, font_size="11sp")
            carte.add_widget(lbl_id)

            ligne = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None, height=45)
            lbl_eq1 = Label(text=data["eq1"], halign="right", font_size="14sp", size_hint_x=0.35)
            score1 = TextInput(text=data["score1"], multiline=False, input_filter="int", size_hint_x=None, width=45, halign="center")
            lbl_vs = Label(text="vs", size_hint_x=None, width=20, color=(0.5, 0.5, 0.5, 1))
            score2 = TextInput(text=data["score2"], multiline=False, input_filter="int", size_hint_x=None, width=45, halign="center")
            lbl_eq2 = Label(text=data["eq2"], halign="left", font_size="14sp", size_hint_x=0.35)

            ligne.add_widget(lbl_eq1)
            ligne.add_widget(score1)
            ligne.add_widget(lbl_vs)
            ligne.add_widget(score2)
            ligne.add_widget(lbl_eq2)
            carte.add_widget(ligne)

            # Bouton pour gérer les prolongations/Tirs au but ou afficher le vainqueur direct
            btn_status = Button(size_hint_y=None, height=30, font_size="12sp", bold=True)
            self.mettre_a_jour_bouton_status(btn_status, data)
            carte.add_widget(btn_status)

            # Événements de saisie de score
            score1.bind(text=lambda instance, val, t=nom_tour, mid=m_id, s="score1", b=btn_status: self.on_score_change(t, mid, s, val, b))
            score2.bind(text=lambda instance, val, t=nom_tour, mid=m_id, s="score2", b=btn_status: self.on_score_change(t, mid, s, val, b))
            
            # Événement clic sur le bouton de qualification (si égalité prolongée)
            btn_status.bind(on_release=lambda instance, t=nom_tour, mid=m_id, b=btn_status: self.on_status_click(t, mid, b))

            grid.add_widget(carte)

        scroll.add_widget(grid)
        objet_onglet.add_widget(scroll)

    def on_score_change(self, tour, match_id, champ_score, valeur, bouton):
        """Enregistre le score entré et calcule le qualifié logique immédiat."""
        self.donnees_tournoi[tour][match_id][champ_score] = valeur.strip()
        match = self.donnees_tournoi[tour][match_id]
        
        v1, v2 = match["score1"], match["score2"]
        if v1 != "" and v2 != "":
            if int(v1) > int(v2):
                match["qualifie"] = match["eq1"]
            elif int(v2) > int(v1):
                match["qualifie"] = match["eq2"]
            else:
                # Égalité : le bouton servira à choisir manuellement (TAB)
                if match["qualifie"] not in [match["eq1"], match["eq2"]]:
                    match["qualifie"] = match["eq1"] # Par défaut eq1
        else:
            match["qualifie"] = None

        self.mettre_a_jour_bouton_status(bouton, match)

    def on_status_click(self, tour, match_id, bouton):
        """Bascule manuellement le qualifié en cas d'égalité (Simulation Tirs au but)."""
        match = self.donnees_tournoi[tour][match_id]
        if match["score1"] != "" and match["score2"] != "" and match["score1"] == match["score2"]:
            # On inverse le qualifié
            match["qualifie"] = match["eq2"] if match["qualifie"] == match["eq1"] else match["eq1"]
            self.mettre_a_jour_bouton_status(bouton, match)
            self.recalculer_tournoi() # Alerte les tours suivants du changement de vainqueur

    def mettre_a_jour_bouton_status(self, bouton, match):
        """Modifie le look et le texte du bouton en fonction de l'état du match."""
        v1, v2 = match["score1"], match["score2"]
        if v1 == "" or v2 == "":
            bouton.text = "En attente du score..."
            bouton.opacity = 0.3
            bouton.background_color = (0.2, 0.2, 0.2, 1)
        elif v1 == v2:
            bouton.text = f"Égalité (TAB) — Qualifié : {match['qualifie']} (Clic pour changer)"
            bouton.opacity = 1
            bouton.background_color = (0.2, 0.6, 0.8, 1) # Bleu action
        else:
            bouton.text = f"Qualifié d'office : {match['qualifie']}"
            bouton.opacity = 1
            bouton.background_color = (0.15, 0.15, 0.15, 1) # Sombre discret

    def generer_ecran_attente(self, objet_onglet, message):
        objet_onglet.clear_widgets()
        objet_onglet.add_widget(Label(
            text=f"[color=7F8C8D]{message}[/color]",
            markup=True, halign="center", valign="middle"
        ))
