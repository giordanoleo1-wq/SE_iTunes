from database.DB_connect import DBConnect
from model.album import Album
from model.connessione import Connessione
from model.track import Track


class DAO:
    @staticmethod
    def read_all_tracks():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM track """

        cursor.execute(query)

        for row in cursor:
            result.append(Track(**row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def read_all_albums():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM album """

        cursor.execute(query)

        for row in cursor:
            result.append(Album(** row))

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def read_all_connessioni():
        conn = DBConnect.get_connection()
        result = []
        cursor = conn.cursor(dictionary=True)
        query = """ SELECT * FROM playlist_track """

        cursor.execute(query)

        for row in cursor:
            result.append(Connessione(** row))

        cursor.close()
        conn.close()
        return result