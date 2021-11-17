"""用Python 计算 24 点
枚举4个数字可以组成的所有的算式，找到其中等于24的式子。

对于每一个算式，我们用一棵二叉树来存取。根节点保存运算符（+,-,*,/），左子树保存运算符左侧的子算式，右子树保存运算符右侧的子算式，运算结果也存在根节点中
dfs构造解答树加剪枝即可

表达式直接计算结果用 eval(source), source='5*(5-1/5)'


"""

from itertools import permutations, product
from math import isclose

class Node(object):
    def __init__(self, result=None):
        self._left = None
        self._right = None
        self._operator = None
        self._result = result

    def set_expression(self, left_node, right_node, operator):
        self._left = left_node
        self._right = right_node
        self._operator = operator
        expression = "{} {} {}".format(left_node._result, operator, right_node._result)
        self._result = eval(expression)

    def __repr__(self):
        if self._operator:
            return '<Node operator="{}">'.format(self._operator)
        else:
            return '<Node value="{}">'.format(self._result)

    def get_expression(self):
        return __repr__(self)


def build_tree(left_tree, right_tree):
    '''build_tree 中会枚举所有的运算方式，组成新的二叉树并返回所有可能的组合。注意: 如果运算方式是除法，除数也就是右侧子算式的结果不能为0。'''

    treelist = []
    tree1 = Node()
    tree1.set_expression(left_tree, right_tree, "+")
    treelist.append(tree1)
    tree2 = Node()
    tree2.set_expression(left_tree, right_tree, "-")
    treelist.append(tree2)
    tree4 = Node()
    tree4.set_expression(left_tree, right_tree, "*")
    treelist.append(tree4)
    if right_tree._result != 0:
        tree5 = Node()
        tree5.set_expression(left_tree, right_tree, "/")
        treelist.append(tree5)
    return treelist


def build_all_trees(array):
    '''函数的输入是一组数字，第一层 for 循环中将这组数字，
    拆成左右两部分，分别对应左右两棵子树的部分，
    输出的 treelist 是所有可能的算式。'''

    if len(array) == 1:
        tree = Node(array[0])
        return [tree]

    treelist = []
    for i in range(1, len(array)):
        left_array = array[:i]
        right_array = array[i:]
        left_trees = build_all_trees(left_array)
        right_trees = build_all_trees(right_array)
        for left_tree in left_trees:
            for right_tree in right_trees:
                combined_trees = build_tree(left_tree, right_tree)
                treelist.extend(combined_trees)
    return treelist


def find_24(array):
    perms = permutations(array)
    found = False
    for perm in perms:
        treelist = build_all_trees(perm)
        for tree in treelist:
            if isclose(tree._result, 24, rel_tol=1e-10):
                expression = get_expression(tree)
                print("{} - {}".format(perm, expression))
                found = True
                break
        if found:
            break


def compute(x, y, op):
    if op=='+': 
        return x+y
    elif op=='*':
        return x*y
    elif op=='-':
        return x-y
    else:
        return x/y if y else None

def exp_old(p, iter=0):
    from itertools import permutations
    if len(p)==1:
        return [(p[0], str(p[0]))]
    operation = ['+','-','*','/']
    ret = []
    p = permutations(p) if iter==0 else [p]
    for array_n in p:
        #print(array_n)
        for num in range(1, len(array_n)):
            ret1 = exp(array_n[:num], iter+1)
            ret2 = exp(array_n[num:], iter+1)
            for op in operation:
                for va1, expression in ret1:
                    if va1==None:
                        continue
                    for va2,expression2 in ret2:
                        if va2==None:
                            continue
                        combined_exp = '{}{}' if expression.isalnum() else '({}){}'
                        combined_exp += '{}' if expression2.isalnum() else '({})'
                        new_val = compute(va1,va2,op)
                        ret.append((new_val,combined_exp.format(expression,op,expression2)))
                        if iter==0 and new_val==24:
                            return ''.join(e+'\n' for x,e in ret if x==24)
    return ret

EXP = {}
def exp(array_n,target,iter=0):
    if len(array_n)==1:
        return [(array_n[0], str(array_n[0]))]
    operation = ['+','-','*','/']
    ret = []
    for num in range(1,len(array_n)):
        exp1 = array_n[:num]
        exp2 = array_n[num:]

        ret1 = EXP[exp1] if exp1 in EXP else exp(exp1,target,iter+1)
        ret2 = EXP[exp2] if exp2 in EXP else exp(exp2,target,iter+1)
        EXP[exp1] = ret1
        EXP[exp2] = ret2
        for op in operation:
            for va1,expression in ret1:
                if va1==None:
                    continue
                for va2,expression2 in ret2:
                    if va2==None:
                        continue
                    combined_exp = '{}{}' if expression.isalnum() else '({}){}'
                    combined_exp += '{}' if expression2.isalnum() else '({})'
                    new_val = compute(va1,va2,op)
                    ret.append((new_val,combined_exp.format(expression,op,expression2)))
                    if iter==0 and new_val==target:
                        #print('ans')
                        return ''.join(e for x,e in ret if x==target)

    return ret if iter else None

def search(array):
    record = set()
    from itertools import permutations
    for p in permutations(array):
        if p in record:
            continue
        record.add(p)
        ret = exp(tuple(p),100)
        if ret:
            print(ret) ; break


def compute_6(x, y):
    '''得到两数的六种运算 + * - /, 后面两种运算各有两个结果，交换位置'''

    ret = []    
    ret.append(x+y)
    ret.append(x*y)
    ret.append(x-y)
    ret.append(y-x)
    ret.append(x/y if y else None)
    ret.append(y/x if x else None)
    return ret


def compute2(narray2):
    '''计算两个数的各种可能性，只要得到24就停止'''
    
    a, b = narray2[0], narray2[1]
    res = compute_6(a,b)
    opt = ''
    for i, c in enumerate(res):
        if c==24:            
            pass


def get24(narray):
    '''分治法得到给定n个数的24点计算公式
    '''
    if len(narray)==2:
        return compute2(narray)
    elif len(narray)==4:
        a,b,c,d = (narray[i] for i in range(4))
        x, y = compute_6(a, b), compute_6(c, d)
        x_y = [(i,j) for i in x for j in y]
        for k, me in enumerate(x_y):
            print(k, me)
            get24(me)

        x, y = compute_6(a, c), compute_6(b, d)
        x_y = [(i,j) for i in x for j in y]
        for k, me in enumerate(x_y):
            print(k, me)
            get24(me)
            
'''https://zhuanlan.zhihu.com/p/37608401'''        