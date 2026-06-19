import os

def exporter_tournoi_excel_csv(tous_les_classements, chemin_dossier=None):
    """Génère un fichier CSV structuré pour Excel avec l'encodage universel."""
    if chemin_dossier is None:
        # Enregistre par défaut dans le dossier du projet
        chemin_dossier = os.path.dirname(os.path.abspath(__file__))
        
    nom_fichier = os.path.join(chemin_dossier, "Rapport_Coupe_du_Monde_2026.csv")
    
    try:
        with open(nom_fichier, "w", encoding="utf-8-sig") as f:
            # En-tête compatible Excel (séparateur point-virgule pour la version française)
            f.write("Groupe;Position;Equipe;Matchs Joues;Gagnes;Nuls;Perdus;Buts Pour;Buts Contre;Difference;Points\n")
            
            for lettre, classement in tous_les_classements.items():
                for index, r in enumerate(classement):
                    pos = index + 1
                    diff = r["BP"] - r["BC"]
                    signe = "+" if diff > 0 else ""
                    
                    ligne = f"{lettre};{pos};{r['equipe']};{r['J']};{r['G']};{r['N']};{r['P']};{r['BP']};{r['BC']};{signe}{diff};{r['Pts']}\n"
                    f.write(ligne)
                    
        return f"Export réussi !\nFichier enregistré sous :\n{nom_fichier}"
    except Exception as e:
        return f"Erreur lors de l'exportation : {str(e)}"
