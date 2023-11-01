from river.neighbors import KNNClassifier
from river.neighbors.base import BaseNN, DistanceFunc, FunctionWrapper
from river.base import DriftDetector
from river.neighbors.ann import SWINN
from river.neighbors.ann.nn_vertex import Vertex

class AdaptiveSWINN (SWINN):
    def __init__(self, graph_k: int = 20, dist_func: DistanceFunc | FunctionWrapper | None = None, maxlen: int = 1000, warm_up: int = 500, max_candidates: int = None, delta: float = 0.0001, prune_prob: float = 0, n_iters: int = 10, seed: int = None):
        super().__init__(graph_k, dist_func, maxlen, warm_up, max_candidates, delta, prune_prob, n_iters, seed)
    
    def removeClass (self, yIdx: int):
        """
            for (node) in self._data:
                if node.y == yIdx:
                    nodetoberemove.append(node)
            
        """
        pass
    
    def _removeNode (self, node: Vertex):
        rns = node.r_neighbors()[0]
        ns = node.neighbors()[0]
        node.farewell()

        # Nodes whose only direct neighbor was the removed node
        rns = {rn for rn in rns if not rn.has_neighbors()}
        # Nodes whose only reverse neighbor was the removed node
        ns = {n for n in ns if not n.has_rneighbors()}

        affected = list(rns | ns)
        isolated = rns.intersection(ns)

        # First we handle the unreachable nodes
        for al in isolated:
            neighbors, dists = self._search(al.item, self.graph_k)
            al.fill(neighbors, dists)

        rns -= isolated
        ns -= isolated
        ns = tuple(ns)

        # Nodes with no direct neighbors
        for rn in rns:
            seed = None
            # Check the group of nodes without reverse neighborhood for seeds
            # Thus we can join two separate groups
            if len(ns) > 0:
                seed = self._rng.choice(ns)

            # Use the search index to create new connections
            neighbors, dists = self._search(rn.item, self.graph_k, seed=seed, exclude=rn)
            rn.fill(neighbors, dists)

        self._refine(affected)
        
    

class AdaptiveKNN(KNNClassifier):
    def __init__(self, n_neighbors: int = 5, engine: BaseNN | None = None, weighted: bool = True, cleanup_every: int = 0, softmax: bool = False, driftDetector: DriftDetector = None ):
        super().__init__(n_neighbors, engine, weighted, cleanup_every, softmax)