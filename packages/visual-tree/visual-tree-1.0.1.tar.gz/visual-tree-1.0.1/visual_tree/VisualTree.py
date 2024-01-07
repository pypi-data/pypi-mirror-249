from dataclasses import dataclass
from typing import Optional, Callable, Any, Iterable
from functools import lru_cache

@dataclass(frozen=True)
class ForkStyle():
    node_middle: str    = '├──── '
    parent_middle: str  = '│     '
    node_last: str      = '└──── '
    parent_last: str    = '      '

    def node(self, islast: bool):
        """
        Returns the appropriate node representation based on the value of `islast`.
        
        Parameters:
            islast (bool): Indicates whether the node is the last node in a sequence.
        
        Returns:
            object: The node representation.
        """
        return (
            self.node_last if islast
            else self.node_middle
        )

    def parent(self, islast: bool):
        """
        Return the appropriate parent value based on the given boolean flag.

        Args:
            islast (bool): A boolean flag indicating whether the parent is the last one.

        Returns:
            The parent_last value if islast is True, otherwise the parent_middle value.
        """
        return (
            self.parent_last if islast
            else self.parent_middle
        )


class VisualTree:
    def __init__(self, root: Any,
                 root_extend_func: Callable[..., Iterable] = iter,
                 root_validator: Callable[[Any], bool] = lambda x: hasattr(
                     x, '__iter__'),
                 *,
                 style: Optional[ForkStyle] = None,
                 naming: Optional[Callable[[Any], str]] = None,
                 naming_child: Optional[Callable[[Any], str]] = None,
                 **kwargs):
        # root and generator
        self.root = root
        self.birth = root_extend_func
        self.validator = root_validator

        # style
        self.style = style or ForkStyle()
        self._prefix = kwargs.get('prefix', '')
        self._naming = naming
        self._name_child = naming_child
        # depth data
        self.depth = kwargs.get('remain_depth')
        self._islast = kwargs.get('islast')

    @property
    def is_mummy(self) -> bool:
        """ Check if the root object is valid to generate a tree.
        
            usually check if it has `__iter__`
            
            you may define your own validator as `root_validator`
        """
        return self.validator(self.root)

    @lru_cache
    def children(self) -> list:
        """ Get the children of the root object
        
            it will be cached by lru_cache
            
            usually use `iter(self.root)`
            
            you may define your own generator as `root_extend_func`
        """
        child = self.birth(self.root)
        if isinstance(child, Iterable):
            return list(child)
        return child

    @property
    def children_count(self) -> int:
        """ Get the number of children of the root object. """
        return len(list(self.children()))
    
    def rebirth(self):
        """ Clear the cache of children. you should call this before re-building the tree. """
        self.children.cache_clear()

    def __str__(self) -> str:
        """ string representation of the tree , default naming is `str`
        you may define your own naming as `naming`
        for different naming for child, you may define `naming_child`
        """
        if self._naming is None:
            return str(self.root)

        return self._naming(self.root)

    def __iter__(self):
        """ Generate the visual representation of the tree.
        it will recurse until the depth is reached. 
        
        or None depth for unlimited depth.
        """
        if self._islast is None:
            yield f'{self._prefix}{self}'
        else:
            yield f'{self._prefix}{self.style.node(self._islast)}{self}'

        # check self is mummy
        if not self.is_mummy:
            return  # work end for non-mummy instance

        # check depth

        children_count = self.children_count
        if not children_count:
            return

        child_prefix = (self._prefix +
                        ('' if self._islast is None
                         else self.style.parent(self._islast)))

        next_depth = None if self.depth is None else self.depth - 1
        # no remaining depth, give ellipsis as child
        if next_depth is not None and next_depth <= 0:
            yield f'{child_prefix}{self.style.node_last}...'
            return

        children = enumerate(self.children())
        for idx, child_content in children:
            yield from VisualTree(
                child_content,
                root_extend_func=self.birth,
                root_validator=self.validator,

                style=self.style,
                prefix=child_prefix,

                remain_depth=next_depth,
                islast=(idx == children_count - 1),
                naming=self._name_child or self._naming,
                name_child=self._name_child
            )
            
    @property
    def seed(self):
        """ Generate the visual representation of the tree."""
        return self.__iter__

    def growing(self):
        """ list representation of the tree """
        return list(self)

    def daily(self):
        """ string body of the tree """
        return '\n'.join(self)

    def report(self):
        """ print the tree """
        for line in self:
            print(line)
