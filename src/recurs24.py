r"""Recursive Algorithm for calculating 24 number from given 4 nums between 1 and 13.
递归计算24点程序设计思路如下：
1. 给定 4 个数 [a,b,c,d] 允许重复数出现
2. 任取两个数，构造多个运算式子。与剩下的两个数构造的多个运算式进行匹配。
   有3种匹配 [ab,cd],[ac,bd],[ad,bc]
3. 递归到最后一个式子后，比较与 24 的差值，判断该算式是否满足条件。

"""

from math import isclose
import random

# global 全局变量定义
COMPARE_N = 24
solutions = set()

def merge2(a, b):
    '''两个数配一个运算符号，共有 6 种可能，去掉了 加法和乘法（满足交换律）中的重复项。a+b,a-b,a*b, b-a,a/b,b/a，注意判断除数不能为 0。
    '''
    res = set()
    ops = ['+','-','*','/']

    for i in range(3):
        res.add('{0} {1} {2}'.format(a, ops[i], b))
    
    res.add('{0} {1} {2}'.format(b, ops[1], a))
    
    if eval(str(b)) != 0:
        res.add('{0} {1} {2}'.format(a, ops[3], b))
    if eval(str(a)) !=0 :
        res.add('{0} {1} {2}'.format(b, ops[3], a))
    
    return res


def recurs24(numbers):
    global solutions
    if len(numbers) == 1:
        if isclose(eval(numbers[0]), COMPARE_N):
            solutions.add(numbers[0][1:-1])  # 清除最外围的一对括号`()`
    else:
        for i in range(len(numbers)):
            for j in range(i+1, len(numbers)):
                _nums = [x for p, x in enumerate(numbers) if p != i and p != j]
                _ariths = merge2(str(numbers[i]), str(numbers[j]))
                for one in _ariths:
                    recurs24(["("+ str(one) +")"] + _nums)


def inputData(count):
    '输入 n 个随机数字'
    digits = ''
    while len(digits) != count or not all(d in '45678910111213' for d in digits):
        digits = input('请输入{0}个数字( < 14, 空格隔开): '.format(count))
        digits = digits.strip().split()
    return digits


if __name__ == '__main__':    
    count = 4
    answer = ''
    while answer.lower() != 'q':
        if answer.lower() == '/':
            indata = inputData(count)
        else:
            indata = [random.randint(1, 13) for _ in range(count)]

        recurs24(indata)  # 递归寻找答案
        # 输出答案
        print("给定数据 {0}, 找到 {1} 个解！".format(indata, len(solutions)))
        for i, s in enumerate(solutions):
            print("{0}: {1} = 24".format(i+1, s))
        
        solutions = set()  # 清除全局变量，重新开始。
        answer = input("q 退出, / 自己输入, 其他键继续: ")
