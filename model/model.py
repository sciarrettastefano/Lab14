import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.DiGraph()
        self._orders = []
        self._idMapOrders = {}
        self._bestPath = []
        self._bestScore = 0


    def buildGraph(self, k, storeId):
        self._graph.clear()
        self._orders = self.getAllOrdersByStore(storeId)
        if len(self._orders) == 0:
            print("No orders found")
            return
        self._graph.add_nodes_from(self._orders)
        edges = self.getAllEdges(k, storeId)
        for edge in edges:
            self._graph.add_edge(edge[0], edge[1], weight=edge[2])


    def getBestPath(self, source):
        self._bestPath = []
        self._bestScore = 0
        parziale = [self._idMapOrders[source]]
        vicini = self._graph.neighbors(self._idMapOrders[source])
        for v in vicini:
            parziale.append(v)
            self._ricorsione(parziale)
            parziale.pop()
        return self._bestPath, self._bestScore


    def _ricorsione(self, parziale, ):
        if self.score(parziale) > self._bestScore:
            self._bestScore = self.score(parziale)
            self._bestPath = copy.deepcopy(parziale)
        #ricorsione
        for v in self._graph.neighbors(parziale[-1]):
            if (v not in parziale and
                self._graph[parziale[-2]][parziale[-1]]['weight'] >
                self._graph[parziale[-1]][v]['weight']):
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()


    def score(self, parziale):
        if len(parziale) < 2:
            return
        score = 0
        for i in range(len(parziale) - 1):
            score += self._graph[parziale[i]][parziale[i + 1]]['weight']
        return score


    def cercaPercorso(self, partenza):
        p = self._idMapOrders[partenza]

        tree = nx.dfs_tree(self._graph, p)
        nodes = list(tree.nodes())
        sol = []
        for node in nodes:
            temp = [node]
            while temp[0] != p:
                pred = nx.predecessor(tree, p, temp[0])
                temp.insert(0, pred[0])
            if len(temp) > len(sol):
                sol = copy.deepcopy(temp)
        return sol


    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllStores(self):
        return DAO.getAllStores()

    def getAllOrdersByStore(self, storeId):
        self._orders = DAO.getAllOrders(storeId)
        for o in self._orders:
            self._idMapOrders[o.order_id] = o
        return DAO.getAllOrders(storeId)

    def getAllEdges(self, k, storeId):
        return DAO.getAllEdges(k, storeId, self._idMapOrders)

