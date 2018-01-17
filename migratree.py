# -*- coding: utf-8 -*-

"""
Generate the dependency tree of the migrations for a given Django application
"""

import os
import itertools
import glob
from importlib import import_module


def import_dependencies(filepath):
    module_name = os.path.splitext(filepath)[0].replace('/', '.')
    module = import_module(module_name)
    if hasattr(module, 'Migration') and hasattr(module.Migration, 'dependencies'):
        dependencies = [x[1] for x in module.Migration.dependencies]
    else:
        dependencies = []
    return dependencies


def node_name(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]


def product(f, deps):
    # The root has no deps
    if len(deps) == 0:
        return [(f, 'None',)]
    else:
        return list(itertools.product([f], deps))


def make_graph(app):
    """
    Read the depedencies and store them in a dictionary
    """
    graph = {}
    migration_files = sorted(glob.glob(os.path.join(app, 'migrations', '0*.py')))
    for f in migration_files:
        dependencies = import_dependencies(f)
        graph[node_name(f)] = dependencies
    return graph


def make_pairs(graph):
    """
    {A: [B, C]} -> [(A, B), (A, C)]
    """
    return [product(f, deps) for f, deps in graph.items()]


def make_dot(pairs):
    data = '\n'.join("m{1} -> m{0}".format(e[0], e[1]) for e in itertools.chain(*pairs))
    dot = 'digraph g {\n'
    dot += data
    dot += '\n}'
    return dot


def save_dot_file(filename, dot):
    with open(filename, 'w') as f:
        f.write(dot)
    print('Saved the file {}'.format(filename))


def generate_graph(app, filename=''):
    """
    Save the dependency graph of the migrations for the specified app
    in a dot file.
    """
    graph = make_graph(app)
    pairs = make_pairs(graph)
    dot = make_dot(pairs)
    if not filename:
        filename = app + '.dot'
    save_dot_file(filename, dot)
