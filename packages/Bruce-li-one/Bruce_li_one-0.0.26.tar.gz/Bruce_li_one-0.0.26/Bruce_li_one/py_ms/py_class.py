"""

在Python中，is，==和isinstance是三个不同的概念，具有不同的用途和功能。
1.is 是一个身份运算符，用于比较两个对象的身份是否相同。换句话说，它检查两个引用是否指向内存中的同一位置。例如：
```python
a = [1, 2, 3]
b = a  # b now references the same object as a
print(b is a)  # This will output True
```

2.== 是一个相等运算符，用于比较两个对象的值是否相等。它比较两个对象的值，而不是它们的身份。例如
```python
a = [1, 2, 3]
b = [1, 2, 3]  # b is a new object, even though it has the same elements as a
print(b == a)  # This will output True
```
3.isinstance() 是一个内置函数，用于检查对象是否是特定类的实例。它接受两个参数：要检查的对象和一个类（或一个包含多个类的元组）。它返回一个布尔值，表示对象是否是给定类的实例。例如
```python
class MyClass:
    pass

a = MyClass()
print(isinstance(a, MyClass))  # This will output True
```


--------------------------------------


"""


# def add(*aaa):
#     print(*aaa)#(1,2,3,4,5)
#     print(type(aaa)) #tuple
#     return sum(aaa) # 输出：15
#
# print(add(1, 2, 3, 4, 5))  # 输出：15

import time


# def timer_decorator(func):
#     def wrapper(*args, **kwargs):
#         start_time = time.time()
#         result = func(*args, **kwargs)
#         end_time = time.time()
#         print(f"函数 {func.__name__} 执行时间：{end_time - start_time:.4f} 秒")
#         return result
#     return wrapper
#
# x='1'
# @timer_decorator(x)
# def my_function():
#     # 执行需要计时的代码
#     time.sleep(2)
#     print("函数执行完成！")
#
# my_function()















def test_test(func):
    def warapper():
        start_time=time.time()
        func()
        end_time=time.time()
        print("耗时多久",end_time-start_time)
    return warapper

@test_test
def test_de():
    time.sleep(2)
    print("执行完成")

test_de()


def greet(name):
    print(f"Hello, {name}!")


def greet(age):
    print(f"You are {age} years old.")


greet("Alice")  # 输出 "Hello, Alice!"
greet(25)  # 输出 "You are 25 years old."