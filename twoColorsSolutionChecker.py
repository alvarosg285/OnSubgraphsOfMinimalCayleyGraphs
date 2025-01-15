from collections import defaultdict
from sage.all import Graph

def isDegreeColorGood(G):
    """
    Function that checks if there is a vertex in G is adjacent to three edges of the same color.
    
    PARAMETERS:
        G: Colored Graph
        
    RETURNS:
        True if the color degree of all vertices is correct.
        False if not.
    """
    for vertex in G.vertices():
        colorDegree = defaultdict(int)
        
        color = 0
        for nei in G.neighbors(vertex):
            color = G.edge_label(vertex, nei)
            colorDegree[color] += 1
        
        if colorDegree[color] == 3:
            return False

    return True


def areOneColorGraphsDisconnected(G1, G2):
    """
    Function that verifies if the subgraphs containing all edges of the same color are disconnected.

    PARAMETERS:
        G1: Graph colored with the color 1
        G2: Graph colored with the color 2

    RETURNS:
        True if both graphs are disconnected.
        False if not.
    """
    return (not G1.is_connected()) and (not G2.is_connected())


def areEndpointsInDifferentComponents(G, G1, G2, color1, color2):
    """
    Function that verifies if all edges of the graph are in the different components.
    
    PARAMETERS:
        G: Graph colored with 2 colors.
        G1: Graph colored with color 1.
        G2: Graph colored with the color 2
        color1: color 1
        color2: color 2
    
    RETURNS:
        True if all the edges have both endpoints in different components.
        False if not.
    """
    componentsList1 = G1.connected_components()
    componentsList2 = G2.connected_components()
    
    for u, v, label in G.edges():
        if label == color1:
            for component in componentsList2:
                if u in component and v in component:
                    #print(f"The edge joining {u} and {v} is in the same component.")
                    return False
                elif u in component or v in component:
                    break
        
        elif label == color2:
            for component in componentsList1:
                if u in component and v in component:
                    #print(f"The edge joining {u} and {v} is in the same component.")
                    return False
                elif u in component or v in component:
                    break
        
        else: print("ERROR!")
    
    return True


def oneColorGraphs(G, color1, color2):   # We will only create two graphs because the solution we need to check only has 2 colors
    """
    Function that separates the graph G into two monochromatic subgraphs.

    PARAMETERS:
        G:      Graph colored with 2 colors.
        color1: color 1
        color2: color 2

    RETURNS:
        G1 and G2, graphs that contains the edges colored with 1 and the edges colored with 2 respectively.
    """
    G1 = Graph()
    G2 = Graph()
    for u, v, label in G.edges():
        if label == color1: G1.add_edge((u, v, label))
        elif label == color2: G2.add_edge((u, v, label))
        else: print("ERROR!")
    
    return G1, G2


def isSolutionCorrect(G, color1, color2):
    """
    Main function that tells whether a graph colored with two colors has a no lonely coloring.

    PARAMETERS:
        G:      Colored Graph
        color1: Color 1
        color2: Color 2

    RETURNS:
        True if the coloring satisfies the no lonely coloring conditions.
        False if not.
    """
    if isDegreeColorGood(G):
        G1, G2 = oneColorGraphs(G, color1, color2)
        if areOneColorGraphsDisconnected(G1, G2):
            return areEndpointsInDifferentComponents(G, G1, G2, color1, color2)
        
        return False
    
    return False