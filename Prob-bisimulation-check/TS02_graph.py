from graphviz import Digraph

def TS02_graph(S, L , W , E ): 

    G  = Digraph("TS02", filename="TS02.gy",format="png")
    G.attr('node', shape='circle')
    for i in range(len(S)):
        G.edge(S[i],E[i], label=f' {L[i]}:{W[i]}',fontsize="9")
    

    G.render()          # save the graph to file. 