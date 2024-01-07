# Visual Tree Python Package

## Introduction

this is a simple tool to visualize the tree structure of any recursable object in python.

## Installation

```bash
pip install visual-tree
```

## Usage

```python
from visual_tree import build_tree
tree = build_tree(data_structure)

# print the data_structure
print(tree)

# print the tree directly
tree()

# get the tree as a string (member of tree)
tree.tree

# get the tree as a list of strings (__iter__)
list(tree)
```

## Example

look at the [example.py](./example.py) file for more examples.

## requirements

- python needs to be installed

1. data structure with `__iter__` (better with `__len__` also)
2. data structure with `__bool__`
3. data structure with `__str__`

or

1. instand of `__iter__` you can use other extending methods pass with `mkchild` parameter
2. instand of `__bool__` you can use other extending methods pass with `valid` parameter

## License

Apache License 2.0 (see [LICENSE](./LICENSE) file)
