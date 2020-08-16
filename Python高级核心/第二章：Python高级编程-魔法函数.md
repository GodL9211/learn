# 第二章：Python高级编程-魔法函数

[笔记](https://coding.imooc.com/class/200.html "Python3高级核心技术97讲")



## 2.1 什么是魔法函数(网络用语)

- ``以双下划线开始，双下滑线结尾。魔法函数是为了增强一个类的特性。``

- ``魔法函数可以随意定义某个类的特性，这些方法在进行特定的操作时会自动被调用。``

### 2.1.1 需求：封装一个员工列表，并遍历查看

**（1）不使用魔法函数方法 **

```python
#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 18:20
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

company = Company(["tom", "bob", "jane"])
employee = company.employee
for em in employee:
    print(em)
```

**（2）使用``__getitem__(self, item)``魔法函数** 

```python
#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 18:20
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

    def __getitem__(self, item):
        return self.employee[item]

company = Company(["tom", "bob", "jane"])
for em in company:
    print(em)
        
"""
在解释器执行到for语句时，解释器首先寻找对象的迭代器。
虽然company对象没有迭代器，
但是解释器会尝试去寻找__getitem__()这一魔法函数，
有了这个魔法函数的对象就是一个可迭代的类型，即便没有迭代器，
解释器会调用该魔法函数，直到其抛出异常结束。
若注释__getitem__代码片段，则会抛出不可迭代异常。
"""
```

> 注意：在案例中，魔法函数既不是属于<class 'Company'>，也不是从<class 'object'>基继承过来。是一个独立的存在，往类里放入魔法函数之后，会增强类的一些类型。魔法函数不需要我们显示调用。Python会识别对象或自定义类的魔法函数，并隐式调用。

## 2.2 Python的数据模型以及数据模型对Python的影响

- 实际上魔法函数是网络上通常的叫法，其实魔法函数只不过是Python数据类型的一个概念而已。

```python
"""
当实现了__getitem__(self, item)魔法函数，就可以使用for循环去遍历。魔法函数实际上会影响python语法的，或可以理解为Python语法实际上会识别一个对象或者说自定义类里的魔法函数。
"""
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 18:20
# 使用__getitem__(self, item)魔法函数
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

    def __getitem__(self, item):
        return self.employee[item]

company = Company(["tom", "bob", "jane"])  # __getitem__(self, item) 实际上也是序列类型
company1 = company[:2]     
print(company1)

"""
['tom', 'bob']

"""
```

- 如果不实现``__getitem__(self, item)``就会报错

```python
#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 18:20
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

    # def __getitem__(self, item):
    #     return self.employee[item]

company = Company(["tom", "bob", "jane"])
company1 = company[:2]
print(company1)

"""
Traceback (most recent call last):
  File "E:/projects/vue-django/myproject/sample/chapter02/company03.py", line 14, in <module>
    company1 = company[:2]
TypeError: 'Company' object is not subscriptable

"""
```

```python
#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 18:20
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

    # def __getitem__(self, item):
    #     return self.employee[item]

company = Company(["tom", "bob", "jane"])
print(len(company))  # 没有定义__len__(self)或__getitem__(self, item)魔法函数时，这个语句会报错

"""
Traceback (most recent call last):
  File "E:/projects/vue-django/myproject/sample/chapter02/company03.py", line 14, in <module>
    print(len(company))
TypeError: object of type 'Company' has no len()
"""
```

- 两种方式实现对象可len()

  **（1）``__getitem__(self, item) + 切片``   实现**

  **（2）``__len__(self, item) ``  实现**

  在调用内置函数len()时，解释器首先会调用魔法函数``__len__(self)``，若没有，则退一步，去不断调用``__getitem__(self, item)``直到抛出异常，len()函数返回执行次数。

```python
!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 18:20
# 使用__getitem__(self, item)魔法函数 + 切片
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

    def __getitem__(self, item):
        return self.employee[item]

company = Company(["tom", "bob", "jane"])
company1 =company[:]
print(len(company1))

"""
3
"""
```

```python
#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 18:20
# 使用__len__(self)魔法函数
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list

    def __len__(self):
        return len(self.employee)

company = Company(["tom", "bob", "jane"])
print(len(company))

"""
3
""" 
```

> 魔法函数会影响Python语法和其内置函数本身的。

## 2.3 魔法函数一览

### 2.3.1 非数学运算

- 字符串表示   魔法函数提供了两个来应对开发模式的不同

  **（1）``__repr__`` 用于命令行模式，作用：输入对象名即可调用__repr__方法**

  ```python
  # jupyter或ipython 命令行终端运行
  class Company(object):
    def __init__(self, employee_list):
          self.employee = employee_list

      def __repr__(self):
          return ','.join(self.employee)
  
  company = Company(['tom', 'bob', 'jane'])
  company
  
  """
  tom,bob,jane
  """
  ```
  
  **（2）``__str__``用于脚本，作用：print(对象名)即可调用__str__方法 **
  
  ```python
  #!usr/bin/env python
  #-*- coding:utf-8 _*-
  # __author__：lianhaifeng
  # __time__：2020/5/10 18:20
  class Company(object):
    def __init__(self, employee_list):
          self.employee = employee_list
  
      def __str__(self):
          return ','.join(self.employee)
  
  company = Company(['tom', 'bob', 'jane'])
  print(company)  
  
  """
  tom,bob,jane
  """
  ```
  

```python
"""
魔法函数只要定义了，就不需要开发者调用，Python解释器自己知道什么时候调用它。
"""


# 以下会在后面章节渗透
"""
集合、序列相关
	__len__
	__getitem__
	__setitem__
	__delitem__
	__contains__
    
    
迭代相关
	__iter__
	__next__
    
    
可调用
	__call__
    
    
with上下文管理器
	__enter__
	__exit__
    
    
数值转换
	__abs__
	__bool__
	__int__
	__float__
	__hash__
	__index__
    
    
元类相关
	__new__
	__init__
    
    
属性相关
    __getattr__
    __setattr__
    __getattribute__
    __setattribute__
    __dir__
    
    
属性描述符
    __get__
    __set__
    __delete__
    
    
协程
    __await__
    __aiter__
    __anext__
    __aenter__
    __aexit   
"""
```

### 2.3.2 数学运算

```python
"""
数学运算在一般开发使用不多，在数据处理是用的比较多，这里简单举几个例子。
"""

# ============== __abs__ Demo start ============
class Nums(object):
    def __init__(self, num):
        self.num = num
        
    def __abs__(self):
        return abs(self.num)
    
    
num = Nums(-1)
print(abs(num))  # 结果：1
# ============== __abs__ Demo end ============


# ============== __add__ Demo start ============
class MyVector(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def __add__(self, other_instance):
        re_vector = MyVector(self.x+other_instance.x, self.y+other_instance.y)
        return re_vector
    
    def __str__(self):
        return "x:{x}, y:{y}".format(x=self.x, y=self.y)
    
    
first_vec = MyVector(1, 2)
second_vec = MyVector(2, 3)
print(first_vec+second_vec)  # 结果：x:3，y:5
# ============== __add__ Demo end ============
```



```python
一元运算符
    __neg__    -
    __pos__    +
    __abs__   |x|
    
    
二元运算符
    __lt__    <
    __le__    <=
    __eq__    ==
    __ne__    != 
    __gt__    > 
    __ge__    >=
    
    
算术运算符
    __add__         +
    __sub__         -
    __mul__         * 
    __truediv__     /
    __floordiv__    // 
    __mod__         % 
    __divmod__      divmod() 
    __pow__         ** 或 pow()
    __round__       round()


反向算术运算符
    __radd__ 
    __rsub__ 
    __rmul__ 
    __rtruediv__ 
    __rfloordiv__ 
    __rmod__ 
    __rdivmod__ 
    __rpow__


增量赋值算术运算符
    __iadd__ 
    __isub__ 
    __imul__ 
    __itruediv__ 
    __ifloordiv__ 
    __imod__ 
    __ipow__


位运算符
    __invert__    ~ 
    __lshift__    << 
    __rshift__    >> 
    __and__       & 
    __or__        | 
    __xor__       ^


反向位运算符
    __rlshift__ 
    __rrshift__ 
    __rand__ 
    __rxor__ 
    __ror__
    
    
增量赋值位运算符
    __ilshift__ 
    __irshift__ 
    __iand__ 
    __ixor__ 
    __ior__    
```

### 2.4 `len`函数的特殊性

`len`函数不仅仅调用`__len__`方法这么简单，`len`函数对于`set` `dict` `list`等Python原生数据结构做了内部的优化，其性能是非常高的。应为原生数据结构中，会有一个专门的字段来储存数据长度，那么`len`函数会直接去读取这个字段，而不会去遍历它。