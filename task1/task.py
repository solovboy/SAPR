import json
import numpy


def main(path):
    with open(path, "r") as file:
        data = json.load(file)
    nodes = data["nodes"]
    print("Graph in json string format:\n", nodes, "\n")
    matrix = numpy.zeros((len(nodes), len(nodes)), int)
    for source in nodes:
        for target in nodes[source]:
            matrix[int(source)-1, int(target)-1] = 1
            matrix[int(target)-1, int(source)-1] = 1

    print("Adjacency matrix:\n", matrix)
    

if __name__ == "__main__":
    path = "./task1/graph.json"
    main(path)