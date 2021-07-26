from typing import Iterable, Any, TypeVar, Iterator, Tuple, Mapping, Union, Callable

def first(iterable: Union[Iterable, Mapping[Any, Any]]) -> Union[Any, Tuple[Any, Any]]:
    """
    Returns the first item in an iterable.
    If iterable is a dict, returns a tuple of the First key-value pair

    >>> first([1,2,3,4,5])
    1
    >>> first({1:"a", 2:"b"})
    (1, "a")

    Added in version: 0.1.0
    """

    if iterable:
        return next(iter(iterable))

    else:  # If iterable is empty
        return None
        
def rest(iterable: Iterable) -> Iterator:
    """
    Returns an iterator of all but the first element in the iterable.
    If iterable is empty it returns an empty iterator.

    >>> list(rest([1,2,3,4,5]))
    [2, 3, 4, 5]

    >>> tuple(rest({1:"a", 2:"b", 3:"c"}))
    ((2,"b"), (3, "c"))

    >>> tuple(rest([]))
    ()

    Added in version: 0.1.0
    """
    try:
        it = iter(iterable)
        next(it)  # discard value
        return it

    except StopIteration:  # If iterable is empty
        return iter([])

def second(iterable: Union[Iterable, Mapping[Any, Any]]) -> Union[Any, Tuple[Any, Any]]:
    """Returns the second item in iterable, or the last item if length is less than 2

    >>> second([1,2,3,4,5])
    2

    Added in version: 0.1.0
    """
    if len(iterable) < 2:
        return last(iterable)
    else:
        return first(rest(iterable))


def third(iterable: Union[Iterable, Mapping[Any, Any]]) -> Union[Any, Tuple[Any, Any]]:
    """Returns the third item in iterable, or the last item if length is less than 3

    >>> third([1,2,3,4,5])
    3

    Added in version: 0.1.0
    """
    if len(iterable) < 3:
        return last(iterable)
    else:
        return first(rest(rest(iterable)))


def fourth(iterable: Union[Iterable, Mapping[Any, Any]]) -> Union[Any, Tuple[Any, Any]]:
    """Returns the fourth item in iterable, or the last item if length is less than 4

    >>> fourth([1,2,3,4,5])
    4

    Added in version: 0.1.0
    """
    if len(iterable) < 4:
        return last(iterable)
    else:
        return first(rest(rest(rest(iterable))))
def is_atom(entity: Any) -> bool:
    """Everything that is NOT an iterable( except strings ) Are considered atoms.

    >>> is_atom("plain string")
        True
    >>> is_atom(1)
        True
    >>> is_atom([1, 2])
        False

    """
    if isinstance(entity, str):
        return True
    else:
        return not isinstance(entity, Iterable)

def is_fn(exp):
    return isinstance(exp, Callable)

def complement(
    expr: Union[bool, Callable[[Any], bool]]
) -> Union[bool, Callable[[Any], bool]]:
    """Takes in a predicate or a Boolean expression and
    returns a negated version of the predicate or expression.

    >>> complement(True)
    >>> False

    >>> def fn(el): # returns the Boolean of el
        return bool(el)
    >>> negated_fn = complement(fn)
    >>> fn(1)
    >>> True
    >>> negated_fn(1)
    >>> False

    Added in version: 0.1.0
    """

    if not isinstance(expr, Callable):
        # Wrapped around bool to handle cases like not_(1).
        # where 1 returns a boolean value of true.
        return not bool(expr)

    else:

        def negated(*args, **kwargs):
            return not expr(*args, **kwargs)

        return negated

def is_nested(collection: Iterable) -> bool:
    """returns true if a collection is nested

    Added in version: 0.1.0
    """
    return any(map(complement(is_atom), collection))

def is_special(fn):
    print('special')
    special_forms = {"if_", "define","let"}
    return fn.__name__ in special_forms

def eval_if(expr):
    print('in if')
    #only ifs.
    if leval(second(expr)): #test clause
        return leval(third(expr)) # then clause
    else:
        return leval(fourth(expr)) # else clause

def eval_define(expr):
    print('defining')
    name = second(expr)
    args = third(expr)
    body = fourth(expr)
    f = f"""def {name}({args}):return leval({body})"""
    # exec(f"global {name}")
    exec(f)
    exec(f"globals()['{name}']={name}")
    return f

def eval_let(expr):
    # expr is a nested list of form [args, bindings]
    # args is a list of args which are strings
    # bindings is a list of bindings

    _, args, bindings, body = expr
    for i in range(len(args)):
        if is_fn(bindings[i]):
            exec(f"{args[i]}={bindings[i].__name__}")
        else:
            exec(f"{args[i]}={bindings[i]}")

    return eval(f"leval({body})")




def special_eval(expr):
    print(f'finding special {first(expr).__name__}')
    special_fn = {"if_":eval_if, "define":eval_define,"let":eval_let}
    fn = special_fn[first(expr).__name__]
    return fn(expr)

def define():
    pass

def let():
    pass

def leval(expr):
    if is_atom(expr):
        return expr
    elif len(expr)==1: # if expr is iterable
        return first(expr)
    elif not is_fn(first(expr)):
        #return the values as a list
        return [leval(e) for e in expr]
    elif is_special(first(expr)):
        return special_eval(expr)
    else:
        #return the result of calling the function and passing the args
        return first(expr)(*[leval(e) for e in rest(expr)])


def if_(bool_expr: bool, then_expr: Any, else_expr: Any = None):
    """Created primarily to be used in lambda functions.

    for e.g.
    >>> f = lambda a,b : if_(a==b, "equality", "discrimination!")
    >>> f(1,3)
    'discrimination!'
    >>> f(2,2)
    'equality'

    """

    if bool_expr:
        return leval(then_expr)
    else:
        return leval(else_expr)

if __name__=="__main__":
    def infix(l, o, r):
        return [o, l, r]
    def reverse(l, o, r):
        return [o, r, l]

    def add(a,b):
        return a + b

    def minus(a,b):
        return a-b
    
    def apply(f,args):
        return f(*args)

    exp = (
        leval((infix, 1, add, 2))
    )
    print(leval(exp))

    # exp2 = (
    #     (apply, reverse, (infix, 1, minus, 2))
    # )
    # print(leval(exp2))
    # def mult(a,b):
    #     return a*b

    # fact = lambda x: leval(
    #                         (if_, x==1, 1, (mult, x, 
    #                                               (fact, (minus, x, 1)) ))
    # )
    # # fact = lambda x: if_(x==1, 1, x*fact(x-1))
    # print(fact(10))
    def add(a,b):
        return a+b

    print(leval((define, "fn", "a,b", "(add, a,b)")))

    # def f():
    #     exec("def fn():return 1")
    #     return 2

    leval((let, ["a","b"], [1,2], "(print, a, b)"))