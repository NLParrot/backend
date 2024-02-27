from scipy.spatial import KDTree
import pickle


class MapDB:
    def __init__(self):
        with open("../data/school_road_graph.pkl", "rb") as f:
            self.graph = pickle.load(f)

        self.nodes = list(self.graph.nodes(data=True))
        kdtree_data = list(map(lambda x: [x[1]["y"], x[1]["x"]], self.nodes))
        self.kdt = KDTree(kdtree_data)

    # Use KDTree to find closest node to lat, lng
    def closest_node(self, latitude, longitude):
        _, node_idx = self.kdt.query((latitude, longitude))
        return self.nodes[node_idx][0]

    def eucledian_distance(self, node1, node2):
        pos1 = self.graph.nodes[node1]
        pos2 = self.graph.nodes[node2]
        return (pos1["x"] - pos2["x"]) ** 2 + (pos1["y"] - pos2["y"]) ** 2

    def astar_multidigraph(self, start, goal, heuristic=None):
        if heuristic == None:
            heuristic = self.eucledian_distance

        # Initialize the priority queue (open list) with the start node
        open_list = [(0, start)]  # (score, node)
        # Initialize the dictionary to keep track of the parent nodes
        parent_nodes = {}
        # Initialize the dictionary to keep track of the cost to reach each node from the start node
        g_score = {node: float("inf") for node in self.graph.nodes()}
        g_score[start] = 0

        # A* search
        while open_list:
            # Pop the node with the lowest f score from the open list
            current_f, current_node = min(open_list)
            open_list.remove((current_f, current_node))

            # Check if the current node is the goal node
            if current_node == goal:
                path = [goal]
                while path[-1] != start:
                    path.append(parent_nodes[path[-1]])
                return list(
                    map(
                        lambda n: {
                            "latitude": self.graph.nodes[n]["y"],
                            "longitude": self.graph.nodes[n]["x"],
                        },
                        path[::-1],
                    )
                )

            # Explore neighbors of the current node
            for neighbor in self.graph.successors(current_node):
                # Calculate the tentative g score for the neighbor
                edge_data = self.graph.get_edge_data(current_node, neighbor)
                for _, data in edge_data.items():
                    tentative_g = g_score[current_node] + data["length"]

                    # If this path to the neighbor is better than any previous one, update the records
                    if tentative_g < g_score[neighbor]:
                        parent_nodes[neighbor] = current_node
                        g_score[neighbor] = tentative_g
                        f_score = g_score[neighbor] + heuristic(neighbor, goal)
                        # Add the neighbor to the open list with its f score
                        open_list.append((f_score, neighbor))

        # If open list is empty but goal is not reached, return None
        return None
