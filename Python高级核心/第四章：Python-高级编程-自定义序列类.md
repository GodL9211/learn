# 第四章：Python-高级编程-自定义序列类



## 4.1 Python中的序列分类

![image-20200513202024752](E:\note\慕课网Python高级核心97讲\第四章：自定义序列类.assets\image-20200513202024752.png)

### 4.1.1 容器序列

```python
"""
list tuple deque 可以放入任意类型的数据
"""
```

### 4.1.2 扁平序列

```python
"""
str bytes bytearray array.array
注意array与list的区别，array存放数据类型需一致,需指明存放什么类型。
"""
```

### 4.1.3 可变序列

```python
"""
list deque bytearry array
"""
```

### 4.1.4 不可变序列

```python
"""
str tuple bytes
"""
```

## 4.2 Python中序列类型的abc继承关系

![image-20200513204025127](E:\note\慕课网Python高级核心97讲\第四章：Python-高级编程-自定义序列类.assets\image-20200513204025127.png)

![image-20200513204123386](E:\note\慕课网Python高级核心97讲\第四章：Python-高级编程-自定义序列类.assets\image-20200513204123386.png)

```python
"""
需要知道的是，在Python中，其跟容器相关的数据结构
的抽象基类是放在collection.abc模块下的
"""

"""
可变序列类型主要使用了
__setitem__
__delitem__
等魔法函数
"""
# collection.abc

__all__ = ["Awaitable", "Coroutine",
           "AsyncIterable", "AsyncIterator", "AsyncGenerator",
           "Hashable", "Iterable", "Iterator", "Generator", "Reversible",
           "Sized", "Container", "Callable", "Collection",
           "Set", "MutableSet",
           "Mapping", "MutableMapping",
           "MappingView", "KeysView", "ItemsView", "ValuesView",
           "Sequence", "MutableSequence",
           "ByteString",
           ]


class Collection(Sized, Iterable, Container):

    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Collection:
            return _check_methods(C,  "__len__", "__iter__", "__contains__")
        return NotImplemented

    
class Reversible(Iterable):

    __slots__ = ()

    @abstractmethod
    def __reversed__(self):
        while False:
            yield None

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Reversible:
            return _check_methods(C, "__reversed__", "__iter__")
        return NotImplemented
    
    
class Sequence(Reversible, Collection):

    """All the operations on a read-only sequence.

    Concrete subclasses must override __new__ or __init__,
    __getitem__, and __len__.
    """

    __slots__ = ()

    @abstractmethod
    def __getitem__(self, index):
        raise IndexError

    def __iter__(self):
        i = 0
        try:
            while True:
                v = self[i]
                yield v
                i += 1
        except IndexError:
            return

    def __contains__(self, value):
        for v in self:
            if v is value or v == value:
                return True
        return False

    def __reversed__(self):
        for i in reversed(range(len(self))):
            yield self[i]

    def index(self, value, start=0, stop=None):
        '''S.index(value, [start, [stop]]) -> integer -- return first index of value.
           Raises ValueError if the value is not present.

           Supporting start and stop arguments is optional, but
           recommended.
        '''
        if start is not None and start < 0:
            start = max(len(self) + start, 0)
        if stop is not None and stop < 0:
            stop += len(self)

        i = start
        while stop is None or i < stop:
            try:
                v = self[i]
                if v is value or v == value:
                    return i
            except IndexError:
                break
            i += 1
        raise ValueError

    def count(self, value):
        'S.count(value) -> integer -- return number of occurrences of value'
        return sum(1 for v in self if v is value or v == value)
 
 # 可变序列    
 class MutableSequence(Sequence):

    __slots__ = ()

    """All the operations on a read-write sequence.

    Concrete subclasses must provide __new__ or __init__,
    __getitem__, __setitem__, __delitem__, __len__, and insert().

    """

    @abstractmethod
    def __setitem__(self, index, value):
        raise IndexError

    @abstractmethod
    def __delitem__(self, index):
        raise IndexError

    @abstractmethod
    def insert(self, index, value):
        'S.insert(index, value) -- insert value before index'
        raise IndexError

    def append(self, value):
        'S.append(value) -- append value to the end of the sequence'
        self.insert(len(self), value)

    def clear(self):
        'S.clear() -> None -- remove all items from S'
        try:
            while True:
                self.pop()
        except IndexError:
            pass

    def reverse(self):
        'S.reverse() -- reverse *IN PLACE*'
        n = len(self)
        for i in range(n//2):
            self[i], self[n-i-1] = self[n-i-1], self[i]

    def extend(self, values):
        'S.extend(iterable) -- extend sequence by appending elements from the iterable'
        for v in values:
            self.append(v)

    def pop(self, index=-1):
        '''S.pop([index]) -> item -- remove and return item at index (default last).
           Raise IndexError if list is empty or index is out of range.
        '''
        v = self[index]
        del self[index]
        return v

    def remove(self, value):
        '''S.remove(value) -- remove first occurrence of value.
           Raise ValueError if the value is not present.
        '''
        del self[self.index(value)]

    def __iadd__(self, values):
        self.extend(values)
        return self   
```

