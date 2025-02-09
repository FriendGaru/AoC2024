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

        self.nodes_dict_plus_self = {}
        for key, value in self.nodes_dict.items():
            self.nodes_dict_plus_self[key] = value
            self.nodes_dict_plus_self[key].add(key)

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

    def find_clusters_that_contain_slow(self, node_name:str, min_cluster_size):
        all_other_nodes = self.nodes_dict[node_name]
        confirmed_clusters = set()
        for cluster_size in range(min_cluster_size, len(all_other_nodes) + 1):
            possible_groups_of_other_nodes = itertools.permutations(all_other_nodes, cluster_size - 1)
            for possible_group_of_other_nodes in possible_groups_of_other_nodes:
                print(possible_group_of_other_nodes)
                valid = True
                for node1 in possible_group_of_other_nodes:
                    if not valid:
                        break
                    for node2 in possible_group_of_other_nodes:
                        if node1 == node2:
                            continue
                        else:
                            if node2 not in self.nodes_dict[node1]:
                                valid = False
                                break
                if valid:
                    possible_group_of_other_nodes = list(possible_group_of_other_nodes)
                    possible_group_of_other_nodes.append(node_name)
                    possible_group_of_other_nodes.sort()
                    possible_group_of_other_nodes = tuple(possible_group_of_other_nodes)
                    confirmed_clusters.add(possible_group_of_other_nodes)
        return confirmed_clusters

    def grow_cluster(self, current_cluster: tuple, already_found_clusters:set, rejected_nodes: set):
        current_cluster = sorted(current_cluster)
        current_cluster = tuple(current_cluster)
        front_node = current_cluster[0]
        possible_expansion_nodes = self.nodes_dict[front_node]
        confirmed_sub_clusters = set()
        for possible_expansion_node in possible_expansion_nodes:
            sub_cluster = list(current_cluster)
            sub_cluster.append(possible_expansion_node)
            sub_cluster = sorted(sub_cluster)
            sub_cluster = tuple(sub_cluster)

            if sub_cluster in already_found_clusters:
                continue

            valid = True
            possible_expansion_node_connections = self.nodes_dict[possible_expansion_node]
            for current_cluster_node in current_cluster:
                if current_cluster_node not in possible_expansion_node_connections:
                    valid = False
                    break
            if not valid:
                continue
            else:

                sub_sub_clusters = self.grow_cluster(sub_cluster, confirmed_sub_clusters, rejected_nodes)
                for sub_sub_cluster in sub_sub_clusters:
                    confirmed_sub_clusters.add(sub_sub_cluster)
        confirmed_sub_clusters.add(current_cluster)
        return confirmed_sub_clusters



    def find_biggest_cluster_that_contains(self, contained_nodes_set: set, already_found_dict: dict=None):
        if already_found_dict is None:
            already_found_dict = {}
        set_key = tuple(sorted(contained_nodes_set))
        if set_key in already_found_dict:
            return already_found_dict[set_key]
        assert len(contained_nodes_set) > 0
        sorted_contained_nodes = sorted(contained_nodes_set)
        potential_nodes_set = None
        for c_node in sorted_contained_nodes:
            node_set_w_self = self.nodes_dict_plus_self[c_node]
            if potential_nodes_set is None:
                potential_nodes_set = node_set_w_self
            else:
                potential_nodes_set = potential_nodes_set.intersection(node_set_w_self)
        if not potential_nodes_set.issuperset(contained_nodes_set):
            raise ValueError("Bad node set")

        best_cluster = contained_nodes_set
        nodes_to_try = potential_nodes_set.difference(contained_nodes_set)

        for expansion_node in nodes_to_try:
            trial_cluster = contained_nodes_set.copy()
            trial_cluster.add(expansion_node)
            trial_best_cluster = self.find_biggest_cluster_that_contains(trial_cluster, already_found_dict)
            if len(trial_best_cluster) > len(best_cluster):
                best_cluster = trial_best_cluster

        already_found_dict[set_key] = best_cluster
        return best_cluster

    def find_biggest_cluster(self):
        very_best_cluster = None
        already_found_dict = {}
        for node in self.nodes_dict.keys():
            print(node)
            trial_cluster = set()
            trial_cluster.add(node)
            best_trial_cluster = self.find_biggest_cluster_that_contains(trial_cluster, already_found_dict)
            if very_best_cluster is None:
                very_best_cluster = best_trial_cluster
            elif len(best_trial_cluster) > len(very_best_cluster):
                very_best_cluster = best_trial_cluster
        return sorted(very_best_cluster)







if __name__ == "__main__":
    pn = PartyNetwork(INPUT)

    # sol = pn.find_biggest_cluster()
    # sol = sorted(sol)
    # print(sol)
    # print(len(sol))

    # print(pn.grow_cluster(["co",], set(), set()))

    # for key in sorted(pn.nodes_dict_plus_self.keys()):
    #     print(key, pn.nodes_dict_plus_self[key])

    # thing_list = ["co", "de", "ka", "ta"]
    # thing_list = ["ka", "ta"]
    # thing_set = pn.nodes_dict_plus_self["co"]
    # for key in thing_list:
    #     thing_set = thing_set.intersection(pn.nodes_dict_plus_self[key])
    # print(thing_set)


    sol = pn.find_biggest_cluster()
    print(sol)
    print(",".join(sol))