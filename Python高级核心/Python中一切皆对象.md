# 第一章：Python高级编程-Python一切皆对象

[笔记](https://coding.imooc.com/class/200.html "Python3高级核心技术97讲")

Python中一切皆对象，Python面向对象更彻底。

### 1.1 函数和类也是对象，属于Python的一等公民

#### 1.1.1 可以赋值给一个变量

```python
#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 14:13

def ask(name="coder"):
    print(name)

class Person:
    def __init__(self):
        print("峰鸽")
# 函数赋值给变量后执行
my_func = ask
my_func("王尼玛") # 输出”王尼玛“

# 类作为变量赋值给变量后实例化
my_class = Person
my_class() # 会执行__init__()方法，输出“峰鸽”
```

![image-20200510142354410](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200510142354410.png)

#### 1.1.2 可以增加到集合对象中

```python
#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 14:13

def ask(name="峰鸽"):
    print(name)

class Person:
    def __init__(self):  # 不返回实例，返回的类对象
        print("峰鸽")

def print_type(item):
    print(type(item))

# 类和函数增加到集合对象
obj_list = []
obj_list.append(ask)
obj_list.append(Person)
for item in obj_list:
    print(item())
```

![image-20200510143916929](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200510143916929.png)

#### 1.1.3 可以作为参数传递给函数

```python
#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 14:13

def ask(name="峰鸽"):
    print(name)

class Person:
    def __init__(self):  # 不返回实例，返回的类对象
        print("峰鸽")

def print_type(item):
    print(type(item))

# 类和函数增加到集合对象
obj_list = []
obj_list.append(ask)
obj_list.append(Person)
for item in obj_list:
    print_type(item)  # 作为参数传入函数
```

#### 1.1.4 可以当做函数的返回值

```python
#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：lianhaifeng
# __time__：2020/5/10 14:13

def ask(name="峰鸽"):
    print(name)

class Person:
    def __init__(self):  # 不返回实例，返回的类对象
        print("峰鸽")

def decorator_func():
    print("dec start")
    return ask  # 作为函数的返回值，Python装饰器的部分实现原理

my_ask = decorator_func()
my_ask("tom")
```

### 1.2 type、object和class的关系

```python
"""
原来type并没有那么简单。
type的两种作用，一是可以生成类，二是判断一个对象的类型。
"""

>>> a = 1
>>> type(1)
<class 'int'>   # class也是一个对象
>>> type(int)
<class 'type'>  # type生成了int,int生成了1                

>>> b = "abc"
>>> type(b)
<class 'str'>
>>> type(str)
<class 'type'>

"""
wow, 得出来一个现象 type->int->1和type->str->"abc"，
"""
```

那么猜测我们自己定义的类是不是也是这样关系呢？

```
>>> class Student():
...    pass
...
>>> stu = Student()
>>> type(stu)
<class '__main__.Student'>
>>> type(Student)
<class 'type'>

"""
soga, 我们可以得出一个结论： type->class->obj,
也就是说，我们所定义的类是type类的一个实例化对象，
而我们的stu是我们自己定义类Student的一个实例化对象。
也就是说的<class 'type'>是用来生成类的。

我仿佛感受到了Python一切皆对象的魅力所在，
哈哈哈。
"""

# object是所有类默认的一个基类, 即object是最顶层基类。
>>> Student.__bases__
(<class 'object'>,)
>>> class MyStudent(Student):
...    pass
...
>>> MyStudent.__bases__
(<class '__main__.Student'>,)

"""
问题来了：type也是一个类，同时type也是一个对象，那么type的基类是谁？
"""

>>> type.__bases__
(<class 'object'>,)

# 好玩的来喽，如果执行type(object)看看object类是谁生成的呢？
>>> type(object)
<class 'type'>
>>> type(type)
<class 'type'>

# 再来好玩的！来看看object类基类谁呢？
>>> object.__bases__
()

# 结论：type继承了object，而object又是type的实例，type也是自身的实例。
# type连自己都变成对象，所有类都是type创建出来的（list、str..）。
```

![image-20200510164932658](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200510164932658.png)

这张图给我展现了``type是个厉害的家伙啊，他把一切都变成了对象，连自己都不放过。所以，有了``你就不缺对象啦，哈哈哈哈。

好啦，其实上面一系列的不伦关系都是`指针`这个东西干的，嘿嘿嘿........

object是所有类的基类，type都要继承object。

> 总结：类都是type的实例 (object也是type的实例，type本身也是自己的实例)，所有的类的顶层基类都是object (type的基类也是object)。Python一切皆对象的哲学就是玩起来的。
>
> Python一切皆对象这么做就是为了一切都可以轻易的修改，使得Python非常灵活。C++/Java中的类一旦加载到内存后就不能修改（不绝对，修改很困难）。Python把类都搞成对象了，这样修改起来就很方便。

**求评论区解释，遇到的问题就是：type需要继承object，但是object又是type的实例，这样的关系有矛盾啊？**

### 1.3 Python中的常见内置类型

#### 1.3.1 对象的三个特征

**(1) 身份**

```
Copy>>> a = 1
"""
这里的1是值由<class 'int'>进行封装，最后变量a指向这个obj
"""
>>> id(a)
5656454878 # 不同机器不同结果
```

**(2) 类型**

```python
"""
字符串类型
int类型
...
"""
```

**(3) 值**

#### 1.3.2 类型

**（1）None(全局只有一个)**

```
Copy"""
解释器启动时None对象被创建，且全局只有一个。
"""

>>> a = None
>>> b = None
>>> id(a) == id(b)  # 通过对比两个变量所指向内存地址相同，可见None对象全局只有一个。
True
```

**（2）数值**

- int

- float

- complex (复数)

- bool

**（3）迭代类型**

- 迭代器
- 生成器

**（4）序列类型**

- list

- bytes、bytearray、memoryview (二进制序列)

* range

- tuple

- str

- array

**（5）映射(dict) **

**（6）集合**

- set

  与`dict`实现原理相似，性能高。

- frozenset

**（7）上下文管理类型(with语句)**

**（8）其他 **

对于Python，一切皆对象啦。那么就会有以下类型。

- 模板类型

- class和实例

- 函数对象

- 方法类型

- 代码类型

- object类型

- type 类型

- ellipsis 类型

- notimplemented 类型

> Python 的灵活性就使得它的严谨性有一定损失，但是其带给我们开发效率上的提升是显然的。