from copy import copy as shallowcopy, deepcopy


def _resolve_attr(obj, attr, default):
    """ auxiliary function for attrgetter. """
    for name in attr.split("."):
        if hasattr(obj, name):
            obj = getattr(obj, name)
        else:
            return default
    return obj


def attrgetter(*items, default=None):
    """ Return a callable object that fetches the given attribute(s) fro its operand.
    Similar to operator.attrgetter, but support default value when a named attr is not found.

    Examples
    --------
    Get attributes with default values.

    >>> from collections import namedtuple
    >>> from pprog import attrgetter
    >>> name = namedtuple("Name", ["first", "last"])
    >>> name.first = "Zhiqing"
    >>> name.last = "Xiao"
    >>> person = namedtuple("Person", ["name", "city"])
    >>> person.name = name
    >>> person.city = "Beijing"
    >>> g = attrgetter("name.first", "name.middle", "name.last", default="")
    >>> result = g(person)
    >>> result
    ("Zhiqing", "", "Xiao")
    """
    if len(items) == 1:
        attr = items[0]

        def g(obj):
            return _resolve_attr(obj, attr, default)
    else:

        def g(obj):
            return tuple(_resolve_attr(obj, attr, default) for attr in items)
    return g


def _resolve_item(obj, item, default):
    """ auxiliary function for itemgetter. """
    if not isinstance(item, list):
        item = [item]
    for i in item:
        try:
            obj = obj[i]
        except KeyError:
            return default
    return obj


def itemgetter(*items, default=None):
    """ Return a callable object that fetches the given item(s) fro its operand.
    Similar to operator.itemgetter, but support multi-level item and a default value when a item is not found.

    Examples
    --------
    Get multiple items with default values.

    >>> person = {"name": {"first": "Zhiqing", "last": "Xiao"}, "city": "Beijing"}
    >>> g = itemgetter(["name", "first"], ["name", "middle"], ["name", "last"], default="")
    >>> result = g(person)
    >>> result
    ("Zhiqing", "", "Xiao")
    """
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return _resolve_item(obj, item, default)
    else:

        def g(obj):
            return tuple(_resolve_item(obj, item, default) for item in items)
    return g


def identity(value, *args, **kwargs):
    """ Returns the first positional arguments, and ignore other arguments.

    Examples
    --------
    Return the first position parameter and ignore all other parameters.

    >>> from pprog import identity
    >>> result = identity("value", "other_input", key="other_keyword_input")
    >>> result
    'value'

    The return value is as-is without copying.

    >>> import pandas as pd
    >>> df = pd.DataFrame()
    >>> identity(df) is df
    True
    """
    return value


def perm(values, cycle):
    """ Permutates a list according to cycle notation.

    Examples
    --------
    Permutate a list of strings.

    >>> from pprog import perm
    >>> result = perm(["a", "b", "c", "d", "e", "f", "g"], [1, 2, 4])
    >>> result
    ['a', 'c', 'e', 'd', 'b', 'f', 'g']

    Permutate a list of integers.

    >>> from pprog import perm
    >>> perm(list(range(6)), [0, 1, 2])
    [1, 2, 0, 3, 4, 5]
    """
    results = shallowcopy(values)
    for i, v in enumerate(cycle):
        results[v] = values[cycle[(i+1) % len(cycle)]]
    return results


class ConstantCreator:
    """ Callable that returns the same constant when it is called.

    Examples
    --------
    Always return the string "value".

    >>> from pprog import ConstantCreator
    >>> creator = ConstantCreator("value")
    >>> creator()
    'value'

    Create a pd.DataFrame whose elements are all empty lists.

    >>> import pandas as pd
    >>> from pprog import ConstantCreator
    >>> df = pd.DataFrame(index=range(3), columns=["A"])
    >>> df.applymap(ConstantCreator([]))
        A
    0  []
    1  []
    2  []

    Return a new copy when `copy=True`.

    >>> import pandas as pd
    >>> from pprog import ConstantCreator
    >>> df = pd.DataFrame(index=range(3), columns=["A"])
    >>> ConstantCreator(df, copy=True)() is df
    False
    """
    def __init__(self, value, copy=False):
        self.value = value
        if copy:
            if copy in ["shallow", shallowcopy]:
                copy = shallowcopy
            else:
                copy = deepcopy
        else:
            copy = identity
        self.copy = copy

    def __call__(self, *args, **kwargs):
        return self.copy(self.value)


class PermArgsExecutor:
    """ Callable that swaps position parameters according to cyclc notation.

    Examples
    --------
    Swap the first two positional arguments.

    >>> from pprog import PermArgsExecutor
    >>> executor = PermArgsExecutor(range)
    >>> executor(3, 2, 6)
    range(2, 3, 6)

    Swap arguments according to cycle notation.

    >>> from pprog import PermArgsExecutor
    >>> executor = PermArgsExecutor(range, cycle=[1, 2])
    >>> executor(3, 2, 6)
    range(3, 6, 2)
    """
    def __init__(self, fun, cycle=None):
        self.fun = fun
        self.cycle = cycle or [0, 1]

    def __call__(self, *args, **kwargs):
        args = perm(list(args), self.cycle)
        return self.fun(*args, **kwargs)
