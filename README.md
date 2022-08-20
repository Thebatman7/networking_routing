# networking_routing
The framework in this repository provides a graphical user interface that generates a graph/network with a specified number of points, for a
provided random seed and a display for the graph vertices and for the subsequently computed shortest paths.
When you hit “Generate” the framework for this project generates a random set of nodes, V, each with 3
randomly selected edges to other nodes. The edges are directed and the edge cost is the Euclidean distance
between the nodes. Thus, all nodes will have an out-degree of 3, but no predictable value for in-degree.
The nodes have an (x,y) location and the edges include the start/end nodes and the edge length. The nodes are
drawn on the display in the provided framework. You can hit “Generate” again to build a new graph (Each
random seed leads to a different random graph).
Code implements Dyskstra’s algorithm which is used for finding the shortest paths or minimum cost between nodes in a graph, 
which may represent, for example, road networks. Code finds shortest paths through a graph representing a network routing problem.
