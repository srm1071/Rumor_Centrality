import random
import math

visited = []
queue = [] 
def rumor_centrality_up(up_messages, who_infected, calling_node, called_node):
    if called_node == calling_node:
        for i in who_infected[called_node]:
                up_messages = rumor_centrality_up(up_messages, who_infected, called_node, i)
    elif len(who_infected[called_node]) == 1:   # leaf node
        up_messages[calling_node] += 1 # check
    else:
        for i in who_infected[called_node]:
            if i != calling_node:
                up_messages = rumor_centrality_up(up_messages, who_infected, called_node, i)
        up_messages[calling_node] += up_messages[called_node]
    return up_messages        

def rumor_centrality_down(down_messages, up_messages, who_infected, calling_node, called_node):
    downm=1
    down=1
    if called_node == calling_node:
        for i in who_infected[called_node]:
            down_messages = rumor_centrality_down(down_messages, up_messages, who_infected, called_node, i) 
            downm=downm*up_messages[i]
        down=math.factorial(len(who_infected)-1)/downm
    else:
        down_messages[called_node] = down_messages[calling_node]*(float(up_messages[called_node])/(len(who_infected)-up_messages[called_node]))
        for i in who_infected[called_node]:
            if i != calling_node:
                down_messages = rumor_centrality_down(down_messages, up_messages, who_infected, called_node, i)
    for i in range(len(down_messages)):
        down_messages[i]=down_messages[i]*down
    return down_messages


def rumor_centrality(who_infected):
    # computes the estimate of the source based on rumor centrality
    initial_node = 0       # can use arbitrary initial index
    up_messages = [1]*len(who_infected) 
    down_messages = [1]*len(who_infected)
    up_messages = rumor_centrality_up(up_messages,who_infected,initial_node,initial_node)
    down_messages = rumor_centrality_down(down_messages,up_messages,who_infected,initial_node,initial_node)
    max_down = max(down_messages)
    max_down_ind = [i for i, j in enumerate(down_messages) if j == max_down]
    return down_messages,max_down_ind[random.randrange(0,len(max_down_ind),1)] 

def find_degree(who_infected):
    degree=[0]*len(who_infected)
    for i in range(len(who_infected)):
        degree[i]=len(who_infected[i])
    return degree

def bfs(visited, graph, node):
  msg=[]
  visited.append(node)
  queue.append(node)

  while queue:
    s = queue.pop(0) 
    #print (s, end = " ")
    msg.append(s)

    for neighbour in graph[s]:
      if neighbour not in visited:
        visited.append(neighbour)
        queue.append(neighbour)
  return msg
        
def ml_irregular_trees(estimation, degrees, who_infected):
    k=[]
    for i in range(len(who_infected)):
        est=1
        estt=[]
        visited=[]
        msg=bfs(visited,who_infected,i)
        deg=degrees[msg[0]]
        if (deg<2):
          estt.append(2)
        else:
          estt.append(deg)
        if(deg>1):
            for j in range(1,len(msg)-1):
                if(degrees[msg[j]]>1):
                    deg=deg+(degrees[msg[j]]-2)
                    estt.append(deg)
                else:
                  estt.append(deg)
        else:
            deg=2
            for j in range(1,len(msg)-1):
                if(degrees[msg[j]]>1):
                    deg=deg+(degrees[msg[j]]-2)
                    estt.append(deg)
                else:
                  estt.append(deg)
        for i in range(len(estt)):
          est=(estt[i]*est)
        est=1/est
        k.append(est)     
    #print(k)
    return k
def ml_estimate_irregular_trees(virtual_source, degrees, who_infected):        
    p = 1.0
    messages = [p]*len(who_infected)
    messages = ml_irregular_trees(messages, degrees, who_infected)
    return messages

def max_ml_estimate(mlestimate,downmsg):
    arr=[1.0]*len(mlestimate)
    for i in range(len(mlestimate)):
        arr[i]=mlestimate[i]*downmsg[i]
    max_message = max(arr)
    max_message_ind = [i for i, j in enumerate(arr) if j == max_message]
    return max_message_ind[random.randrange(0,len(max_message_ind),1)]

        
# creating a toy graph (tree)
adjacency = [ [] for i in range(9)]
adjacency[0] = [1, 2]
adjacency[1] = [0, 3, 4]
adjacency[2] = [0, 5, 6]
adjacency[3] = [1, 7, 8]
adjacency[4] = [1]
adjacency[5] = [2]
adjacency[6] = [2]
adjacency[7] = [3]
adjacency[8] = [3]


root_node = 0
msg,messages1 = rumor_centrality(adjacency)
degrees=find_degree(adjacency)
messages2=ml_estimate_irregular_trees(0,degrees,adjacency)
max_cal=max_ml_estimate(messages2,msg)

print(msg)
print(messages2)
#print(arr)
print ('Rumor Center is:' ,max_cal)
