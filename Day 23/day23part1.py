import itertools

TEST1 = "test1.txt"
INPUT = "input.txt"

class PartyNetwork:
    def __init__(self, filename):
        self.nodes_dict = {}
        with open(filename) as file:
            for line in file:
                line = line.strip()
                assert len(line) == 5
                node1 = line[0:2]
                node2 = line[3:5]

                if node1 not in self.nodes_dict:
                    self.nodes_dict[node1] = set()
                self.nodes_dict[node1].add(node2)

                if node2 not in self.nodes_dict:
                    self.nodes_dict[node2] = set()
                self.nodes_dict[node2].add(node1)

    def find_clusters(self, cluster_size: int):
        confirmed_clusters = set()
        for start_node in self.nodes_dict.keys():
            connected_nodes = self.nodes_dict[start_node]
            if len(connected_nodes) >= cluster_size - 1:
                possible_cluster_other_node_groups = itertools.permutations(connected_nodes, cluster_size - 1)
                for possible_cluster_other_node_group in possible_cluster_other_node_groups:
                    possible_cluster = list(possible_cluster_other_node_group)
                    possible_cluster.append(start_node)
                    possible_cluster.sort()
                    possible_cluster = tuple(possible_cluster)
                    if possible_cluster not in confirmed_clusters:
                        valid_cluster = True
                        for node1 in possible_cluster:
                            if not valid_cluster:
                                break
                            for node2 in possible_cluster:
                                if node1 == node2:
                                    continue
                                if node2 not in self.nodes_dict[node1]:
                                    valid_cluster = False
                                    break
                        if valid_cluster:
                            confirmed_clusters.add(possible_cluster)
        return confirmed_clusters

    def solve(self, cluster_size:int, node_start_letter: str):
        possible_clusters = self.find_clusters(cluster_size)
        valid_clusters = []
        for cluster in possible_clusters:
            for node in cluster:
                if node[0] == node_start_letter:
                    valid_clusters.append(cluster)
                    break
        return valid_clusters






if __name__ == "__main__":
    pn = PartyNetwork(INPUT)

    sol = pn.solve(3, "t")
    print(sol)
    print(len(sol))