## 4.3 extend方法和+、+=的区别

+只能是同一类型（如列表），+=就地加,不产生新序列，且参数可以为任意的序列类型.是通过魔法函数__iadd__实现的，extend也可以添加任意序列类型

```python
a = [1, 2]
c = a + [3, 4]
print(c)

a += [3, 4]
print(a)
a += (5, 6)  # 不报错，+=就地加
print(a)
c = a + (7, 8)  # 报错

"""
为什么会有这种差别，
实际上在 += 时，Python
实现的魔法函数是 __iadd__
，调用这个魔法函数实际就是把
+= 右边的值传入 list 的 extend方法。
"""

"""
注意append的方法与extend的方法
append会将参数作为整个。extend会for循环将
参数分开。extend()没有返回值。
"""
```

![image-20200513204748160](E:\note\慕课网Python高级核心97讲\第四章：Python-高级编程-自定义序列类.assets\image-20200513204748160.png)

## 4.4 实现可切片的对象

```python
#模式[start:end:step]
# 切片返回的新的列表
"""
    其中，第一个数字start表示切片开始位置，默认为0；
    第二个数字end表示切片截止（但不包含）位置（默认为列表长度）；
    第三个数字step表示切片的步长（默认为1）。
    当start为0时可以省略，当end为列表长度时可以省略，
    当step为1时可以省略，并且省略步长时可以同时省略最后一个冒号。
    另外，当step为负整数时，表示反向切片，这时start应该比end的值要大才行。
"""
## 取值操作
aList = [3, 4, 5, 6, 7, 9, 11, 13, 15, 17]
print (aList[::])  # 返回包含原列表中所有元素的新列表
print (aList[::-1])  # 返回包含原列表中所有元素的逆序列表
print (aList[::2])  # 隔一个取一个，获取偶数位置的元素
print (aList[1::2])  # 隔一个取一个，获取奇数位置的元素
print (aList[3:6])  # 指定切片的开始和结束位置
aList[0:100]  # 切片结束位置大于列表长度时，从列表尾部截断
aList[100:]  # 切片开始位置大于列表长度时，返回空列表

## 赋值操作
aList[len(aList):] = [9]  # 在列表尾部增加元素
aList[:0] = [1, 2]  # 在列表头部插入元素
aList[3:3] = [4]  # 在列表中间位置插入元素
aList[:3] = [1, 2]  # 替换列表元素，等号两边的列表长度相等
aList[3:] = [4, 5, 6]  # 等号两边的列表长度也可以不相等
aList[::2] = [0] * 3  # 隔一个修改一个
print (aList)
aList[::2] = ['a', 'b', 'c']  # 隔一个修改一个
aList[::2] = [1,2]  # 左侧切片不连续，等号两边列表长度必须相等
aList[:3] = []  # 删除列表中前3个元素

del aList[:3]  # 切片元素连续
del aList[::2]  # 切片元素不连续，隔一个删一个
```

