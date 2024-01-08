import numpy as np


# TODO: write unit test
# what do we need this function for?
def shuffle(x_data, y_data=None):
    # Create a list of indices based on the length of x_data
    shuf_idxs = np.arange(len(x_data))

    # Shuffle the indices
    np.random.shuffle(shuf_idxs)

    # Reorder x_data and y_data (if it exists) using the shuffled indices
    # This approach is agnostic to the type of x_data and y_data
    x_data_shuffled = [x_data[i] for i in shuf_idxs]

    if y_data is not None:
        y_data_shuffled = [y_data[i] for i in shuf_idxs]
    else:
        y_data_shuffled = None

    return x_data_shuffled, y_data_shuffled


def topological_sort(dicts: list, idx_key='name', dependency_key='depends_on') -> list:
    def dfs(node: int, visited: set, stack: list, graph: dict):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, visited, stack, graph)
        stack.append(node)

    # Build graph
    graph = {}
    node_to_dict = {}
    for d in dicts:
        node = d[idx_key]
        node_to_dict[node] = d
        if dependency_key in d:
            if d[dependency_key] not in graph:
                graph[d[dependency_key]] = []
            graph[d[dependency_key]].append(node)

    # Perform DFS and topological sort
    visited = set()
    stack = []
    for node in node_to_dict:
        if node not in visited:
            dfs(node, visited, stack, graph)

    # Reconstruct dictionaries from sorted order
    sorted_dicts = [node_to_dict[node] for node in reversed(stack)]
    return sorted_dicts
