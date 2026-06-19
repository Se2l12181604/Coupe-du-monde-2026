import sqlite3

DB_NAME = "worldcup.db"


def connexion():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = connexion()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS matchs(
        phase TEXT,
        groupe TEXT,
        equipe1 TEXT,
        equipe2 TEXT,
        score1 TEXT,
        score2 TEXT,
        PRIMARY KEY(phase, groupe, equipe1, equipe2)
    )
    """)

    conn.commit()
    conn.close()


def sauvegarder_match(
        groupe,
        equipe1,
        equipe2,
        score1,
        score2,
        phase="GROUPES"):

    conn = connexion()
    cur = conn.cursor()

    cur.execute("""
    INSERT OR REPLACE INTO matchs
    (phase,groupe,equipe1,equipe2,score1,score2)
    VALUES(?,?,?,?,?,?)
    """, (
        phase,
        groupe,
        equipe1,
        equipe2,
        score1,
        score2
    ))

    conn.commit()
    conn.close()


def charger_match(
        groupe,
        equipe1,
        equipe2,
        phase="GROUPES"):

    conn = connexion()
    cur = conn.cursor()

    cur.execute("""
    SELECT score1,score2
    FROM matchs
    WHERE phase=?
    AND groupe=?
    AND equipe1=?
    AND equipe2=?
    """, (
        phase,
        groupe,
        equipe1,
        equipe2
    ))

    resultat = cur.fetchone()
    conn.close()
    return resultat


def supprimer_tout():
    conn = connexion()
    cur = conn.cursor()

    cur.execute("DELETE FROM matchs")

    conn.commit()
    conn.close()


def reinitialiser_matchs_groupe(nom_groupe):
    """Supprime tous les scores enregistrés pour un groupe donné."""
    conn = connexion()
    cur = conn.cursor()
    cur.execute("""
        UPDATE matchs 
        SET score1 = NULL, score2 = NULL 
        WHERE groupe = ?
    """, (nom_groupe,))
    conn.commit()
    conn.close()