```python
"""
编写支持切片的对象  
"""
import numbers
class Group:
    #支持切片操作
    def __init__(self, group_name, company_name, staffs):
        self.group_name = group_name
        self.company_name = company_name
        self.staffs = staffs

    def __reversed__(self):
        self.staffs.reverse()

    def __getitem__(self, item):    # 可切片的关键
        cls = type(self)
        print(cls)
        if isinstance(item, slice):
            return cls(group_name=self.group_name, company_name=self.company_name, staffs=self.staffs[item])
        elif isinstance(item, numbers.Integral):
            return cls(group_name=self.group_name, company_name=self.company_name, staffs=[self.staffs[item]])

    def __len__(self):
        return len(self.staffs)

    def __iter__(self):
        return iter(self.staffs)

    def __contains__(self, item):
        if item in self.staffs:
            return True
        else:
            return False

staffs = ["bobby1", "imooc", "bobby2", "bobby3"]
group = Group(company_name="imooc", group_name="user", staffs=staffs)
reversed(group)
print(list(group[:]))
print(group[2].staffs)
#调用__contains_
print('1' in group)
#调用__len__
print(len(group))
#调用__iter__
for user in group:
    print(user)
    
"""
django的queryset()可以切片，典型的实现了__getitem__(self, item)
"""
```

## 4.5 bisect管理可排序序列

作用：用来处理已排序的序列，用来维持已排序的序列，采用二分查找，性能非常高，推荐

![image-20200513224811723](E:\note\慕课网Python高级核心97讲\第四章：Python-高级编程-自定义序列类.assets\image-20200513224811723.png)

```python
# 默认插入右边，如插入两个3，则第二个在第一个的右边，可以查看插入的位置（左右）
import bisect

my_list = []
bisect.insort(my_list, 1)
bisect.insort(my_list, 2)
bisect.insort(my_list, 3)
bisect.insort(my_list, 4)
bisect.insort(my_list, 5)
bisect.insort(my_list, 6)
print(my_list)
# 查看插入的位置，默认从右数
print(bisect.bisect(my_list, 3))
#从左边数
print(bisect.bisect_left(my_list, 3))
print(my_list)

"""
[1, 2, 3, 4, 5, 6]
3
2
"""
```



## 4.6 什么时候我们不该使用列表

array: 性能比list高很多，但是array只能存放指定类型的数据（要求性能，且类型固定时可以使用）

![image-20200513224911389](E:\note\慕课网Python高级核心97讲\第四章：Python-高级编程-自定义序列类.assets\image-20200513224911389.png)

deque: 双端队列

```python
# array, deque

import array
# array和list的一个重要区别，array只能存放指定的类型
my_array = array.array("i")
my_array.append(1)
my_array.append("abc")
```

## 4.7 列表推导式、生成器表达式、字典推导式

```python
# 列表生成式（列表推导式）
# 提取出1-20之间的奇数

odd_list = []
for i in range(21):
    if i%2 == 1:
        odd_list.append(i)
        
odd_list = [i for i in range(21) if i%2 == 1]


# 逻辑复杂的情况
def handle_item(item):
    return item * item


odd_list = [handle_item(i) for i in range(21) if i%2 == 1]

# 列表生成式性能比列表操作高


# 生成器表达式
odd_gen = (i for i in range(21) if i%2 == 1)
print(type(odd_list))


# 字典推导式
my_dict = {"bobby1":22, "bobby2":23, "imooc.com":5}
reversed_dict = {value:key for key, value in my_dict.items()}


# 集合推导式
my_set = {key for key, value in my_dict.items()}
print(type(my_set))

my_set = set(my_dict.keys())  # 不够灵活
```