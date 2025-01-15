from sage.all import Graph

def searchOfLonelyEdgesByColor(G, color):
    """
    Method that vertifies a colored graph by calling a DFS method for each vertex of the graph.
    It also returns some candidates to be colored next.
    
    PARAMETERS:
        G: Graph which has some edges colored
    
    RETURNS:
        True, None if all the cycles are correctly colored.
        False, uncoloredEdges if we have found a cycle that has a lonely edge of color "color" and gives the
          uncolored edges that should be colored next.
    """
    visited = set()
    for v in G.vertices():
        if v not in visited:
            visited.add(v)
            check, uncoloredEdges = searchOfLonelyEdgesByColorDFS(G, v, v, color, visited, set(), 0, set())
            if not check:
                return False, uncoloredEdges

    return True, None


def searchOfLonelyEdgesByColorDFS(G, currentNode, finalNode, color, visited, path, numEdgesColor, uncoloredEdges):
    """
    DFS method that goes through all the cycles that contain the vertex finalNode in the search of a lonely colored edge of color "color".
    
    PARAMETERS:
        G:              Partially colored Graph
        currentNode:    Vertex that we are visiting at the moment
        finalNode:      Vertex where the cycle ends (and begins)
        color:          Color of which we are searching a lonely color edge in a cycle
        visited:        set of vertices whose cycles have already been checked
        path:           set that contains the vertices that uses the path
        numColor:       number of vertices of color "color" that are in the path
        uncoloredEdges: set of edges that are uncolored in the current cycle
    
    RETURNS:
        True, uncoloredEdges if all the cycles are correctly colored.
        False, uncoloredEdges if we have found a cycle that has a lonely edge of color "color" and gives the uncolored edges of the cycle.
    """
    if currentNode not in path:
        path.add(currentNode)
        
        for nei in G.neighbors(currentNode):
            label = G.edge_label(currentNode, nei)
            aux_numEdgesColor = numEdgesColor
            
            if nei not in visited and nei not in path:  # To not use vertices that are already fully checked
                if label == color: aux_numEdgesColor += 1
                
                if aux_numEdgesColor > 1:
                    # If we find two edges of color "color" in a cycle, it won't be a lonely color cycle
                    continue
                
                else:
                    if label == 0:
                        uncoloredEdges.add((currentNode, nei, label))
                    
                    check, uncoloredEdges = searchOfLonelyEdgesByColorDFS(G, nei, finalNode, color, visited, path, aux_numEdgesColor, uncoloredEdges)
                    if not check:
                        return False, uncoloredEdges

            elif nei == finalNode and len(path) > 2:
                if label == color: aux_numEdgesColor += 1
                
                if aux_numEdgesColor == 1:
                    if label == 0:
                        uncoloredEdges.add((currentNode, nei, label))
                    
                    # We have found a cycle with a lonely color
                    return False, uncoloredEdges
            
            # We delete the edge because if we have arrived here means that the cycle was correct
            uncoloredEdges.discard((currentNode, nei, label))

        path.remove(currentNode)

    return True, uncoloredEdges


def searchMonochromaticCyclesInEdge(G_coloredEdges, edge, color):
    """
    Function that calls a DFS method to go through all the cycles that contain "edge".
    
    PARAMETERS:
        G_coloredEdges: Graph that contains only the colored edges.
        edge:           Edge that has to be contained in the cycles.
        color:          Color of the monochromatic cycles.
    
    RETURNS:
        The length of the cycle found. If it has not found a cycle it returns 0.
    """
    v0, v1 = edge[0], edge[1]
    path = set([v0])
    
    # Calling the DFS like this, we force the cycles to contain both vertices
    return searchMonochromaticCyclesInEdgeDFS(G_coloredEdges, v1, v0, color, path)


def searchMonochromaticCyclesInEdgeDFS(G_coloredEdges, currentNode, v0, color, path):
    """
    DFS method that goes through all the cycles that contain the vertex finalNode in the search of a monochromatic cycle of color "color".
    
    PARAMETERS:
        G_coloredEdges: Colored Graph
        currentNode:    Vertex that we are visiting at the moment
        v0:             Vertex where the cycle ends (and begins)
        color:          Color of which we are searching a monochromatic cycle
        path:           set that contains the vertices that uses the path
    
    RETURNS:
        The length of the cycle found. If it has not found a cycle it returns 0.
    """
    if currentNode not in path:
        path.add(currentNode)
        
        for nei in G_coloredEdges.neighbors(currentNode):
            label = G_coloredEdges.edge_label(currentNode, nei)
            
            # If the edge has a different color, we do not consider the neighbor
            if label != color: continue
            
            if nei not in path:
                lenCycle = searchMonochromaticCyclesInEdgeDFS(G_coloredEdges, nei, v0, color, path)

                if lenCycle > 0:
                    # We do not search for more cycles, because each time that we color an edge, it can only appear one monochromatic cycle
                    return lenCycle
            
            elif nei == v0 and len(path) > 2:  # Cycle closed, we have found a monochromatic cycle
                return len(path)
    
        path.remove(currentNode)
        
    return 0


