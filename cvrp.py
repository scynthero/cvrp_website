from functools import reduce

import numpy
import streamlit as st

import file_parser

alfa = 2
beta = 5
sigm = 3
ro = 0.8
th = 80
iterations = 1000


def generate_graph(file):
    graph, demand = file_parser.get_data(file)
    vertices = list(graph.keys())
    vertices.remove(1)

    edges = {(min(a, b), max(a, b)): numpy.sqrt((graph[a][0] - graph[b][0]) ** 2 + (graph[a][1] - graph[b][1]) ** 2) for
             a in graph.keys() for b in graph.keys()}
    pheromones = {(min(a, b), max(a, b)): 1 for a in graph.keys() for b in graph.keys() if a != b}

    return vertices, edges, demand, pheromones


def solution_one_ant(vertices, edges, capacity_limit, demand, pheromones):
    solution = list()

    while (len(vertices) != 0):
        path = list()
        city = numpy.random.choice(vertices)
        capacity = capacity_limit - demand[city]
        path.append(city)
        vertices.remove(city)
        while (len(vertices) != 0):
            probabilities = list(map(lambda x: ((pheromones[(min(x, city), max(x, city))]) ** alfa) * (
                    (1 / edges[(min(x, city), max(x, city))]) ** beta), vertices))
            probabilities = probabilities / numpy.sum(probabilities)

            city = numpy.random.choice(vertices, p=probabilities)
            capacity = capacity - demand[city]

            if (capacity > 0):
                path.append(city)
                vertices.remove(city)
            else:
                break
        solution.append(path)
    return solution


def rate_solution(solution, edges):
    s = 0
    for i in solution:
        a = 1
        for j in i:
            b = j
            s = s + edges[(min(a, b), max(a, b))]
            a = b
        b = 1
        s = s + edges[(min(a, b), max(a, b))]
    return s


def update_feromone(pheromones, solutions, best_solution):
    lavg = reduce(lambda x, y: x + y, (i[1] for i in solutions)) / len(solutions)
    pheromones = {k: (ro + th / lavg) * v for (k, v) in pheromones.items()}
    solutions.sort(key=lambda x: x[1])
    if (best_solution is not None):
        if (solutions[0][1] < best_solution[1]):
            best_solution = solutions[0]
        for path in best_solution[0]:
            for i in range(len(path) - 1):
                pheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))] = sigm / best_solution[1] + \
                                                                                     pheromones[
                                                                                         (min(path[i], path[i + 1]),
                                                                                          max(path[i], path[i + 1]))]
    else:
        best_solution = solutions[0]
    for l in range(sigm):
        paths = solutions[l][0]
        L = solutions[l][1]
        for path in paths:
            for i in range(len(path) - 1):
                pheromones[(min(path[i], path[i + 1]), max(path[i], path[i + 1]))] = (sigm - (l + 1) / L ** (l + 1)) + \
                                                                                     pheromones[(
                                                                                         min(path[i], path[i + 1]),
                                                                                         max(path[i], path[i + 1]))]
    return best_solution


# @st.cache
def main(file, vehicle_count, capacity_limit):
    best_solution = None
    vertices, edges, demand, pheromones = generate_graph(file)
    my_bar = st.progress(0)
    for i in range(iterations):
        solutions = list()
        for _ in range(vehicle_count):
            solution = solution_one_ant(vertices.copy(), edges, capacity_limit, demand, pheromones)
            solutions.append((solution, rate_solution(solution, edges)))
        best_solution = update_feromone(pheromones, solutions, best_solution)
        my_bar.progress(i/iterations + 1/iterations)
        print(str(i) + ":\t" + str(int(best_solution[1])))
    return best_solution
