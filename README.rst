=========
MIGRATREE
=========

migratree is a script generating the dependency graph of the migrations of a
Django application.
It's still a young project and has rough edges but works for me.

It basically goes through all the dependencies in the migration files
and write a GraphViz .dot file from a Python dictionary
(each key is a migration file and the values are the corresponding dependencies) 


Usage
-----

Copy the file migratree.py in the directory where all your Django applications
are.

Import migratree in your Django shell:

```python
>>> from migratree import generate_graph
>>> generate_graph('myapplication', 'myapplication.dot')
```


Now use Graphviz to generate a PDF or PNG file:

```
dot -Tpdf myapplication.dot -o myapplication.pdf
```


TODO
----

- Create a django plugin from the script
