from typing import Iterable, Any, TypeVar, Iterator, Tuple, Mapping, Union, Callable
from functionali import first, second, third, fourth, is_atom

def is_fn(exp):
    return isinstance(exp, Callable)


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