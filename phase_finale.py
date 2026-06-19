def determiner_les_32(tous_les_groupes_classements):
    """
    Prend en paramètre un dictionnaire contenant les classements des 12 groupes :
    {'A': [...], 'B': [...], ...}
    Retourne la liste des 32 équipes qualifiées.
    """
    qualifies_directs = []
    tous_les_troisiesmes = []

    # 1. Extraction des 1ers, 2èmes et 3èmes
    for lettre, classement in tous_les_groupes_classements.items():
        if len(classement) >= 4:
            qualifies_directs.append({"groupe": lettre, "position": 1, "equipe": classement[0]["equipe"]})
            qualifies_directs.append({"groupe": lettre, "position": 2, "equipe": classement[1]["equipe"]})
            
            # On garde les stats du 3ème pour pouvoir les départager globalement
            troisieme = classement[2]
            tous_les_troisiesmes.append({
                "groupe": lettre,
                "equipe": troisieme["equipe"],
                "Pts": troisieme["Pts"],
                "Diff": troisieme["BP"] - troisieme["BC"],
                "BP": troisieme["BP"]
            })

    # 2. Tri des 3èmes selon les critères de la FIFA
    # Points -> Différence de buts -> Buts marqués
    tous_les_troisiesmes.sort(key=lambda x: (x["Pts"], x["Diff"], x["BP"]), reverse=True)

    # On ne garde que les 8 meilleurs
    meilleurs_troisiesmes = tous_les_troisiesmes[:8]
    for t in meilleurs_troisiesmes:
        t["position"] = 3

    # 3. Regroupement complet des 32 rescapés
    les_32 = qualifies_directs + meilleurs_troisiesmes
    return les_32, tous_les_troisiesmes


def generer_seiziemes(les_32):
    """
    Génère l'arbre des 16èmes de finale selon le tableau de la Coupe du Monde 2026.
    Pour simplifier l'affectation complexe des meilleurs 3èmes, on applique une logique de tableau fixe.
    """
    # Indexation rapide pour retrouver une équipe par son groupe et sa position
    dict_equipes = {}
    meilleurs_3es = []
    
    for eq in les_32:
        if eq["position"] == 3:
            meilleurs_3es.append(eq["equipe"])
        else:
            dict_equipes[f"{eq['groupe']}{eq['position']}"] = eq["equipe"]

    # Remplissage par défaut en attendant les 3èmes
    def obtenir_equipe(cle):
        return dict_equipes.get(cle, f"2e {cle[0]}" if cle[1]=='2' else f"1er {cle[0]}")

    # Simulation du tableau officiel des 16 affiches des 1/16 de finale
    # (Mélange officiel des 1ers vs 3èmes et 2èmes vs 2èmes)
    affiches = [
        {"id": 1, "eq1": obtenir_equipe("A1"), "eq2": meilleurs_3es[0] if len(meilleurs_3es) > 0 else "3ème Grp"},
        {"id": 2, "eq1": obtenir_equipe("B2"), "eq2": obtenir_equipe("F2")},
        {"id": 3, "eq1": obtenir_equipe("E1"), "eq2": meilleurs_3es[1] if len(meilleurs_3es) > 1 else "3ème Grp"},
        {"id": 4, "eq1": obtenir_equipe("I1"), "eq2": obtenir_equipe("J2")},
        
        {"id": 5, "eq1": obtenir_equipe("C1"), "eq2": meilleurs_3es[2] if len(meilleurs_3es) > 2 else "3ème Grp"},
        {"id": 6, "eq1": obtenir_equipe("D2"), "eq2": obtenir_equipe("H2")},
        {"id": 7, "eq1": obtenir_equipe("G1"), "eq2": meilleurs_3es[3] if len(meilleurs_3es) > 3 else "3ème Grp"},
        {"id": 8, "eq1": obtenir_equipe("K1"), "eq2": obtenir_equipe("L2")},

        {"id": 9, "eq1": obtenir_equipe("B1"), "eq2": meilleurs_3es[4] if len(meilleurs_3es) > 4 else "3ème Grp"},
        {"id": 10, "eq1": obtenir_equipe("A2"), "eq2": obtenir_equipe("C2")},
        {"id": 11, "eq1": obtenir_equipe("F1"), "eq2": meilleurs_3es[5] if len(meilleurs_3es) > 5 else "3ème Grp"},
        {"id": 12, "eq1": obtenir_equipe("K2"), "eq2": obtenir_equipe("I2")},

        {"id": 13, "eq1": obtenir_equipe("D1"), "eq2": meilleurs_3es[6] if len(meilleurs_3es) > 6 else "3ème Grp"},
        {"id": 14, "eq1": obtenir_equipe("E2"), "eq2": obtenir_equipe("G2")},
        {"id": 15, "eq1": obtenir_equipe("H1"), "eq2": meilleurs_3es[7] if len(meilleurs_3es) > 7 else "3ème Grp"},
        {"id": 16, "eq1": obtenir_equipe("J1"), "eq2": obtenir_equipe("L2")}
    ]
    
    return affiches