def searchMonochromaticCyclesByColor(G, color):
    """
    Function that calls a DFS method that searches monochromatic cycles of color "color" and tells if there are such cycles of different lengths.
    
    PARAMETERS:
        G:     Colored Graph
        color: Color of the monochromatic cycles.
    
    RETURNS:
        True if there is not monochromatic cycles of different lengths.
        False if we find two monochromatic cycles of different lengths.
    """
    visited = set()
    lenMonochromaticCycle = 0
    for v in G.vertices():
        if v not in visited:
            visited.add(v)
            check, lenMonochromaticCycle = searchMonochromaticCyclesByColorDFS(G, v, v, color, visited, set(), lenMonochromaticCycle)
            if not check:
                return False
        
    return True


def searchMonochromaticCyclesByColorDFS(G, currentNode, v0, color, visited, path, lenMonochromaticCycle):
    """
    DFS method that goes through all the cycles searching for monochromatic cycles. It tells if there are such cycles of different lengths.
    
    PARAMETERS:
        G: Colored Graph
        currentNode:           Vertex that we are visiting at the moment
        v0:                    Vertex where the cycle ends (and begins)
        color:                 Color of which we are searching a monochromatic cycle
        path:                  set that contains the vertices that uses the path
        lenMonochromaticCycle: Length of a monochromatic cycle found. If we have not found such cycle, the value is zero.
    
    RETURNS:
        True, lenMonochromaticCycle: if there is not monochromatic cycles of different lengths.
        False, lenMonochromaticCycle: if we find two monochromatic cycles of different lengths.
    """
    if currentNode not in path:
        path.add(currentNode)
        
        for nei in G.neighbors(currentNode):
            label = G.edge_label(currentNode, nei)

            # If the edge has a different color, we do not consider the neighbor
            if label != color: continue
            
            if nei not in visited and nei not in path:  # So that we do not use vertices that are already fully checked
                check, lenMonochromaticCycle = searchMonochromaticCyclesByColorDFS(G, nei, v0, color, visited, path, lenMonochromaticCycle)
                if not check:
                    return False, lenMonochromaticCycle
            
            elif nei == v0 and len(path) > 2: # Cycle closed, we have found a monochromatic cycle
                if lenMonochromaticCycle != 0 and lenMonochromaticCycle != len(path):
                    # If we had found a monochromatic cycle before and the lengths are different
                    return False, lenMonochromaticCycle
                else:
                    # We save the length of the cycle found
                    lenMonochromaticCycle = len(path)

        path.remove(currentNode)
            
    return True, lenMonochromaticCycle


def isDegreeColorGood(G_coloredEdges, edge, color):
    """
    Function that checks if we are coloring an edge that is adjacent with two other edges of the same color.
    
    PARAMETERS:
        G_coloredEdges: Colored Graph that has "edge" colored with "color"
        edge:           Edge that has been colored.
        color:          Color used.
        
    RETURNS:
        True if both endpoints have at least one adjacent edge with label different to "color".
    """
    for vertex in [edge[0], edge[1]]:
        colorDegree = 0
        for nei in G_coloredEdges.neighbors(vertex):
            if G_coloredEdges.edge_label(vertex, nei) == color:
                colorDegree += 1

        if colorDegree > 2:
            return False

    return True


def areEndpointsInDifferentComponents(G_coloredEdges, componentsList, color):
    """
    Function that verifies if all edges of a certain color are in different components.
    
    PARAMETERS:
        G_coloredEdges: Graph that contains only the colored edges (since we are only interested in the ones
                          that are colored with "color")
        componentsList: List of made of list that contain the vertices of each connected component of the graph
                          where the edges colored with "color" are deleted
        color:          Label of the edges that we want to check if have both endpoints in the same connected component
    
    RETURNS:
        True if all the edges that use the color "color" have both endpoints in different components.
        False if not.
    """
    for edge in G_coloredEdges.edges():
        u, v, label = edge[0], edge[1], edge[2]

        if label == color:
            for component in componentsList:
                if u in component and v in component:
                    # If we find an edge that has both endpoints in the same component, we return False
                    return False
                elif u in component or v in component:
                    # If we find an edge that has the endpoints in different components, we go to the next edge
                    break
    
    return True


def findNextEdge(G):
    """
    Function that returns an uncolored edge in the graph G.
    """
    for edge in G.edges():
        if G.edge_label(edge[0], edge[1]) == 0:
            return edge

    return None