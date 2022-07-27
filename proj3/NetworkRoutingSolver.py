#!/usr/bin/python3


from abc import abstractclassmethod, abstractmethod
from re import S
from xml.dom.minicompat import NodeList
from CS312Graph import *
import time


class NetworkRoutingSolver:
    def __init__( self):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath( self, destIndex ):
        path_edges = [] 
        total_length = 0
        node = self.prev[destIndex] # we get the previous of the node we want
        index = destIndex # we save node we want to reach 
        total_length = self.dist[destIndex] # total dist is here
        if (node == None):
            return {'cost':float("inf"), 'path':[]}

        while(node != None):
            pathEdge = None
            for v in node.neighbors:
                if(v.dest.node_id == index): # we iterate through the neighbors to find the node we should go through
                    pathEdge = v # we get the edge from previous to the next node in the path to the destination
                    break
            path_edges.append((pathEdge.src.loc, pathEdge.dest.loc, '{:.0f}'.format(pathEdge.length))) # we add the edge to the array of edges
            index = node.node_id # the new distination towards our final distination is the previous node and we repeat the process by
            node = self.prev[node.node_id] # finding the previous of the new distination 
        return {'cost':total_length, 'path':path_edges}

    def computeShortestPaths( self, srcIndex, use_heap=True ):
        self.source = srcIndex
        
        t1 = time.time()
        # TODO: RUN DIJKSTRA'S TO DETERMINE SHORTEST PATHS.
        #       ALSO, STORE THE RESULTS FOR THE SUBSEQUENT
        #       CALL TO getShortestPath(dest_index) ???

        nodes = self.network.getNodes()
        start_node = self.network.nodes[self.source]

        self.dist = self.make_distList(nodes, start_node) #distance array 
        self.prev = self.make_prevList(nodes) #previous array

        if (use_heap):
            print("We are using a heap for our priority queue")
            priority_queue = PriorityQueueHeap(nodes, self.dist)
        else:
            print("We are using an array for our priority queue")
            priority_queue = PriorityQueueArray(nodes, self.dist)

        self.dijkstra(priority_queue)
    
        t2 = time.time()
        return (t2-t1)

    # Dijkstra algorithm
    def dijkstra(self, priority_queue):
        priority_queue.make_queue() # H = makequeue(V)
        while(not priority_queue.isEmpty()): # Big O(n)
            
            u = priority_queue.delete_min() # Big O(n)
            for v in u.neighbors: # Big O(3) = Big O(1)   #for each nieghbor v of u still in Q:
                newDist = self.dist[u.node_id] + v.length #alt <- dist[u] + Graph.Edges(u,v) = v.lenght 
                if(newDist < self.dist[v.dest.node_id]):           #if(alt < dist[v]):
                    self.dist[v.dest.node_id] = newDist # Big O(1) #dist[v] <- alt
                    self.prev[v.dest.node_id] = u # Big O(1)       #prev[v] <- u
                    
                    priority_queue.decrease_key(v) #only needed for heap implementation
        
    
    def make_distList(self, nodes, source_node): # Big O(n)
        dist = []
        for n in nodes:
            dist.insert(n.node_id, float("inf"))

        dist[source_node.node_id] = 0
        #self.printList(dist)
        return dist

    def make_prevList(self, nodes): # Big O(n)
        prev = []
        for n in nodes:
            prev.insert(n.node_id, None)
        #self.printList(prev)
        return prev


    def printList(self, list):
            print("Printing list: ")
            for n in range(len(list)):
                print("node_id:", n, list[n])

# Parent class
class PriorityQueue():
    def __init__(self, nodes, dist):
        self.nodes = nodes
        self.dist = dist

    def make_queue(self):
        pass

    def delete_min(self):
        pass

    def decrease_key(self, v):
        pass

    def isEmpty(self):
        pass

