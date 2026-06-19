def calculer_classement(equipes, matchs):
    # 1. Initialisation du dictionnaire de statistiques pour chaque équipe
    stats = {}
    for equipe in equipes:
        stats[equipe] = {
            "equipe": equipe,
            "J": 0,   # Matchs joués
            "G": 0,   # Gagnés
            "N": 0,   # Nuls
            "P": 0,   # Perdus
            "BP": 0,  # Buts Pour (marqués)
            "BC": 0,  # Buts Contre (encaissés)
            "Pts": 0  # Points
        }

    # 2. Traitement des matchs
    for eq1, eq2, score1, score2 in matchs:
        # On ne traite le match que si les deux scores sont des entiers (saisis)
        if score1 is not None and score2 is not None:
            # Mise à jour des matchs joués et des buts
            stats[eq1]["J"] += 1
            stats[eq2]["J"] += 1
            stats[eq1]["BP"] += score1
            stats[eq1]["BC"] += score2
            stats[eq2]["BP"] += score2
            stats[eq2]["BC"] += score1

            # Attribution des points selon le résultat
            if score1 > score2:      # Victoire Équipe 1
                stats[eq1]["G"] += 1
                stats[eq1]["Pts"] += 3
                stats[eq2]["P"] += 1
            elif score1 < score2:    # Victoire Équipe 2
                stats[eq2]["G"] += 1
                stats[eq2]["Pts"] += 3
                stats[eq1]["P"] += 1
            else:                    # Match nul
                stats[eq1]["N"] += 1
                stats[eq2]["N"] += 1
                stats[eq1]["Pts"] += 1
                stats[eq2]["Pts"] += 1

    # 3. Conversion en liste pour pouvoir trier
    classement_liste = list(stats.values())

    # 4. Tri du classement :
    # Critère 1 : Le nombre de points (Pts) décroissant
    # Critère 2 : La différence de buts (BP - BC) décroissante
    # Critère 3 : Les buts marqués (BP) décroissants
    classement_liste.sort(
        key=lambda x: (x["Pts"], x["BP"] - x["BC"], x["BP"]),
        reverse=True
    )

    return classement_liste
