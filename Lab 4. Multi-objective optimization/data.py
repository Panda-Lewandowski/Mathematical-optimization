import pandas as pd

alter_matrix = pd.DataFrame([
    #1  2  3  4
    [3, 3, 5, 7], # A
    [1, 2, 2, 3], # B
    [5, 6, 6, 6], # C
    [6, 7, 8, 4]  # D  
], index=["A", "B", "C", "D"], columns=[1, 2, 3, 4])

weight_vector = [6, 2, 5, 8]

vars = {
    
1: pd.DataFrame([
    #A  B  C  D
    [1, 1/5, 3, 7], # A
    [5, 1, 7, 9], # B
    [1/3, 1/7, 1, 3], # C
    [1/7, 1/9, 1/3, 1]  # D  
], index=["A", "B", "C", "D"], columns=["A", "B", "C", "D"]), 

2: pd.DataFrame([
    #A  B  C  D
    [1, 1/3, 5, 7], # A
    [3, 1, 6, 8], # B
    [1/5, 1/6, 1, 1], # C
    [1/7, 1/8, 1, 1]  # D  
], index=["A", "B", "C", "D"], columns=["A", "B", "C", "D"]), 


3: pd.DataFrame([
    #A  B  C  D
    [1, 5, 1/3, 1/7], # A
    [1/5, 1, 1/7, 1/9], # B
    [3, 7, 1, 1], # C
    [7, 9, 1, 1]  # D  
], index=["A", "B", "C", "D"], columns=["A", "B", "C", "D"]),


4: pd.DataFrame([
    #A  B  C  D
    [1, 3, 7, 7], # A
    [1/3, 1, 1/5, 1/5], # B
    [1/7, 5, 1, 5], # C
    [1/7, 5, 1/5, 1]  # D  
], index=["A", "B", "C", "D"], columns=["A", "B", "C", "D"])

}

criteria = pd.DataFrame([
    #1  2  3  4
    [1, 5, 1/3, 1/5], # 1
    [1/5, 1, 1/5, 1], # 2
    [3, 5, 1, 1/5], # 3
    [5, 1, 5, 1]  # 4  
], index=[1, 2, 3, 4], columns=[1, 2, 3, 4])

