import json


def read_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return data


def fuzzify(value, fuzzy_set):
    """Фаззификация: вычисление степени принадлежности четкого значения нечетким множествам."""
    memberships = {}
    for term, points in fuzzy_set.items():
        membership = 0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            if x1 <= value <= x2:  # Линейная интерполяция между точками
                if x1 == x2:  # На случай вертикальной линии
                    membership = max(y1, y2)
                else:
                    membership = y1 + (y2 - y1) * (value - x1) / (x2 - x1)
                break
        memberships[term] = membership
    return memberships


def defuzzify(fuzzy_result, output_set):
    """Дефаззификация: преобразование нечеткого результата в четкое значение."""
    numerator = 0
    denominator = 0
    for term, degree in fuzzy_result.items():
        if degree > 0:  # Берем степень принадлежности > 0
            points = output_set[term]
            centroid = sum([x for x, y in points]) / len(points)  # Центр масс множества
            numerator += degree * centroid
            denominator += degree
    return numerator / denominator if denominator != 0 else 0


def main(input_file, regulator_file, transition_file, element_for_phasing):
    # Загрузка входных данных
    input_data = read_json(input_file)
    regulator = read_json(regulator_file)
    transition = read_json(transition_file)
    
    # Фаззификация входного значения
    fuzzy_input = fuzzify(element_for_phasing, input_data)
    print("Фаззифицированное значение:", fuzzy_input)
    
    # Применение правил переходов
    fuzzy_output = {}
    for input_term, degree in fuzzy_input.items():
        if input_term in transition:
            output_term = transition[input_term]
            
            if output_term in fuzzy_output:
                fuzzy_output[output_term] = max(fuzzy_output[output_term], degree)  # Комбинирование
            else:
                fuzzy_output[output_term] = degree
    print("Результат с правил переходов:", fuzzy_output)
    
    # Дефаззификация результата
    crisp_output = defuzzify(fuzzy_output, regulator)
    print("Дефаззифицированное значение:", crisp_output)
    
    return crisp_output


if __name__ == "__main__":
    input_file = './task6/input.json'
    regulator_file = './task6/regulator.json'
    transition_file = './task6/transition.json'
    element_for_phasing = 19.3
    main(input_file, regulator_file, transition_file, element_for_phasing)