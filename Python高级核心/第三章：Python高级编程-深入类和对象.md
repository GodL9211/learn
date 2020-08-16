## 3.1 鸭子类型和多态

```python
"""
当看到一直鸟走起来像鸭子、游泳起来像鸭子、叫起来像鸭子，那么这只鸟就可以被称为鸭子。
这句话看上去有趣，却不太容易理解。接下来用实例来说明。
"""

# ============ Demo1 start =============
class Cat(object):
    def say(self):
        print("I am a cat")
        
        
class Dog(object):
    def say(self):
        print("I am a dog")

        
class Duck(object):
    def say(self):
        print("I am a duck")
        
        
animal = Cat
animal().say()
# ============ Demo1 end ===============

# ============ Java pseudocode contrast start =============
"""
在 Java中实现多态，需要子类继承父类并重写父类方法。并需要声明类型
Dog继承Animal,必须重写say方法
"""
class Animal:
    def say(self):
        print("I am an animal")
        
        
class Dog(Animal):
    def say(self):
        print("I am an Doy")
        
        
animal = Dog()
animal.say()

# ============ Java pseudocode contrast end =============

"""
在Python中就不一样了，如Demo1所示，变量animal可以指向任意类型，
所有类不需要继承父类，只需定义相同的方法say()就可以实现多态。在调用的时候，
只需调用共同的say()方法。如下示例。
"""

# ============== Demo2 start ===================
class Cat(object):
    def say(self):
        print("I am a cat")
        
        
class Dog(object):
    def say(self):
        print("I am a dog")

        
class Duck(object):
    def say(self):
        print("I am a duck")
        
        
animal_list = [Cat, Dog, Duck]
for animal in animal_list:
    animal().say()  
# ============== Demo2 end ===================

# ============== Demo3 start ====================
a = ["bobby1", "bobby2"]
name_tuple = ("bobby3", "bobby4")
name_set = set()
name_set.add("bobby5")
name_set.add("bobby6")
name_list = ["bobby7", "bobby8"]
a.extend(name_tuple)
a.extend(name_list)
a.extend(name_set)

"""
def extend(self, *args, **kwargs): # real signature unknown
    """ Extend list by appending elements from the iterable. """
    pass
不能单纯的认为extend()只能传递一个列表，传进去的是iterable
"""
# =============== Demo4 end ======================

"""
在 Demo3 中不知你是否发现除了列表本身，元组和集合对象都可以传入列表对象的
extend()方法。其实是extend()是接收一个可迭代对象，也就是前面章节所提到的
迭代类型，那么好玩的就来了。
"""

# =============== Demo5 start =====================
class Dog(object):
    def say(self):
        print("I am a dog")

    def __getitem__(self, item):
        print("loop!!!!!!!!")


a = ["bobby1", "bobby2"]
dog = Dog()
a.extend(dog)

"""
结果：
loop!!!!!!!!
loop!!!!!!!!
loop!!!!!!!!
loop!!!!!!!!
loop!!!!!!!!
loop!!!!!!!!
loop!!!!!!!!
loop!!!!!!!!
loop!!!!!!!!
....
"""
# =============== Demo5 end =======================

"""
在 Demo5 中程序陷入了死循环，传入一个Dog对象也没有报错，
为什么？因为魔法函数，前面章节提到的__getitem__()是的对象
变成了可迭代对象，因此传入extend中，方法一直运行，直到抛出异常，
但是示例中是不会抛出异常的，因此会陷入死循环。
python当中魔法函数正是利用了鸭子类型。
"""
```

## 3.2 抽象基类（abc模块）

