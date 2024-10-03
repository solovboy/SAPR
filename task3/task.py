import pandas
import numpy
import math


def getRelations(graph):
    matrix = numpy.zeros((graph['target'].max(), 5), int)

    for node in range(1, graph['target'].max() + 1):
        r1 = graph[graph['source'] == node]['target'].count()
        r2 = graph[graph['target'] == node]['source'].count()
        r3 = graph[graph['source'].isin(graph[graph['source'] == node]['target'])]['target'].count()
        r4 = graph[graph['target'].isin(graph[graph['target'] == node]['source'])]['source'].count()
        r5 = graph[graph['source'].isin(graph[graph['target'] == node]['source'])]['target'].count()
        
        if r5 != 0:
            r5 -= 1

        matrix[node - 1] = [r1, r2, r3, r4, r5]

    print("Relationship matrix:")
    for i in range(len(matrix)):
        print(f"Node {i+1}", matrix[i])

    return matrix


def main(graph):
    relationsMatrix = getRelations(graph)
    entropy = 0

    for i in range(graph['target'].max()):
        for j in range(5):
            if relationsMatrix[i][j] != 0:
                entropy += (relationsMatrix[i][j] / (graph['target'].max() - 1)) * math.log(relationsMatrix[i][j] / (graph['target'].max() - 1), 2)
                
    return -entropy


if __name__ == "__main__":
    graph = pandas.read_csv('./task3/graph.csv', sep=',')
    graph.columns = ['source', 'target']
    result = main(graph)
    print("Entropy =", result)
    