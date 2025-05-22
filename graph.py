from prettytable import PrettyTable
from utils import * 

class Node:

   def __init__(self, name):
       self.parent = None
       self.name = name
       self.edges = []
       self.value = 0
       self.cost = float('inf')
     

class Edge:

   def __init__(self, edge):
      self.start = edge[0]
      self.end = edge[1]
      self.value = edge[2]


class Graph:

   def __init__(self, node_list, edges):
      self.nodes = []
      for name in node_list:
         self.nodes.append(Node(name))

      for e in edges:
        e = (getNode(e[0],self.nodes), getNode(e[1], self.nodes), e[2])        

        self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[0].name), -1)].edges.append(Edge(e))
        self.nodes[next((i for i,v in enumerate(self.nodes) if v.name == e[1].name), -1)].edges.append(Edge((e[1], e[0], e[2])))
      #print(self.nodes[0].__dict__)
      #資料結構:
         #[node(A),node(B),node(C),...] 為node的物件
         #而node下方又有其他屬性，其中.edges代表邊緣的點，並使用Edge屬性[start,end, cost]
   def print(self):
      node_list = self.nodes
      
      t = PrettyTable(['  '] +[i.name for i in node_list])
      for node in node_list:
         edge_values = ['X'] * len(node_list)
         for edge in node.edges:
            edge_values[ next((i for i,e in enumerate(node_list) if e.name == edge.end.name) , -1)] = edge.value           
         t.add_row([node.name] + edge_values)
      print(t)
            
         

                   
            