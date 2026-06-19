from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle

from classement import calculer_classement
from database import sauvegarder_match, charger_match, reinitialiser_matchs_groupe


class CardContainer(BoxLayout):
    """Un conteneur stylisé avec un fond gris foncé et des bords arrondis."""
    def __init__(self, bg_color=(0.15, 0.15, 0.15, 1), **kwargs):
        super().__init__(**kwargs)
        self.bg_color = bg_color
        with self.canvas.before:
            Color(*self.bg_color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[12])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size


class GroupeWidget(ScrollView):

    def __init__(self, nom_groupe, equipes, **kwargs):
        super().__init__(**kwargs)
        self.nom_groupe = nom_groupe
        self.equipes = equipes
        self.inputs = []
        self.classement_actuel = []

        # Conteneur principal
        self.layout_principal = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=20,
            padding=25
        )
        self.layout_principal.bind(minimum_height=self.layout_principal.setter("height"))

        # --- EN-TÊTE DU GROUPE ---
        entete_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=60, spacing=10)

        titre = Label(
            text=f"[b][color=3498db]GROUPE {nom_groupe}[/color][/b]",
            markup=True,
            font_size="24sp",
            halign="left",
            valign="middle",
            size_hint_x=0.7
        )
        titre.bind(size=titre.setter('text_size'))
        
        btn_effacer = Button(
            text="Effacer",
            size_hint_x=0.3,
            size_hint_y=None,
            height=40,
            pos_hint={"center_y": 0.5},
            background_color=(0.9, 0.3, 0.2, 1),
            font_size="13sp",
            bold=True
        )
        btn_effacer.bind(on_release=self.confirmer_reinitialisation)
        
        entete_layout.add_widget(titre)
        entete_layout.add_widget(btn_effacer)
        self.layout_principal.add_widget(entete_layout)

        # --- BLOC 1 : MATCHS ---
        lbl_matchs = Label(
            text="[b]MATCHS DU GROUPE[/b]", 
            markup=True, 
            size_hint_y=None, 
            height=30, 
            font_size="14sp", 
            color=(0.6, 0.6, 0.6, 1),
            halign="left"
        )
        lbl_matchs.bind(size=lbl_matchs.setter('text_size'))
        self.layout_principal.add_widget(lbl_matchs)

        self.carte_matchs = CardContainer(orientation="vertical", size_hint_y=None, spacing=12, padding=15)
        self.carte_matchs.bind(minimum_height=self.carte_matchs.setter("height"))
        self.creer_matchs()
        self.layout_principal.add_widget(self.carte_matchs)

        # --- BLOC 2 : CLASSEMENT ---
        lbl_class = Label(text="[b]Classement En Direct[/b]", markup=True, size_hint_y=None, height=30, font_size="16sp", halign="left")
        lbl_class.bind(size=lbl_class.setter('text_size'))
        self.layout_principal.add_widget(lbl_class)

        self.carte_classement = CardContainer(orientation="vertical", size_hint_y=None, spacing=5, padding=15)
        self.carte_classement.bind(minimum_height=self.carte_classement.setter("height"))
        
        self.tableau = GridLayout(cols=10, size_hint_y=None, spacing=2)
        self.tableau.bind(minimum_height=self.tableau.setter("height"))
        self.carte_classement.add_widget(self.tableau)
        
        self.layout_principal.add_widget(self.carte_classement)
        self.add_widget(self.layout_principal)

        # Calcul au démarrage
        self.calculer()

    def creer_matchs(self):
        combinaisons = [(0, 1), (2, 3), (0, 2), (1, 3), (0, 3), (1, 2)]

        for a, b in combinaisons:
            eq1, eq2 = self.equipes[a], self.equipes[b]

            ligne = BoxLayout(orientation="horizontal", size_hint_y=None, height=50, spacing=10)
            ligne.add_widget(Label(text=eq1, halign="right", font_size="16sp", size_hint_x=0.35))

            # Saisie Équipe 1
            btn_moins1 = Button(text="-", size_hint_x=None, width=40, background_color=(0.7, 0.2, 0.2, 1))
            score1 = TextInput(text="", multiline=False, input_filter="int", size_hint_x=None, width=45, halign="center", font_size="16sp", input_type="number")
            btn_plus1 = Button(text="+", size_hint_x=None, width=40, background_color=(0.2, 0.6, 0.2, 1))

            ligne.add_widget(btn_moins1)
            ligne.add_widget(score1)
            ligne.add_widget(btn_plus1)

            ligne.add_widget(Label(text="VS", size_hint_x=None, width=30, halign="center", color=(0.5, 0.5, 0.5, 1)))

            # Saisie Équipe 2
            btn_moins2 = Button(text="-", size_hint_x=None, width=40, background_color=(0.7, 0.2, 0.2, 1))
            score2 = TextInput(text="", multiline=False, input_filter="int", size_hint_x=None, width=45, halign="center", font_size="16sp", input_type="number")
            btn_plus2 = Button(text="+", size_hint_x=None, width=40, background_color=(0.2, 0.6, 0.2, 1))

            ligne.add_widget(btn_moins2)
            ligne.add_widget(score2)
            ligne.add_widget(btn_plus2)

            ligne.add_widget(Label(text=eq2, halign="left", font_size="16sp", size_hint_x=0.35))

            # Chargement BDD
            sauvegarde = charger_match(self.nom_groupe, eq1, eq2)
            if sauvegarde:
                score1.text = str(sauvegarde[0]) if sauvegarde[0] is not None else ""
                score2.text = str(sauvegarde[1]) if sauvegarde[1] is not None else ""

            # CORRECTION LOGIQUE SYNTAXE : Liaison propre sans lambda anonyme instable
            score1.bind(text=self.sur_changement_texte)
            score2.bind(text=self.sur_changement_texte)

            # Boutons + et -
            btn_plus1.bind(on_release=lambda x, s=score1: self.modifier_score(s, 1))
            btn_moins1.bind(on_release=lambda x, s=score1: self.modifier_score(s, -1))
            btn_plus2.bind(on_release=lambda x, s=score2: self.modifier_score(s, 1))
            btn_moins2.bind(on_release=lambda x, s=score2: self.modifier_score(s, -1))

            self.inputs.append((eq1, eq2, score1, score2))
            self.carte_matchs.add_widget(ligne)

    def sur_changement_texte(self, instance, value):
        """Méthode de secours propre appelée à chaque saisie de score."""
        self.calculer()

    def modifier_score(self, input_field, valeur):
        actuel = input_field.text.strip()
        if actuel == "":
            nouveau = 0 if valeur > 0 else ""
        else:
            nouveau = max(0, int(actuel) + valeur)
        input_field.text = str(nouveau)

    def calculer(self, *args):
        liste_matchs_sauvegarde = []

        for eq1, eq2, s1, s2 in self.inputs:
            val1 = s1.text.strip()
            val2 = s2.text.strip()

            if val1 != "" and val2 != "":
                sauvegarder_match(self.nom_groupe, eq1, eq2, int(val1), int(val2))
                liste_matchs_sauvegarde.append((eq1, eq2, int(val1), int(val2)))
            else:
                sauvegarder_match(self.nom_groupe, eq1, eq2, None, None)
                liste_matchs_sauvegarde.append((eq1, eq2, None, None))

        self.classement_actuel = calculer_classement(self.equipes, liste_matchs_sauvegarde)
        self.tableau.clear_widgets()

        headers = ["Pos", "Équipe", "J", "G", "N", "P", "BP", "BC", "Diff", "Pts"]
        self.tableau.cols = len(headers)
        
        for h in headers:
            self.tableau.add_widget(Label(text=f"[b]{h}[/b]", markup=True, size_hint_y=None, height=40, font_size="14sp", color=(0.7, 0.7, 0.7, 1)))

        for index, r in enumerate(self.classement_actuel):
            pos = index + 1
            if pos <= 2:
                couleur = "2ECC71"
            elif pos == 3:
                couleur = "3498DB"
            else:
                couleur = "E74C3C"

            self.tableau.add_widget(Label(text=f"[color={couleur}]{pos}[/color]", markup=True, size_hint_y=None, height=35))
            self.tableau.add_widget(Label(text=f"[color={couleur}][b]{r['equipe']}[/b][/color]", markup=True, size_hint_y=None, height=35, font_size="14sp"))
            self.tableau.add_widget(Label(text=str(r["J"]), size_hint_y=None, height=35))
            self.tableau.add_widget(Label(text=str(r["G"]), size_hint_y=None, height=35))
            self.tableau.add_widget(Label(text=str(r["N"]), size_hint_y=None, height=35))
            self.tableau.add_widget(Label(text=str(r["P"]), size_hint_y=None, height=35))
            self.tableau.add_widget(Label(text=str(r["BP"]), size_hint_y=None, height=35))
            self.tableau.add_widget(Label(text=str(r["BC"]), size_hint_y=None, height=35))
            
            diff = r["BP"] - r["BC"]
            signe = "+" if diff > 0 else ""
            self.tableau.add_widget(Label(text=f"{signe}{diff}", size_hint_y=None, height=35))
            self.tableau.add_widget(Label(text=f"[b]{r['Pts']}[/b]", markup=True, size_hint_y=None, height=35, font_size="15sp"))

    def obtenir_resultats_groupe(self):
        return self.classement_actuel
        
    def confirmer_reinitialisation(self, instance):
        reinitialiser_matchs_groupe(self.nom_groupe)
        for eq1, eq2, score1, score2 in self.inputs:
            score1.text = ""
            score2.text = ""
        self.calculer()
