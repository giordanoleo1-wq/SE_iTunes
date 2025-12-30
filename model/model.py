import networkx as nx
from database.dao import DAO
from model.album import Album


class Model:
    def __init__(self):
        self.G = nx.Graph()

        self.track_to_album = {}
        self.album_duration = {}
        self.valid_albums = set()
        self.playlist_to_albums = {}

        self.albums = {}


    def load_data(self):
        tracks = DAO.read_all_tracks()
        albums = DAO.read_all_albums()
        playlist_tracks = DAO.read_all_playlists_track()

        self.albums = {a.id: a for a in albums}

        for t in tracks:
            self.track_to_album[t.id] = t.album_id

            if t.album_id not in self.album_duration:
                self.album_duration[t.album_id] = 0
            self.album_duration[t.album_id] += t.milliseconds

        for playlist_id, track_id in playlist_tracks:
            album_id = self.track_to_album.get(track_id)
            if album_id is None:
                continue

            if playlist_id not in self.playlist_to_albums:
                self.playlist_to_albums[playlist_id] = set()

            self.playlist_to_albums[playlist_id].add(album_id)


    def crea_grafo(self, soglia_minuti):
        self.G.clear()

        self.track_to_album.clear()
        self.album_duration.clear()
        self.playlist_to_albums.clear()
        self.valid_albums.clear()

        self.load_data()

        soglia_ms = soglia_minuti * 60 * 1000

        for album_id, durata in self.album_duration.items():
            if durata > soglia_ms:
                self.valid_albums.add(album_id)
                self.G.add_node(self.albums[album_id])

        for album_set in self.playlist_to_albums.values():
            valid = [a for a in album_set if a in self.valid_albums]

            for i in range(len(valid)):
                for j in range(i + 1, len(valid)):
                    a1 = self.albums[valid[i]]
                    a2 = self.albums[valid[j]]
                    self.G.add_edge(a1, a2)


    def analisi_componente(self, album: Album):
        component = nx.node_connected_component(self.G, album)

        dimensione = len(component)
        durata_totale = sum(
            self.album_duration[a.id] for a in component
        ) // (60 * 1000)

        return dimensione, durata_totale

    def get_ottimo(self, soglia):
        pass


    def _ricorsione(self, album : Album, percorso_parziale, tempo_parziale, soglia):
        pass











