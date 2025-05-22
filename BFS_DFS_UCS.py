from collections import deque
from prettytable import PrettyTable

#map_structure:graph.py
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
#utils.py
def getNode(name, l): #回傳在列表l內對應name的NODE物件
   return next(( i for i in l if i.name == name), -1)
#graph infromation
romania = Graph( ['Or', 'Ne', 'Ze', 'Ia', 'Ar', 'Si', 'Fa',
 'Va', 'Ri', 'Ti', 'Lu', 'Pi', 'Ur', 'Hi',
 'Me', 'Bu', 'Dr', 'Ef', 'Cr', 'Gi'],
[
   ('Or', 'Ze', 71), ('Or', 'Si', 151),
   ('Ne', 'Ia', 87), ('Ze', 'Ar', 75),
   ('Ia', 'Va', 92), ('Ar', 'Si', 140),
   ('Ar', 'Ti', 118), ('Si', 'Fa', 99),
   ('Si', 'Ri', 80), ('Fa', 'Bu', 211),
   ('Va', 'Ur', 142), ('Ri', 'Pi', 97),
   ('Ri', 'Cr', 146), ('Ti', 'Lu', 111),
   ('Lu', 'Me', 70), ('Me', 'Dr', 75),
   ('Dr', 'Cr', 120), ('Cr', 'Pi', 138),
   ('Pi', 'Bu', 101), ('Bu', 'Gi', 90),
   ('Bu', 'Ur', 85), ('Ur', 'Hi', 98),
   ('Hi', 'Ef', 86)
] )

#implement FIFO, LIFO and PRIO queue.
class Queue:
    def __init__(self):
        self.list = []
    def is_empty(self):
        return len(self.list) == 0
    def show_list_name(self):
        print("list:", [node.name for node in self.list])
    def show_list_cost(self):
        print("cost:", [node.cost for node in self.list])
class FIFO(Queue):
    def put_in(self,item):
        self.list.append(item)

    def take_out(self):
        if not self.is_empty():
            return self.list.pop(0)
        return None
class LIFO(Queue):
    def put_in(self,item):
        self.list.append(item)
    def take_out(self):
        if not self.is_empty():
            return self.list.pop()
        return None
class PRIO(Queue):
    def put_in(self,node):
        self.list = [item for item in self.list if item != node]
        self.list.append(node)
        self.list.sort(key=lambda n: n.cost)  # 根據 cost 排序
    def take_out(self):
        if not self.is_empty():
            return self.list.pop(0)
        return None


#route planning algorithm
def B_DFS_graph_search(graph,start_name,goal_name,queue_type_class):
    #initial
    visited =[] #紀錄去過的點
    queue = queue_type_class() #紀錄之後要探訪的點，根據不同演算法而結構不同
    #set initial state
    start_node = getNode(start_name,graph.nodes)
    visited.append(start_node)
    queue.put_in(start_node)
    #node finding
    while not queue.is_empty():
        current = queue.take_out() #抓出要探訪的點，此點不會在之後要探訪的佇列中
        if current.name == goal_name:
            break
        for edge in current.edges: 
            neighbor = edge.end 
            if neighbor not in visited:
                neighbor.parent = current #為了能回朔，因此將.parent設成上個點的NODE
                visited.append(neighbor)
                queue.put_in(neighbor) 
    #find the path and the cost between start and goal
    path = []
    cost= 0
    node = getNode(goal_name, graph.nodes)
    while node is not None:
        path.insert(0, node.name)
        if node.parent is not None: #因為NODE的距離需從上層得知
            for edge in node.parent.edges:#每個節點都有很多個edge節點，需確認名字為相同
                if edge.end == node:
                    cost += edge.value
                    break
        node = node.parent #切換到上層的NODE
    return path,cost

def UCS_graph_search(graph,start_name,goal_name,queue_type_class):
    #initial
    visited =[] 
    queue = queue_type_class() 
    #set initial state
    start_node = getNode(start_name,graph.nodes)
    start_node.cost = 0 
    queue.put_in(start_node)
    #node finding
    while not queue.is_empty():
        current = queue.take_out() 
        if current in visited:
            continue
        visited.append(current)
        #print("--------------------")
        #print("current:",current.name)
        for edge in current.edges: 
            #print('edge:',edge.end.name)
            #print('edge_value:',edge.value)
            neighbor = edge.end
            new_cost = current.cost + edge.value
            if new_cost < neighbor.cost:
                neighbor.parent = current #為了能回朔，因此將.parent設成上個點的NODE
                neighbor.cost = new_cost
                queue.put_in(neighbor) 
        #queue.show_list_name()
        #queue.show_list_cost()
        #print("visited",[node.name for node in visited])
    #find the path and the cost between start and goal
    path = []
    node = getNode(goal_name, graph.nodes)
    while node is not None:
        path.insert(0, node.name)
        node = node.parent #切換到上層的NODE
    cost = getNode(goal_name, graph.nodes).cost
    return path,cost


#test different algorithm
path,cost = UCS_graph_search(romania,'Bu','Ti',PRIO)
print("UCS path:", path)
print("UCS cost:", cost)

path_1,cost_1 = B_DFS_graph_search(romania,'Bu','Ti',FIFO)
print("BFS path:", path_1)
print("BFScost:", cost_1)

path_2,cost_2 = B_DFS_graph_search(romania,'Bu','Ti',LIFO)
print("DFS path:", path_2)
print("DFS cost:", cost_2)

