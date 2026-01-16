import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model

    def handle_crea_grafo(self, e):
        """ Handler per gestire creazione del grafo """""
        # TODO
        self._view.lista_visualizzazione_1.clean()
        self._view.lista_visualizzazione_2.clean()
        self._view.lista_visualizzazione_3.clean()
        self._view.dd_album.options.clear()
        self._view.dd_album.value = None

        try:
            soglia= float(self._view.txt_durata.value)
        except ValueError:
            self._view.show_alert("Inserire una durata valida")
            return

        self._model.crea_grafo(soglia)

        for a in self._model.album_validi:
            self._view.dd_album.options.append(ft.dropdown.Option(key=str(a.id), text=a.title))



        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo creato: {self._model.G.number_of_nodes()} album, {self._model.G.number_of_edges()} archi"))
        self._view.update()




    def get_selected_album(self, e):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO




    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO
        self._view.lista_visualizzazione_2.controls.clear()


        album_id= self._view.dd_album.value
        if album_id is None:
            self._view.show_alert("Inserire un album")
            return

        album= self._model.dic_album_id[int(album_id)]

        lunghezza_connesse, durata_totale = self._model.trova_connesse(album)

        self._view.lista_visualizzazione_2.controls.append(ft.Text(f"Dimensione componente: {lunghezza_connesse} "
                                                           f"Durata totale: {durata_totale:.2f} minuti"))
        self._view.update()

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO

        self._view.lista_visualizzazione_3.controls.clear()

        album_id= self._view.dd_album.value
        start= self._model.dic_album_id[int(album_id)]
        if start is None:
            self._view.show_alert("Inserire un album")
            return



        try:
            soglia= float(self._view.txt_durata_totale.value)
        except ValueError:
            self._view.show_alert("Inserire una durata valida")
            return

        durata_totale, set_album= self._model.get_percorso_ottimo(start, soglia)

        self._view.lista_visualizzazione_3.controls.append(ft.Text(f"Set trovato: ({len(set_album)} album,  {durata_totale:.2f} minuti"))
        for a in self._model.sequenza_ottima:
            nome_album= a.title
            durata_album= self._model.dic_album_duration[a.id]
            self._view.lista_visualizzazione_3.controls.append(ft.Text(f"-{nome_album} ({durata_album:.2f} minuti)"))
        self._view.update()



