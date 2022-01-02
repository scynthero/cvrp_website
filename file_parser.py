import re


def get_data(content):
    graph = re.findall(r"^(\d+) (\d+) (\d+)$", content, re.MULTILINE)
    demand = re.findall(r"^(\d+) (\d+)$", content, re.MULTILINE)
    graph = {int(a): (int(b), int(c)) for a, b, c in graph}
    demand = {int(a): int(b) for a, b in demand}
    return graph, demand
