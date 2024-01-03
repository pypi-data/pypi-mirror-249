__version__ = '0.0.1'
import os, sys, platform
from typing import Union, Callable, Tuple, List

if platform.system() == "Windows":
    mypath = os.path.dirname(os.path.realpath(__file__))
    if mypath not in sys.path:
        sys.path.insert(0, mypath)
    os.add_dll_directory(mypath)

from .cpppart import cpppart as base
import networkx as nx

VF3_CALLS = {
    # (use_node_attrs, use_edge_attrs) => Appropriate function of the base pybind11 module
    (False, False) : base.calc_noattrs,
    (True, False) : base.calc_nodeattr,
    (False, True) : base.calc_edgeattr,
    (True, True) : base.calc_bothattrs,
}


def _ensure_graph_correctness(graph: Union[nx.Graph, nx.DiGraph]) -> None:
    assert not isinstance(graph, nx.MultiGraph) and not isinstance(graph, nx.MultiDiGraph), \
        "Cannot accept Multigraph type for isomorphism calculations"
    
    assert isinstance(graph, nx.Graph) or isinstance(graph, nx.DiGraph), \
        f"Cannot accept graph of type '{type(graph)}' (nx.Graph or nx.DiGraph is expected)"

    assert graph.number_of_edges() > 0, \
        "Graph must contain non-zero number of edges"
    
    assert graph.number_of_nodes() > 0, \
        "Graph must contain non-zero number of nodes"
    

def _process_graph(graph: Union[nx.Graph, nx.DiGraph]) -> Tuple[dict, dict, bool]:
    assert isinstance(graph, nx.Graph) or isinstance(graph, nx.DiGraph), \
        f"Provided '{repr(graph)}' is not a NetworkX graph"
    
    directed = isinstance(graph, nx.DiGraph)

    int_relabel = [
        node
        for node in graph.nodes
    ]

    relabeling = {
        'to_int': {
            node: i
            for i, node in enumerate(int_relabel)
        },
        'from_int': int_relabel
    }

    return {
        'nodes': [i for i in range(graph.number_of_nodes())],
        'edges': [
            [relabeling['to_int'][vA], relabeling['to_int'][vB]]
            for vA, vB in graph.edges
        ],

        # Attr lists will be filled later
        'node_attrs': [],
        'edge_attrs': [],
    }, relabeling, directed


def _group_attrs(itemviewA, itemviewB, match_function, item_type) -> Tuple[dict]:
    assert match_function is not None
    
    dep_graph = nx.Graph()
    a_nodes = []
    i = 0
    for item_name in itemviewA:
        dep_graph.add_node(i, base='A', name=item_name)
        a_nodes.append(i)
        i += 1

    b_nodes = []
    for item_name in itemviewB:
        dep_graph.add_node(i, base='B', name=item_name)
        b_nodes.append(i)
        i += 1
    
    for a_node in a_nodes:
        for b_node in b_nodes:
            if match_function(itemviewA[dep_graph.nodes[a_node]['name']], itemviewB[dep_graph.nodes[b_node]['name']]):
                dep_graph.add_edge(a_node, b_node)
    
    a_attrs = {}
    b_attrs = {}
    a_failed = False
    b_failed = False
    for attr_index, component in enumerate(nx.connected_components(dep_graph)):
        comp_subgraph = dep_graph.subgraph(component)
        a_number = sum(
            1
            for node, keys in comp_subgraph.nodes(data=True)
            if keys['base'] == 'A'
        )
        b_number = sum(
            1
            for node, keys in comp_subgraph.nodes(data=True)
            if keys['base'] == 'B'
        )
        if a_number == 0:
            a_failed = True
        if b_number == 0:
            b_failed = True
            
        num_edges = comp_subgraph.number_of_edges()
        assert num_edges == a_number * b_number, \
            f"Unable to create valid {item_type} attributes for {repr(match_function)}"
        for node, keys in comp_subgraph.nodes(data=True):
            if keys['base'] == 'A':
                a_attrs[keys['name']] = attr_index
            else:
                b_attrs[keys['name']] = attr_index
    
    if a_failed:
        a_attrs = None
    if b_failed:
        b_attrs = None
    return a_attrs, b_attrs


def get_log_function(verbose: bool) -> Callable[[str], None]:
    if verbose:
        return lambda message: print(f"[VF3Py] {message}")
    else:
        return lambda message: None


