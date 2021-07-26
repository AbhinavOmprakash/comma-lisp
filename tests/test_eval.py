from lisp_eval import leval, if_, define

def test_leval():
    assert leval((1,)) == 1
    assert leval((1,2,3)) == [1,2,3]

    add = lambda a,b: a+b
    assert leval((add,1,2)) == 3
    assert leval((add,(add, 1,2), 2)) == 5
    assert leval((add,(add, 1,2), (add, 1,2))) == 6
    assert leval(
            (add,
                (add, 
                    (add,1,2),3), 
                    (add, 1,2))
                    ) == 9

    sub = lambda a,b: a-b

    plambda = lambda a,b, op: leval( (if_, op=="add",(add, a,b), (lambda a,b:a*b, a,b)) )
    
    assert plambda(1,2,"add") == 3
    assert plambda(1,2,"sub") == 2


def test_define():
    leval((define, "test",lambda x:x))
    assert test(0) ==0