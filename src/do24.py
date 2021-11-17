"""暴力穷举法 “求24点” 的编程思路：（do24.py)
1、得到给定数组的全排列：def perms(given_array), 返回值用集合可以清除重复项
2、给定四则运算符号的全部组合，含重复，def operations(len(given_array)-1)
3、二重循环，得到 所有可能的 4个数与3个符号的组合 (array1，ops1)
4、考虑运算优先级问题，4个数，4-1个符号可以组成 5 种与优先级有关的代数式
5、计算代数式的值，eval(expression), 并与 24 比较，“相等”就保留代数式。
6、可以通过集合对元素唯一性要求，可以清除部分完全一样的算式。
7、对于加法和乘法的运算规则可知：满足交换律，故也可以清除重复项 TODO
8、目前解决了3，4个数的情形，推广到超过 4个数，如何？ TODO

"""

from sys import argv
from itertools import permutations, product
from math import isclose

RESULTN = 24


def operations(ndim):
    '''穷举各种运算排列，含重复运算，ndim = 给定数个数-1
    4个数，需要3个运算符号才能连起来。
    '''
    basic_ops = ['+','-','*','/']
    return product(basic_ops, repeat = ndim)

def perms(narr):
    '''得到给定数组的全排列，4个数有4！个不同的排列
    建议用集合，可以预先删除重复项。
    '''
    return set(permutations(narr))

def get_expr(a, ops):
    '''要考虑运算顺序：
    譬如：设四张牌为 $a、b、c、d$，代表4个数，运算符为 $①、②、③$，代表3个数学运算符号。代数表达式为 $a ① b ② c ③ d$。 
    这 3 个运算符的运算顺序有 $3！=6$ 种，分别是：  
    1．①②③  2.①③②  3.②①③  4.②③① 5.③①②  6.③②①
    等价的表达式分别是：  
    1. [(a①b)②c]③d  2. (a①b)②(c③d)  3. [a①(b②c)]③d  
    4. a①[(b②c)③d]  5. (a①b)②(c③d)  6. a①[b②(c③d)]

    (2)与(5)等价, 只取其一。
    '''

    #TODO: 清除 a+b=b+a, a*b=b*a的情形, 满足交换律只取一种，满足结合律也只取一种。
    # 同级运算符从左到右运算即可
    if len(a) == 4:
        exp1 = '(({0}{1}{2}){3}{4}){5}{6}'.format(a[0], ops[0], a[1], ops[1], a[2], ops[2], a[3])
        exp2 = '({0}{1}{2}){3}({4}{5}{6})'.format(a[0], ops[0], a[1], ops[1], a[2], ops[2], a[3])
        exp3 = '({0}{1}({2}{3}{4})){5}{6}'.format(a[0], ops[0], a[1], ops[1], a[2], ops[2], a[3])
        exp4 = '{0}{1}(({2}{3}{4}){5}{6})'.format(a[0], ops[0], a[1], ops[1], a[2], ops[2], a[3])
        exp5 = '{0}{1}({2}{3}({4}{5}{6}))'.format(a[0], ops[0], a[1], ops[1], a[2], ops[2], a[3])
        expr = [exp1, exp2, exp3, exp4, exp5]
    if len(a) == 3:
        exp1 = '({0}{1}{2}){3}{4}'.format(a[0], ops[0], a[1], ops[1], a[2])
        exp2 = '{0}{1}({2}{3}{4})'.format(a[0], ops[0], a[1], ops[1], a[2])
        expr = [exp1, exp2]

    return expr


def find24(narr):
    '''找到所有结果是24的运算式,
    TODO: 如何清理重复的算式，可以交换的算式, 譬如 a*b = b*a, a+b = b+a
    '''

    ops = set(operations(len(narr)-1))  #
    perms_arr = perms(narr)  #清除了带重复数的排列
    reslist = set()

    for arr1 in perms_arr:
        for op in ops:
            expressions = get_expr(arr1, op)  # 组合数组和运算符号组
            #print(expr)
            for expr in expressions:
                try:
                    res = eval(expr)  # 计算表达式的值用eval(source)
                except ZeroDivisionError:
                    continue

                if isclose(res, RESULTN):
                    reslist.add('{0}={1}'.format(expr, round(res)))  #int(24.0)=24

    return reslist  # 可以清除相同项。


def output(result, outfile=None):
    '''打印输出结果'''
    if outfile is not None:
        with open(outfile, encoding='utf-8', mode='a') as output:
            for one in result:
                output.write('{0}, '.format(one))
            output.write('\n')
    #else:
    for one in result:
        print(one, end='; ')


if __name__=='__main__': 
    if len(argv) > 1:
        inputa = argv[1]  # 如何处理多个数组的情形？
        if len(inputa) > 0: 
            inarray = eval(inputa) 
        else:
            print("输入的数据{0}有误！".format(inputa))
            exit()

        sep = ' '
        enter = '<div STYLE="page-break-after: always;"></div>\n\n'
        tmpfile = argv[2] if len(argv) > 2 else ""
        if len(tmpfile) == 0:
            tmpfile = "temp_point24"  
        outfile = tmpfile if tmpfile.find(".") > 0 else tmpfile+".md" 

        print('结果保存在文件 {0} 中!'.format(outfile))

        if type(inarray) is list is type(inarray[0]):
            for one in inarray:
                res24 = find24(one)
                if len(res24) > 0:
                    output(res24, outfile)
                else:
                    print('{0} 无解'.format(one))
        else:
            res24 = find24(inarray)
            if len(res24) > 0:
                output(res24, outfile)
            else:
                print('{0} 无解'.format(inarray))
    
    else:
        print("""计算24点游戏。
        使用说明：python do24.py "数组" [可选输出文件名]
        使用举例：python do24.py "[5,5,5,1]"
        使用举例：python do24.py "[[5,5,5,1],[1,2,3,4]]" point24.md
        """)

'''
Refs 
https://blog.csdn.net/pp634077956/article/details/53354786
https://blog.csdn.net/haoxun08/article/details/104828749
'''