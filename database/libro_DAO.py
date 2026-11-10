from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        pass

    def get_all_generi(self):
        """Restituisce la lista di tutti i generi distinti presenti nel database."""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return result

        cursor = cnx.cursor(dictionary=True)
        query = "SELECT DISTINCT genere FROM libro WHERE genere IS NOT NULL ORDER BY genere"
        cursor.execute(query)

        for row in cursor:
            if row["genere"]:
                result.append(row["genere"])

        cursor.close()
        cnx.close()
        return result

    def get_libri_filtrati(self, biblioteca, genere):
        """Restituisce i libri filtrati per nome biblioteca e/o genere gestendo i filtri opzionali."""
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            return result

        cursor = cnx.cursor(dictionary=True)

        # Utilizziamo COALESCE o condizioni logiche per gestire i filtri opzionali
        query = """
            SELECT l.id, l.titolo, l.autore, l.genere, l.anno_pubblicazione, l.id_biblioteca
            FROM libro l
            JOIN biblioteca b ON l.id_biblioteca = b.id
            WHERE (%s IS NULL OR b.nome = %s)
              AND (%s IS NULL OR l.genere = %s)
        """
        cursor.execute(query, (biblioteca, biblioteca, genere, genere))

        for row in cursor:
            result.append(Libro(
                id=row["id"],
                titolo=row["titolo"],
                autore=row["autore"],
                genere=row["genere"],
                anno_pubblicazione=row["anno_pubblicazione"],
                id_biblioteca=row["id_biblioteca"]
            ))

        cursor.close()
        cnx.close()
        return result