```python
"""
abc -> abstract base class
抽象基类相当于Java中的接口，Java无法实现多继承，
但可以继承多个接口，接口是不可以实例化的。所以说，
Python中的抽象基类也是不可以实例化的。Python是
动态语言，是没有变量类型的。实际上，变量只是一个符
号而已，它是可以指向任意类型的对象。动态语言不需要
指定类型，所以就少了一个编译时检查错误的环境，只有运
行时才知道错误。
与Java最大的一个区别就是，在定义一个类的时候，是不
需要去继承一个指定类型的。而要知道Python的一个类是
属于哪个类型的，是去看实现了那些魔法函数，魔法函数赋予
了类的一些特性。在实现了某个魔法函数之后，使得对象变成了
一个指定的类型，这种方法，在Python中可以说是一种协议。
在写代码是要尽量遵守这种协议，这样写出来的代码，才是
足够Pythonic的一种代码。
"""

# ============ Demo1 start =============
class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list
        
    def __len__(self):
        return len(self.employee)
      
com = Company(["bob", "jane"])
# 如何判断对象的类型呢？
# 第一种方案
print(hasattr(com, '__len__'))  # 通过判断是否有某个属性而判断属于什么类型，不够直观

# 通过抽象基类
from collections.abc import Sized
print(isinstance(com, Sized))  # 这样的方式更加直观，易读
"""
class Sized(metaclass=ABCMeta):

    __slots__ = ()

    @abstractmethod
    def __len__(self):
        return 0

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Sized:
            return _check_methods(C, "__len__")  # 这个魔法函数判断是否有__len__
        return NotImplemented
"""
# ============ Demo2 end =============


"""
抽象基类的两个使用场景：
1. 我们在某些情况下希望判定某个对象的类型
2. 我们需要强制某个子类必须实现某些方法
"""

# =============== Demo2 start =================
# 如何去模拟一个抽象基类
class CacheBase():
    def get(self, key):
        raise NotImplementedError
        
    def set(self, key, value):
        raise NotImplementedError       
        
class RedisCache(CacheBase):
    pass

redis_cache = RedisCache()
redis_cache.set("key", "value")  # 调用时会抛出NotImplementedError异常，因为子类没有实现父类对应方法
# =============== Demo2 end ====================

"""
Demo2 的方法虽实现了第二个场景的需求，但是不够好，
只是在对象方法在调用时才抛出异常，如果想要在对象在
初始化就抛出异常，就需要使用我们的abc模块了。
"""

# ================= Demo3 start ===================
# 使用全局的abc模块
import abc

class CacheBase(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def get(self, key):
        pass
    
    @abc.abstractmethod
    def set(self, key, value):
        raise NotImplementedError
              
class RedisCache(CacheBase):
    pass

redis_cache = RedisCache()  # 初始化时抛出异常
"""
    redis_cache = RedisCache()
TypeError: Can't instantiate abstract class RedisCache with abstract methods get, set
"""
# ================= Demo3 end ======================
"""
抽象基类很容易设计过度，所以不是很推荐
更推荐多继承和鸭子类型
"""
```

## 3.3 使用instance而不是type判断类型

```python
class A:
    pass


class B(A):
    pass


b = B()
print(isinstance(b, B))  # True
print(isinstance(b, A))  # True


print(type(b) is B)  # is 判断是否是同一个对象
print(type(b) == B)  # == 判断的是值是否相等

print(type(b) is A)  # False


"""
注意isinstance比使用type好，type无法找到父类，
而isinstance可以。
同时注意 == 与 is 的区别。
"""
```



## 3.4 类变量和对象变量（实例变量）

```python
# =========== Demo1 start ==============
class A:
    aa = 1  # 类变量
    
    def __init__(self, x, y):
        self.x = x    # self实际指向实例，实例变量
        self.y = y
        

a = A(2, 3)
print(a.x, a.y, a.aa)  # 2 3 1
print(A.aa)  # 1
print(A.x)  # 抛出异常 AttributeError: type object 'A' has no attribute 'x'
# =========== Demo1 end ================


"""
在 Demo1 中打印a.aa时，首先会在对象属性中查找，
若是找不到则在类属性中查找。以上 Demo 很好理解。
"""


# ============ Demo2 start =================
class A:
    aa = 1  # 类变量
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        
a = A(2, 3)
A.aa = 11  # 修改类对象的aa值，实例的aa查找的类对象的aa
print(a.x, a.y, a.aa)  # 2 3 11
A.aa = 111
a.aa = 100  # 赋值给实例的aa，类变量aa的值不变
print(a.x, a.y, a.aa)  # 2 3 100
# ============= Demo2 end ==================


"""
在对A.aa与a.aa同时赋值时，此时，对象属性中
就有了aa属性，所以在打印a.aa时，就会首先打
印对象里的属性啦。注意这个细节哦。类与实例的
变量是两个独立的存在。
"""


# 在Demo3中加入以下代码
b = A(3, 4)
print(b.aa)  # 3 4 111


"""
可见类变量是所有实例共享的。
""
```

