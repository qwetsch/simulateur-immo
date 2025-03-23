import sqlite3
from datetime import datetime

DB_FILE = "simulateur.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS projets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            nom TEXT UNIQUE,
            prix REAL,
            surface REAL,
            frais_notaire REAL,
            frais_agence REAL,
            achat_mobilier REAL,
            travaux REAL,
            loyer REAL,
            charges_recuperable REAL,
            charges_copro REAL,
            taxe_fonciere REAL,
            assurance REAL,
            frais_gestion REAL,
            frais_dossier REAL,
            apport_personnel REAL,
            montant_pret REAL,
            taux_interet REAL,
            duree_pret REAL
        )
    """)
    conn.commit()
    conn.close()

def save_project(nom, data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT OR REPLACE INTO projets (
            timestamp, nom, prix, surface, frais_notaire, frais_agence, achat_mobilier,
            travaux, loyer, charges_recuperable, charges_copro, taxe_fonciere,
            assurance, frais_gestion, frais_dossier, apport_personnel,
            montant_pret, taux_interet, duree_pret
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        nom,
        data["prix"],
        data["surface"],
        data["frais_notaire"],
        data["frais_agence"],
        data["achat_mobilier"],
        data["travaux"],
        data["loyer"],
        data["charges_recuperable"],
        data["charges_copro"],
        data["taxe_fonciere"],
        data["assurance"],
        data["frais_gestion"],
        data["frais_dossier"],
        data["apport_personnel"],
        data["montant_pret"],
        data["taux_interet"],
        data["duree_pret"]
    ))
    conn.commit()
    conn.close()

def list_projects():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT nom FROM projets")
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]

def load_project(nom):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM projets WHERE nom = ?", (nom,))
    row = c.fetchone()
    conn.close()
    if row:
        return {
            "prix": row[3],
            "surface": row[4],
            "frais_notaire": row[5],
            "frais_agence": row[6],
            "achat_mobilier": row[7],
            "travaux": row[8],
            "loyer": row[9],
            "charges_recuperable": row[10],
            "charges_copro": row[11],
            "taxe_fonciere": row[12],
            "assurance": row[13],
            "frais_gestion": row[14],
            "frais_dossier": row[15],
            "apport_personnel": row[16],
            "montant_pret": row[17],
            "taux_interet": row[18],
            "duree_pret": row[19]
        }
    return None