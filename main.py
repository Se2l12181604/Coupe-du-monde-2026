from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem

from data import GROUPES
from database import init_db
from UI.groupe_widget import GroupeWidget
from UI.phase_finale_widget import PhaseFinaleWidget


class CoupeDuMondeTabs(TabbedPanel):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.do_default_tab = False
        
        # Dictionnaire pour garder une référence sur l'interface de chaque groupe
        self.onglets_groupes = {}

        # 1. Génération des onglets de Groupes (A à L)
        for lettre, equipes in GROUPES.items():
            onglet = TabbedPanelItem(text=f"Groupe {lettre}")
            widget_groupe = GroupeWidget(lettre, equipes)
            self.onglets_groupes[lettre] = widget_groupe
            onglet.add_widget(widget_groupe)
            self.add_widget(onglet)

        # 2. Ajout du véritable onglet de Phase Finale
        self.onglet_phase_finale = TabbedPanelItem(text="[b]PHASE FINALE[/b]", markup=True)
        self.widget_phase_finale = PhaseFinaleWidget(self)
        self.onglet_phase_finale.add_widget(self.widget_phase_finale)
        self.add_widget(self.onglet_phase_finale)

        # Liaison de l'événement de changement d'onglet
        self.bind(current_tab=self.mettre_a_jour_phase_finale)

    def mettre_a_jour_phase_finale(self, instance, value):
        """Déclenche le rafraîchissement de l'arbre dès que l'onglet Phase Finale est sélectionné."""
        if value.text == "[b]PHASE FINALE[/b]":
            self.widget_phase_finale.rafraichir_arbre()


class WorldCupApp(App):

    def build(self):
        init_db()
        return CoupeDuMondeTabs()


if __name__ == "__main__":
    try:
        WorldCupApp().run()
    except Exception as e:
        import traceback
        with open("crash_log.txt", "w") as f:
            f.write(f"Erreur : {str(e)}\n\n")
            traceback.print_exc(file=f)