## 3.5 类属性和实例属性以及查找顺序

```python
"""
属性就是在类或实例中定义的变量或方法。
"""

class A:
    name = "A"
    def __init__(self):
        self.name = "obj"
        
        
a = A()
print(a.name)  # obj

"""
在单继承这很简单，但是在多继承下，这些就会变得复杂起来。
"""
```

### MRO算法

Method Relation order

Python3使用的算法是C3，以下算法是Python早些版本的属性查找算法，均存在一些缺陷，下面一一介绍。

**深度优先搜索**

![image-20200511211630878](E:\note\慕课网Python高级核心97讲\第三章：Python高级编程-深入类和对象.assets\image-20200511211630878.png)

上图的继承关系中使用深度优先搜索是没有问题的，但是要是继承关系是菱形，如下图所示就会出现问题。需要使用广度优先搜索算法，使得继承顺序为A->B->C->D。

问题就是，下图中，如果C里的方法重写了D的方法。但是由于深度优先搜索算法会首先查找D中的属性，那么C的重写方法就不会生效。所有需要使用广度优先搜索算法解决问题。

![image-20200511211709456](E:\note\慕课网Python高级核心97讲\第三章：Python高级编程-深入类和对象.assets\image-20200511211709456.png)

广度优先**

广度优先虽然解决了上述问题，但是呢，若果出现如下继承关系，广度优先算法又出现问题了。就是，如果D，C都有一个同名的方法，而继承D的B没有实现这个同名方法。那么在搜索完B时，应该搜索D，但是广度优先算法回去搜索C，这逻辑上是不合理的。

![image-20200511211829682](E:\note\慕课网Python高级核心97讲\第三章：Python高级编程-深入类和对象.assets\image-20200511211829682.png)

所以Python3统一成了一种方法，C3使得这些问题都不复存在。

```python
# =============== 菱形继承问题 ==================
#新式类
class D:
    pass


class B(D):
    pass


class C(D):
    pass


class A(B, C):
    pass


print(A.__mro__)  # 属性查找顺序
"""
结果：
(<class '__main__.A'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.D'>, <class 'object'>)
"""


# ================ 非菱形继承问题 =================
class D:
    pass


class B(D):
    pass


class E:
    pass


class C(E):
    pass


class A(B, C):
    pass


print(A.__mro__)  # 属性查找顺序
"""
结果：
(<class '__main__.A'>, <class '__main__.B'>, <class '__main__.D'>, <class '__main__.C'>, <class '__main__.E'>, <class 'object'>)
"""
```

## 3.6 静态方法、类方法以及对象方法以及参数

```python
class Date:

    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def tomorrow(self):
        self.day += 1
    
    @staticmethod
    def parse_from_string(data_str):
        year, month, day = tuple(date_str.split("-"))  # tuple拆包
        return Date(int(year), int(month), int(day))  # 出现硬编码情况   
    
    @classmethod
    def from_string(cls, date_str):
        year, month, day = tuple(date_str.split("-"))
        return cls(int(year), int(month), int(day))  # 解决硬编码，使用cls
    
    def __str__(self):
        return "{year}/{month}/{day}".format(year=self.year, month=self.month, day=self.day)


if __name__ == "__main__":
    new_day = Date(2020, 4, 30)
    new_day.tomorrow()
    print(new_day)
    date_str = "2020-4-30"
    new_day = Date.parse_from_string(date_str)
    print(new_day)
"""
貌似classmethod可以完全替代staticmethod，而且更灵活。其实classmethod也是有用的，比如判断一个字符串是不是一个合法的时间字符串，不需要return一个对象,只需要检查，可见3.7demo
"""
```

## 3.7 数据封装和私有属性