def _main_caller(
        graph:    Union[nx.Graph, nx.DiGraph],
        subgraph: Union[nx.Graph, nx.DiGraph],
        node_match: Callable[[dict, dict], bool] = None,
        edge_match: Callable[[dict, dict], bool] = None,
        all_solutions=True,
        return_integers=False,
        verbose=False
    ) -> List[Tuple]:

    log = get_log_function(verbose)

    _ensure_graph_correctness(graph)
    _ensure_graph_correctness(subgraph)
    log("Graph correctness checks were passed")

    target_dict, target_labels, target_directed = _process_graph(graph)
    pattern_dict, pattern_labels, pattern_directed = _process_graph(subgraph)
    assert not (target_directed ^ pattern_directed), \
        f"Both graphs must be either directed or undirected"
    directed = target_directed
    log("Graphs were loaded successfully")

    if node_match is not None:
        log("Generating node attributes")
        graph_node_attrs, subgraph_node_attrs = _group_attrs(graph.nodes, subgraph.nodes, node_match, 'node')
        if graph_node_attrs is None or subgraph_node_attrs is None:
            return []
        use_node_attrs = (len(set(graph_node_attrs.values())) > 1) and (len(set(subgraph_node_attrs.values())) > 1)
        if use_node_attrs:
            target_dict['node_attrs'] = [
                graph_node_attrs[original_label]
                for original_label in target_labels['from_int']
            ]
            pattern_dict['node_attrs'] = [
                subgraph_node_attrs[original_label]
                for original_label in pattern_labels['from_int']
            ]
            log("Node attributes were generated successfully")
        else:
            log("Use of node attributes is redundant")
    else:
        log("Skipping node attributes generation")
        use_node_attrs = False
    
    if edge_match is not None:
        log("Generating edge attributes")
        graph_edge_attrs, subgraph_edge_attrs = _group_attrs(graph.edges, subgraph.edges, edge_match, 'edge')
        if graph_edge_attrs is None or subgraph_edge_attrs is None:
            return []
        use_edge_attrs = (len(set(graph_edge_attrs.values())) > 1) and (len(set(subgraph_edge_attrs.values())) > 1)
        log(f"graph_edge_attrs = {repr(graph_edge_attrs)}")
        log(f"subgraph_edge_attrs = {repr(subgraph_edge_attrs)}")
        if use_edge_attrs:
            target_dict['edge_attrs'] = [
                graph_edge_attrs[target_labels['from_int'][vA], target_labels['from_int'][vB]]
                for vA, vB in target_dict['edges']
            ]
            pattern_dict['edge_attrs'] = [
                subgraph_edge_attrs[pattern_labels['from_int'][vA], pattern_labels['from_int'][vB]]
                for vA, vB in pattern_dict['edges']
            ]
            log("Edge attributes were generated successfully")
        else:
            log("Use of edge attributes is redundant")
    else:
        log("Skipping edge attributes generation")
        use_edge_attrs = False

    log("Loading finished. Entering C++ part...")
    result = VF3_CALLS[use_node_attrs, use_edge_attrs](
        target=target_dict, pattern=pattern_dict,
        directed=directed, all_solutions=all_solutions, verbose=verbose
    )
    log(f"Returned to Python. Found {len(result)} solutions")
    if not return_integers:
        result = [
            [
                (target_labels['from_int'][source], pattern_labels['from_int'][target])
                for source, target in match_data
            ]
            for match_data in result
        ]
        log("Successfully translated solutions to the original node labels")
    return result


def _strict_isomorphisms(graphA, graphB, **kwargs) -> List[Tuple]:
    if (graphA.number_of_nodes() != graphB.number_of_nodes()):
        return []
    
    return _main_caller(graphA, graphB, **kwargs)


# FRONT-END FUNCTIONS
# Exact matches

def are_isomorphic(main_graph, ref_graph, **kwargs) -> bool:
    return len(_strict_isomorphisms(main_graph, ref_graph, all_solutions=False, **kwargs)) > 0


def get_exact_isomorphisms(main_graph, ref_graph, **kwargs) -> List[Tuple]:
    return _strict_isomorphisms(main_graph, ref_graph, all_solutions=True, **kwargs)


def get_automorphisms(graph, **kwargs) -> List[Tuple]:
    return _strict_isomorphisms(graph, graph, all_solutions=True, **kwargs)


# FRONT-END FUNCTIONS
# Subgraph matches

def has_subgraph(graph, subgraph, **kwargs) -> bool:
    return len(_main_caller(graph, subgraph, all_solutions=False, **kwargs)) > 0


def get_subgraph_isomorphisms(graph, subgraph, **kwargs) -> List[Tuple]:
    return _main_caller(graph, subgraph, all_solutions=True, **kwargs)
