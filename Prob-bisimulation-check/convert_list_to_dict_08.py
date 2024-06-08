import pandas as pd 

def list2dict(S,L,W,E):
    S = [x.upper() for x in S]  # Start Nodes Should be in Upper Case
    L = [x.lower() for x in L ]
    W = [float(x) for x in W]
    E = [x.upper() for x in E]

    unique_nodes1 = list(set(S+E))
    df = pd.DataFrame()
    df['Node'] = S
    df['output_labels']= L
    df['output_prob'] = W
    df['target'] = ''

    for i in range(len(S)):   # Add targets
        df.iloc[i,3] = E[i]
    
    return df