```python
class Date:
    #构造函数
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def tomorrow(self):
        self.day += 1

    @staticmethod
    def parse_from_string(date_str):
        year, month, day = tuple(date_str.split("-"))
        return Date(int(year), int(month), int(day))

    @staticmethod
    def valid_str(date_str):
        year, month, day = tuple(date_str.split("-"))
        if int(year)>0 and (int(month) >0 and int(month)<=12) and (int(day) >0 and int(day)<=31):
            return True
        else:
            return False

    @classmethod
    def from_string(cls, date_str):
        year, month, day = tuple(date_str.split("-"))
        return cls(int(year), int(month), int(day))

    def __str__(self):
        return "{year}/{month}/{day}".format(year=self.year, month=self.month, day=self.day)


class User:
    def __init__(self, birthday):
        self.__birthday = birthday  # _User__birthday
        
    def get_age(self):
        return 2018 - self.__birthday.year
    
    
if __name__ == "__main__":
    user = User(Date(1990, 2, 1))
    print(user._User__birthday)  # 1990/2/1
    print(user.get_age())  # 28
    print(user.birthday)  # AttributeError: User' object has no attribute '__birthday'

"""
python内部将__私有属性加了小技巧，如user._User__birthday可以访问，可以解决同样的属性的继承问题
"""
```



## 3.8 Python对象自省机制

```python
"""
自省就是通过一定的机制查询到对象的内部结构。
"""

class Person:
    name = "User"
    
    
class Student(Person):
    """
    文档
    """
    def __init__(self, school_name):
        self.school_name = school_name
        
        
if __name__ == "__main__":
    stu = Student("家里蹲")
    # 通过__dict__查询属性
    print(stu.__dict__)  # {'school_name': '家里蹲'}
    print(stu.name)  # User
    """
    stu的属性字典里没有name，那么是怎么能够得到User的呢？
    实际上这个name在Person的属性字典里，类也是对象嘛！！
    stu没有，解释器就往上层找
    """
    print(Person.__dict__)  # {'__module__': '__main__', 'name': 'User', ...}
    print(Student.__dict__)  # {... '__doc__': '\n    文档\n    ', ... }
    print(dir(stu))  # ['__class__', '__delattr__', '__dict__', '__dir__', ...]
    
    stu.__dict__["city"] = "BJ"
    print(stu.city)  # BJ
```

## 3.9 super函数

```python
"""
super函数并没有那么简单...
"""
class A:
    def __init__(self):
        print("A")
               
class B(A):
    def __init__(self):
        print("B")
        # super(B, self).__init__()  # python2的用法，python3对super()做了简化
        super().__init__()
        
class C(A):
    def __init__(self):
        print("C")
        super().__init__()
                
class D(B, C):
    def __init__(self):
        print("D")
        super(D, self).__init__()
                
# 既然我们重写了B的构造函数，为什么还要去调用super？
"""
为了能够重用父类的一些方法，避免编写重复的逻辑
"""

# super到底执行顺序什么样？
"""
super并不是仅仅调用父类方法....
"""
if __name__ == "__main__":
    d = D()
    """
    直观结果：        实际结果：
    D                D
    B                B
    A                C
                     A
    """    
    # 所以super的查找顺序是根据mro顺序来的
	print(D.__mro__)
    # (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```



## 3.10 Django rest framework 中对多继承使用的经验

Python支持多继承，却推荐尽量单继承。DRF中大量使用了mixin模式编程技巧，这也是Python推荐使用的模式。

Mixin 即 `Mix-in`，常被译为“混入”，是一种编程模式，在 Python 等面向对象语言中，通常它是实现了某种功能单元的类，用于被其他子类继承，将功能组合到子类中。

利用 Python 的多重继承，子类可以继承不同功能的 Mixin 类，按需动态组合使用。

当多个类都实现了同一种功能时，这时应该考虑将该功能抽离成 Mixin 类。

定义一个简单的类：

```python
class Person:
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age
        
p = Person("小陈", "男", 18)
print(p.name)  # "小陈"  # 我们可以通过调用实例属性的方式来访问
# print(p["name"])  # 抛出异常TypeError: 'Person' object is not subscriptable
```

