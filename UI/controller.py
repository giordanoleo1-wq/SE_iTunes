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
        try:
            soglia= float(self._view.txt_durata.value)
        except:
            self._view.show_alert("Inserire un valore valido per la soglia")
            return

        self._view.lista_visualizzazione_1.controls.clear()
        self._model.crea_grafo(soglia_minuti=soglia)
        self._view.lista_visualizzazione_1.controls.append(ft.Text(f"Grafo creato: {self._model.G.nodes} album, {self._model.G.edges} archi"))
        self._view.update()





    def get_selected_album(self, e, dd):
        """ Handler per gestire la selezione dell'album dal dropdown """""
        # TODO
        albums= self._model.G.nodes
        for a in albums:
            dd.options.append(ft.dropdown.Option(key=a.title))



    def handle_analisi_comp(self, e):
        """ Handler per gestire l'analisi della componente connessa """""
        # TODO

    def handle_get_set_album(self, e):
        """ Handler per gestire il problema ricorsivo di ricerca del set di album """""
        # TODO