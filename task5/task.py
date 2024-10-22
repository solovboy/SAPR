import numpy as np
import json


def read_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data['data']


def write_core_to_json(core_AB, output_file):
    with open(output_file, 'w') as file:
        json.dump({"core_AB": core_AB}, file, indent=4)


def build_relation_matrix(ranking, n):
    Y = np.zeros((n, n), dtype=int)
    np.fill_diagonal(Y, 1)

    for idx, cluster in enumerate(ranking):
        if isinstance(cluster, int):
            cluster = [cluster]

        for i in cluster:
            for j in cluster:
                Y[i - 1][j - 1] = 1

        for i in cluster:
            for prev_cluster in ranking[:idx]:
                if isinstance(prev_cluster, int):
                    prev_cluster = [prev_cluster]
                for j in prev_cluster:
                    Y[j - 1][i - 1] = 1

    return Y


def find_discrepancies(YA, YB):
    n = YA.shape[0]
    discrepancies = []
    for i in range(n):
        for j in range(n):
            if YA[i, j] == 1 and YB[i, j] == 0 and YA[j, i] == 0 and YB[j, i] == 1:
                discrepancies.append((i + 1, j + 1)) 
            elif YA[i, j] == 0 and YB[i, j] == 1 and YA[j, i] == 1 and YB[j, i] == 0:
                discrepancies.append((j + 1, i + 1))
    return discrepancies


def find_core_AB(discrepancies):
    core_AB = []
    added = set()

    for x, y in discrepancies:
        if any(x in group or y in group for group in core_AB):
            for group in core_AB:
                if x in group or y in group:
                    if x not in group:
                        group.append(x)
                    if y not in group:
                        group.append(y)
                    break
        else:
            core_AB.append([x, y])

        added.update([x, y])

    return core_AB


def main(file_A, file_B, output_file):
    ranking_A = read_json(file_A)
    ranking_B = read_json(file_B)

    n_A = sum(len(item) if isinstance(item, list) else 1 for item in ranking_A)
    n_B = sum(len(item) if isinstance(item, list) else 1 for item in ranking_B)
    n = max(n_A, n_B)

    YA = build_relation_matrix(ranking_A, n)
    print("The YA matrix for ranking A:")
    print(YA)

    YB = build_relation_matrix(ranking_B, n)
    print("The YB matrix for ranking B:")
    print(YB)

    discrepancies = find_discrepancies(YA, YB)
    print(f"Contradictions: {discrepancies}")

    core_AB = find_core_AB(discrepancies)
    print(f"Core AB: {core_AB}")

    write_core_to_json(core_AB, output_file)


if __name__ == "__main__":

    file_A = './task5/a.json'
    file_B = './task5/b.json'
    output_file = './task5/core_AB.json'

    main(file_A, file_B, output_file)