# Child class
class PriorityQueueArray(PriorityQueue):
    def __init__(self, nodes, dist):
        super().__init__(nodes, dist)
        self.visit = [] # nodes we haven't visited yet

    def delete_min(self): # Big O(n)
        min_node = None
        min_dist = float("inf")
        for n in self.visit: 
            if (self.dist[n.node_id] <= min_dist): 
                min_dist = self.dist[n.node_id]
                min_node = n 
        self.visit.remove(min_node)

        return min_node

    def make_queue(self): # Big O(n)
        for n in self.nodes:
            self.visit.append(n)
        #self.printNonVisited()

    def isEmpty(self):
        if len(self.visit) == 0: return True # Big O(1)
        return False

    # No need to implement this method becuase it is only needed for heap implementation
    #def decrease_key(self, v): pass

    def printNonVisited(self):
        print("Nodes not visited and length of list", len(self.visit))
        for n in range(len(self.visit)):
            print(self.visit[n])


# Child class
class PriorityQueueHeap(PriorityQueue):
    def __init__(self, nodes, dist):
        super().__init__(nodes, dist)
        self.pointers = []
        self.heap = []
        self.heap_len = 0
    
    # def make_queue(self): #Big O(n)
    #     self.pointers = [-1] * len(self.nodes)
    #     self.heap.append(None)
    #     for n in self.nodes:
    #         if self.dist[n.node_id] == 0:
    #             self.heap[0] = n
    #         else:
    #             self.heap.append(n)
    #         self.heap_len += 1

    # def sift_up(self, i):
    #     # While the element is not the root or the left element
    #     while i // 2 > 0:
    #         # If the element is less than its parent swap the elements
    #         if self.heap_list[i] < self.heap_list[i // 2]:
    #             self.heap_list[i], self.heap_list[i // 2] = self.heap_list[i // 2], self.heap_list[i]
    #         # Move the index to the parent to keep the properties
    #         i = i // 2
 
    # def insert(self, k):
    #     # Append the element to the heap
    #     self.heap_list.append(k)
    #     # Increase the size of the heap.
    #     self.current_size += 1
    #     # Move the element to its position from bottom to the top
    #     self.sift_up(self.current_size)
 
    # def sift_down(self, i):
    #     # if the current node has at least one child
    #     while (i * 2) <= self.current_size:
    #         # Get the index of the min child of the current node
    #         mc = self.min_child(i)
    #         # Swap the values of the current element is greater than its min child
    #         if self.heap_list[i] > self.heap_list[mc]:
    #             self.heap_list[i], self.heap_list[mc] = self.heap_list[mc], self.heap_list[i]
    #         i = mc
 
    # def min_child(self, i):
    #     # If the current node has only one child, return the index of the unique child
    #     if (i * 2)+1 > self.current_size:
    #         return i * 2
    #     else:
    #         # Herein the current node has two children
    #         # Return the index of the min child according to their values
    #         if self.heap_list[i*2] < self.heap_list[(i*2)+1]:
    #             return i * 2
    #         else:
    #             return (i * 2) + 1
 
    # def delete_min(self):
    #     # Equal to 1 since the heap list was initialized with a value
    #     if len(self.heap_list) == 1:
    #         return 'Empty heap'
 
    #     # Get root of the heap (The min value of the heap)
    #     root = self.heap_list[1]
 
    #     # Move the last value of the heap to the root
    #     self.heap_list[1] = self.heap_list[self.current_size]
 
    #     # Pop the last value since a copy was set on the root
    #     *self.heap_list, _ = self.heap_list
 
    #     # Decrease the size of the heap
    #     self.current_size -= 1
 
    #     # Move down the root (value at index 1) to keep the heap property
    #     self.sift_down(1)
 
    #     # Return the min value of the heap
    #     return root


    


    # def printArray(self, array):
    #     print("Size of array: ", len(array))
    #     for n in range(len(array)):
    #         print(array[n])





# Implement Dijkstra’s algorithm to find shortest paths in a graph.
#
# Implement two versions of a priority queue class, one using an unsorted array (a python list) as the
# data structure and one using a heap:
#
#   For the array implementation, insert and decrease-key are simple O(1) operations, but deletemin will unavoidably be O(|V|).
#
#   For the heap implementation, all three operations (insert, delete-min, and decrease-key) must be 
#   worst case O(log|V|). For your binary heap implementation, you may implement the binary heap 
#   with an array, but remember that decrease-key will be O(|V|) unless you have a separate array (or 
#   map) of object references into your binary heap, so that you can have fast access to an arbitrary
#   node. Thus, you must use the separate lookup map. Also, don't forget that you will need to adjust
#   this lookup array/map of references every time you swap elements in the heap.
