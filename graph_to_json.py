import networkx as nx
import pandas as pd
import networkx.algorithms.community as nxComm
from networkx.readwrite import json_graph
import json


def load_graph(edges_path, nodes_path):
    g = nx.Graph()
    edges0 = pd.read_csv(edges_path)
    list_edges = edges0.values.tolist()
    for row in list_edges:
        g.add_edge(row[0], row[1])

    # Añadir atributos
    nodes0 = pd.read_csv(nodes_path)
    list_nodes = nodes0[['new_id', 'name', 'country', 'country_id', 'chef']].values.tolist()
    # print(list_nodes)
    for row in list_nodes:
        g.add_node(row[0], name=row[1], country=row[2], country_id=row[3], chef=row[4])
    # print(g.nodes)
    return g


def get_communities(g):
    """
    Perform community detection algorithms over g
    :param g:
    :return:
    """
    comm_greedy = list(nxComm.greedy_modularity_communities(g))
    comm_label = list(nxComm.label_propagation_communities(g))
    comm_dict = {
        'greedy': comm_greedy,
        'label': comm_label
    }
    return comm_dict


def get_centrality_metrics(g):
    """
    Calculate centrality metrics over g
    :param g:
    :return:
    """
    degree = nx.degree_centrality(g)
    closeness = nx.closeness_centrality(g)
    betweenness = nx.betweenness_centrality(g)
    centrality_dict = {
        'degree': degree,
        'closeness': closeness,
        'betweenness': betweenness
    }
    return centrality_dict


def add_node_metrics_to_g(g, comm_dict, centrality_dict):
    """
    Adds communities and centrality measures to graph nodes.
    :param g:
    :param comm:
    :param centrality_dict:
    :return:
    """
    for community, comm_nodes in comm_dict.items():
        print(community)
        idComm = 1
        for c in comm_nodes:
            for node in c:
                g.nodes[node][community] = idComm
                # Esto no deberia hacerse varias veces, pero no he sido capaz de mantenerlo si no
                for metric_name, metric in centrality_dict.items():
                    g.nodes[node][metric_name] = metric[node]
            idComm += 1
    return g


def add_edge_metrics_to_g(g, edge_betwenness):
    """
    Add edge metrics to graph. For now, only betweenness is added.
    :param g:
    :param edge_betwenness:
    :return:
    """
    for edge in edge_betwenness:
        g[edge[0]][edge[1]]['eb'] = edge_betwenness[edge]
    return g


def write_graph_json(g, json_file):
    json_data = json_graph.node_link_data(g)
    # print(json_data)
    with open(json_file, 'w') as file:
        json.dump(json_data, file, indent='\t')


if __name__ == '__main__':
    base_path = 'fb-pages-food'
    json_path = 'json'
    edges_path = base_path + '/fb-pages-food_unique.edges'
    nodes_path = base_path + '/nodes_final.csv'
    community = ''
    json_file = json_path + '/food_graph_final.json'
    # Load graph
    g = load_graph(edges_path, nodes_path)

    # Calculate node metrics
    comm_dict = get_communities(g)
    centrality_dict = get_centrality_metrics(g)
    # print(comm_dict)
    # print(centrality_dict)

    g = add_node_metrics_to_g(g, comm_dict, centrality_dict)

    # Calculate edge metrics
    edge_betwenness = nx.edge_betweenness(g)
    g = add_edge_metrics_to_g(g, edge_betwenness)

    # Create json
    write_graph_json(g, json_file)
