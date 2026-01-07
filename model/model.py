import networkx as nx
from database.dao import DAO
from model.album import Album


class Model:
    def __init__(self):
        self.G= nx.Graph()
        self.lista_tracks = []
        self.lista_connessioni_track_playlist = []
        self.lista_albums = []
        self.dic_album_id= {}
        self.dic_track_id= {}
        self.dic_album_to_track= {}
        self.dic_album_duration= {}
        self.dic_playlist_to_track= {}
        self.album_validi= []
        self.connesse= set()
        self.durata_totale= 0
        self.durata_ottima = 0
        self.sequenza_ottima = []



    def load_all_tracks(self):
        self.lista_tracks = DAO.read_all_tracks()
    def load_all_albums(self):
        self.lista_albums= DAO.read_all_albums()
    def load_all_connessioni_track_playlist(self):
        self.lista_connessioni_track_playlist= DAO.read_all_connessioni()


    def crea_grafo(self, soglia):
        self.G= nx.Graph()
        self.load_all_tracks()
        self.load_all_albums()
        self.load_all_connessioni_track_playlist()
        self.album_validi = []




        for a in self.lista_albums:
            self.dic_album_id[a.id]= a

        for t in self.lista_tracks:
            self.dic_track_id[t.id]= t

            if t.album_id not in self.dic_album_to_track:
                self.dic_album_to_track[t.album_id]= set()
            self.dic_album_to_track[t.album_id].add(t)

        for album in self.dic_album_to_track.keys():
            if album not in self.dic_album_duration:
                self.dic_album_duration[album] = 0
            for t in self.dic_album_to_track[album]:
                self.dic_album_duration[album] += t.milliseconds
            durata_minuti= self.dic_album_duration[album] /(1000* 60)
            self.dic_album_duration[album] = durata_minuti


        for p_t in self.lista_connessioni_track_playlist:
            if p_t.track_id not in self.dic_playlist_to_track:
                self.dic_playlist_to_track[p_t.track_id]= set()
            self.dic_playlist_to_track[p_t.track_id].add(p_t.playlist_id)



        for a in self.lista_albums:
            if self.dic_album_duration[a.id] >= soglia:
                self.G.add_node(a)
                self.album_validi.append(a)


        for i in range(len(self.album_validi)):
            for j in range(i+1, len(self.album_validi)):
                a1 = self.album_validi[i]
                a2 = self.album_validi[j]

                trovato= False
                for t1 in self.dic_album_to_track[a1.id]:
                    for t2 in self.dic_album_to_track[a2.id]:
                        if self.dic_playlist_to_track[t1.id]&self.dic_playlist_to_track[t2.id]:
                            self.G.add_edge(a1, a2)
                            trovato = True
                            break
                    if trovato:
                        break


        print(self.G)


    def trova_connesse(self, album):
        self.durata_totale = 0
        self.connesse = set()

        if album in self.album_validi:
            self.connesse= nx.node_connected_component(self.G, album)
            for a in self.connesse:
                durata_minuti= self.dic_album_duration[a.id]
                self.durata_totale += durata_minuti
        return len(self.connesse), self.durata_totale

    def get_percorso_ottimo(self, start, soglia):
        self.durata_ottima= 0
        self.sequenza_ottima= []
        self.connesse = nx.node_connected_component(self.G, start)
        set_album_usati= set()

        durata_start= self.dic_album_duration[start.id]
        set_album_usati= {start}
        self.ricorsione(start, [start], durata_start, set_album_usati, soglia)
        return self.durata_ottima, self.sequenza_ottima


    def ricorsione(self, start: Album, sequenza_parziale, durata_parziale, set_album_usati, soglia ):

        if durata_parziale > soglia:
            return

        if len(sequenza_parziale) > len(self.sequenza_ottima):
            self.sequenza_ottima = list(sequenza_parziale)
            self.durata_ottima = durata_parziale


        for vicino in self.G.neighbors(start):
            if vicino not in self.connesse:
                continue
            if vicino in set_album_usati:
                continue
            durata_vicino= self.dic_album_duration[vicino.id]

            if durata_parziale + durata_vicino < soglia:
                sequenza_parziale.append(vicino)
                set_album_usati.add(vicino)
                self.ricorsione(vicino, sequenza_parziale, durata_parziale + durata_vicino, set_album_usati, soglia)

                sequenza_parziale.pop()
                set_album_usati.remove(vicino)





























