import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model



    def handleCreaGrafo(self, e):
        storeId = self._view._ddStore.value
        if storeId is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare uno store.", color="red"))
            self._view.update_page()
            return
        strK = self._view._txtIntK.value
        if strK == "":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Inserire numero massimo di giorni k.", color="red"))
            self._view.update_page()
            return
        try:
            k = int(strK)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"K deve essere un intero.", color="red"))
            self._view.update_page()
            return
        if k <= 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"K deve essere un intero positivo.", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(k, storeId)
        self.fillddNode(storeId)
        n, e = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato:"))
        self._view.txt_result.controls.append(ft.Text(f"Numero nodi: {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero archi: {e}"))
        self._view.update_page()


    def handleCerca(self, e):
        strNode = self._view._ddNode.value
        if strNode is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un nodo sorgente.", color="red"))
            self._view.update_page()
            return
        try:
            node = int(strNode)
        except ValueError:
            print("errore")
            return
        sol = self._model.cercaPercorso(node)
        self._view.txt_result.controls.append(ft.Text(f"Nodo di partenza: {node}"))
        for n in sol:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()



    def handleRicorsione(self, e):
        strNode = self._view._ddNode.value
        if strNode is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Selezionare un nodo sorgente.", color="red"))
            self._view.update_page()
            return
        try:
            node = int(strNode)
        except ValueError:
            print("errore")
            return
        bestPath, bestScore = self._model.getBestPath(node)
        self._view.txt_result.controls.append(ft.Text(f"---- Risultato ricorsione -----"))
        self._view.txt_result.controls.append(ft.Text(f"Score: {bestScore}"))
        self._view.txt_result.controls.append(ft.Text(f"Nodi del best path:"))
        for n in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()


    def fillddStore(self):
        stores = self._model.getAllStores()
        for store in stores:
            self._view._ddStore.options.append(ft.dropdown.Option(store.store_id))
        self._view.update_page()

    def fillddNode(self, storeId):
        self._view._ddNode.options.clear()
        nodes = self._model.getAllOrdersByStore(storeId)
        for node in nodes:
            self._view._ddNode.options.append(ft.dropdown.Option(node))
        self._view.update_page()
