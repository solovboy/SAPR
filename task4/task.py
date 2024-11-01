import pandas as pd
import numpy as np


def entropy(probabilities):
    return -np.sum(probabilities * np.log2(probabilities), where=(probabilities > 0))


def conditional_entropy(joint_probabilities, conditional_probabilities):
    valid_probs = (joint_probabilities > 0) & (conditional_probabilities > 0)
    return -np.sum(joint_probabilities[valid_probs] * np.log2(conditional_probabilities[valid_probs]))

def mutual_information(H_A, H_B, H_AB):
    return H_A + H_B - H_AB


def task(data):
    
    total_count = data.values.sum()
    joint_probabilities = data / total_count  
    marginal_prob_A = joint_probabilities.sum(axis=1)  
    marginal_prob_B = joint_probabilities.sum(axis=0) 
    
    H_AB = entropy(joint_probabilities.values.flatten())
    H_A = entropy(marginal_prob_A.values)
    H_B = entropy(marginal_prob_B.values)
    
    conditional_probabilities = joint_probabilities.div(marginal_prob_A, axis=0)
    Ha_B = conditional_entropy(joint_probabilities.values.flatten(), conditional_probabilities.values.flatten())
    
    I_AB = mutual_information(H_A, H_B, H_AB)
    
    return [float(round(H_AB, 2)), float(round(H_A, 2)), float(round(H_B, 2)), float(round(Ha_B, 2)), float(round(I_AB, 2))]


if __name__ == "__main__":
    data = pd.read_csv('./task4/data.csv', index_col=0)
    result = task(data)
    print(result)
