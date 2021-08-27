from comma_lisp import eval_, if_, define

def test_leval():
    assert eval_((1,)) == 1
    assert eval_((1,2,3)) == [1,2,3]

    add = lambda a,b: a+b
    assert eval_((add,1,2)) == 3
    assert eval_((add,(add, 1,2), 2)) == 5
    assert eval_((add,(add, 1,2), (add, 1,2))) == 6
    assert eval_(
            (add,
                (add, 
                    (add,1,2),3), 
                    (add, 1,2))
                    ) == 9

    sub = lambda a,b: a-b

    plambda = lambda a,b, op: eval_( (if_, op=="add",(add, a,b), (lambda a,b:a*b, a,b)) )
    
    assert plambda(1,2,"add") == 3
    assert plambda(1,2,"sub") == 2


def test_define():
    eval_((define, "test",lambda x:x))
    assert test(0) ==0