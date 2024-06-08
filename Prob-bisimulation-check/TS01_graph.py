from graphviz import Digraph

def TS01_graph(S, L , W , E ): 

    G  = Digraph("TS01", filename="TS01.gy",format="png")
    G.attr('node', shape='circle')
    for i in range(len(S)):
        G.edge(S[i],E[i], label=f' {L[i]}:{W[i]}',fontsize="9")
    

    G.render()          # save the graph to file. 