然后我们定义一个 Mixin 类：

```python
class MappingMixin:
    def __getitem__(self, key):
        return self.__dict__.get(key)

    def __setitem__(self, key, value):
        return self.__dict__.set(key, value)
```

这个类可以让子类拥有像 dict 一样调用属性的功能

我们将这个 Mixin 加入到 Person 类中：

```python
class Person(MappingMixin):
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age
        
p = Person("小陈", "男", 18)    # 现在 Person 拥有另一种调用属性方式了
print(p['name'])  # "小陈"
print(p['age'])  # 18
```

再定义一个 Mixin 类，这个类实现了 `__repr__` 方法，能自动将属性与值拼接成字符串：

```python
class ReprMixin:
    def __repr__(self):
        s = self.__class__.__name__ + '('
        for k, v in self.__dict__.items():
            if not k.startswith('_'):
                s += '{}={}, '.format(k, v)
        s = s.rstrip(', ') + ')'  # 将最后一个逗号和空格换成括号
        return s


# 利用 Python 的特性，一个类可以继承多个父类：
class Person(MappingMixin, ReprMixin):
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age


# 这样这个子类混入了两种功能：
p = Person("小陈", "男", 18)
print(p['name'])  # "小陈"
print(p)  # Person(name=小陈, gender=男, age=18)
```

Mixin 实质上是利用语言特性，可以把它看作一种特殊的多重继承，所以它并不是 Python 独享，只要支持多重继承或者类似特性的都可以使用，比如 Ruby 中 include 语法，Vue 等前端领域也有 Mixin 的概念。

但 Mixin 终归不属于语言的语法，为了代码的可读性和可维护性，定义和使用 Mixin 类应该遵循几个原则：

1. Mixin 实现的功能需要是通用的，并且是单一的，比如上例中两个 Mixin 类都适用于大部分子类，每个 Mixin 只实现一种功能，可按需继承。
2. Mixin 只用于拓展子类的功能，不能影响子类的主要功能，子类也不能依赖 Mixin。比如上例中 `Person` 继承不同的 Mixin 只是增加了一些功能，并不影响自身的主要功能。如果是依赖关系，则是真正的基类，不应该用 Mixin 命名。
3. Mixin 类自身不能进行实例化，仅用于被子类继承。

## 3.11 Python中的with语句

```python
"""
try expect finally 的用法
"""

# ============== Demo1 start ====================
try:
    print("code started")
	raise KeyError
except KeyError as e:
    print("key error")
else:  # 没有异常再执行
    print("other code")
finally:
    print("finally")  # 不管怎么样该行代码都会运行，用于关闭文件对象等
# ============== Demo1 end =====================


# ================== Demo2 start ========================
def exe_try():
    try:
        print("code start")
        raise KeyError
        return 1
    except KeyError as e:
        print("Key error")
        return 2
    else:
        print("other error")
        return 3
    finally:
        print("finally")
        return 4
    
    
if __name__ == "__main__":
    result = exe_try()
    print(result)
    
"""
result 的结果会是什么呢？
答案是： 4
那么注释 return 4
结果又是什么呢？
答案是： 2

因为每次执行到return语句时，
其值都会压入栈中，最终取栈顶的值。
"""
# ================== Demo2 end ==========================
```

**上下文管理协议**

```python
"""
基于：
__enter__(self)
__exit__(self, exc_type, exc_val, exc_tb)
"""


class Sample:
    def __enter__(self):
        # 获取资源
        print("enter")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # 释放资源
        print("exit")
        
	def do_something(self):
        print("doing something")
        
        
with Sample() as sample:
    sample.do_something()
    
    
"""
执行结果：
enter
doing something
exit
"""
```



## 3.12 contextlib（简化）实现上下文管理器

```python
Copyimport contextlib

# 这个装饰器把简单的生成器函数编程上下文管理器，这样就不用创建类去实现管理器协议了。
@contextlib.contextmanager
def file_open(file_name):
    print("file open")
    yield {}
    print("file end")
    
    
with file_open("bobby.txt") as f_opened:
    print("file processing")
    
    
"""
执行结果：
file open
file processing
file end
"""
```

