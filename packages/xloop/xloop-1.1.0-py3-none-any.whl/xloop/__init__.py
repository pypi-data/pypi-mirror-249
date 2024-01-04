from typing import Union, Iterator, Iterable, TypeVar, Set, Type, Tuple
from xsentinels.default import Default, DefaultType

DEFAULT_NOT_ITERATE = (str, int, bytes, dict)

try:
    # If pydantic is available, add that to the default list.
    from pydantic import BaseModel as PydanticModel
    DEFAULT_NOT_ITERATE = (*DEFAULT_NOT_ITERATE, PydanticModel)
except ImportError:
    pass

T = TypeVar("T")

__version__ = '1.1.0'


def xloop(
    *args: Union[Iterable[T], T],
    not_iterate: Iterable[Type] | None = None,
    default_not_iterate: Iterable[Type] | DefaultType = Default,
    yield_items_for_dicts=False
) -> Iterator[T]:
    """
    The intention behind this method is to easily iterate though things that are like 'lists'.
    Lists of dicts, lists of objects, etc.... but if it's a None, don't iterate that (or raise
    an error), we would rather skip that. Or if the value is not a list like thing, then we
    would simply just want to yield only that. Basically you can do things like this:


    >>> from xloop import xloop
    >>>
    >>> for obj in xloop(None):
    >>>     # Won't loop at all, as only value is `None`.
    >>>     assert False, 'Looped when we should not have.'
    >>>
    >>> for obj in xloop('hello!'):
    >>>     assert obj == 'hello!'
    >>>
    >>> for obj in xloop(['v1', 'v2']):
    >>>     assert obj in ['v1', 'v2']
    >>>
    >>> for obj in xloop({'some_key': 'some_value'}):
    >>>     assert obj == 'some_key'
    >>>
    >>> for key, value in xloop({'some_key': 'some_value'}, yield_items_for_dicts=True):
    >>>     assert key == 'some_key'
    >>>     assert value == 'some_value'


    Can also pass multiple items into xloop function, each one will be evaluated the same way,
    in order:

    >>> for obj in xloop('v1', 'v2'):
    >>>     assert obj in ['v1', 'v2']
    >>>
    >>> # Each passed in positional argument will be iterated, if needed:
    >>> for obj in xloop(['v1-1', 'v1-2'], 'v2'):
    >>>     assert obj in ['v1-1', 'v1-2', 'v2']

    >>> # If any argument is None, it will be skipped:
    >>> for obj in xloop(['v1-1', 'v1-2'], None, 'v2'):
    >>>     assert obj in ['v1-1', 'v1-2', 'v2']


    >>> # If a `None` is inside a list to be iterated, it will be skipped.
    >>> # Basically, `xloop` will never directly yield a `None` by its self.
    >>> result = []
    >>> for obj in xloop(['v1-1', None], 'v2'):
    >>>     result.append(obj)
    >>> assert result == ['v1-1', 'v2']

    xloop will try to iterate anything that is not in the `not_iterate` argument.
    If we get a TypeError while trying to iterate something we will just yeild the object
    and not iterate it
    (so you don't have to worry about causing an error with something that is not-iterable,
    it just loops/iterates though anything it can like you would want).

    Every argument passed in will be yielded if it can't be iterated or is in the `not_iterate`
    list. If argument can be iterated without a TypeError, every iterated value will be
    yielded instead. Only exception is if any yielded values are `None`, which are skipped.

    If the argument is of type in `not_iterate` (default: str|bytes|int)
    or is non-iterable (ie: TypeError while trying to get an iterator for it),
    then will I will yield that argument by its self without iterating it.

    If the argument is in any way iterable (except if it's type is in `not_iterate`),
    then will yield every value inside it. Only `None` value are skipped, I will never direcly
    yield a value of exactly `None`.

    `xloop` is useful if a var could be a list or just a normal value.
    Using `xloop` you can easily for "loop" though the value(s) of the var without inspecting,
    filtering, or combining them together.

    Future:
        Right now we don't loop recursively (ie: `[['hello']]` will yield a list: `['hello']`).
        In the future I may add a named-param 'recursively=True' flag you can pass to support this.

    Other Basic Examples:


    >>> some_var = 'some str'
    >>> for value in xloop(some_var):
    >>>     assert value == 'some str'

    Or another way that will do the same thing:

    >>> some_var = ['some str']
    >>> for value in xloop(some_var):
    >>>     assert value == 'some str'

    Other Examples:

    This: `list(loop("a-str", 1, ['hi-1', 'hi-2']))`
    Produces: `["a-str", 1, 'hi-1', 'hi-2']`

    This: `list(loop(None, "hello!"))`
    Produces: `["hello!"]`

    This: `list(loop(None, ["next!", None]))`
    Produces: `["next!"]`

    Args:
        not_iterate: Set of addtional types (added to the default set) to directly yield and not iterate.
            This can be any iterable (ie: list/tuple/etc).

        default_not_iterate: Default types to not iterate (added with `not_iterate` above),
            This is normally just `str`, `int`, `bytes` and `dict` (see `DEFAULT_NOT_ITERATE`).
            Also, if `pydantic` is avaliable we also add pydantic.BaseModel to the DEFAULT_NOT_ITERATE.

        yield_items_for_dicts: If True: Will yeild items from dicts, which are their key/value pairs as a tuple.
            The same as if you did this:

                >>> some_dict = {'key1': 'value1', 'key2': 'value2'}
                >>> for key, value in some_dict.items():
                ...     ...

                When True, `dict` will still be iterated by `.items()`, even if `dict` in the not iterated list.
    """
    # Reminder: 'anything' is all positional arguments passed into method.
    if not args:
        return

    if not_iterate is None and default_not_iterate is Default:
        not_iterate = DEFAULT_NOT_ITERATE
    else:
        if default_not_iterate is Default:
            default_not_iterate = DEFAULT_NOT_ITERATE

        if not_iterate is None:
            not_iterate = ()

        not_iterate = (*default_not_iterate, *not_iterate)

    for arg in args:
        if arg is None:
            continue

        if yield_items_for_dicts and isinstance(arg, dict):
            arg = arg.items()
        elif isinstance(arg, not_iterate):
            yield arg
            continue

        try:
            arg_iter = iter(arg)
        except TypeError:
            yield arg
        else:
            for item in arg_iter:
                if item is not None:
                    yield item
