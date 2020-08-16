# 第六章：Python高级编程-对象引用、可变性和垃圾回收

## 6.1 Python中的变量是什么

在示例所示的交互式控制台中，无法使用“变量是盒子”做解释。下图说明了在 Python 中为什么不能使用盒子比喻，而便利贴则指出了变量的正确工作方式。

　  变量 a 和 b 引用同一个列表，而不是那个列表的副本

```python
python和java中的变量本质不一样，python的变量实质上是一个指针 int str， 便利贴

a = 1
a = "abc"
#1. a贴在1上面
#2. 先生成对象 然后贴便利贴

a = [1,2,3]
b = a
print (id(a), id(b))
print (a is b)
# b.append(4)
# print (a)
```

![image-20200518203620784](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200518203620784.png)

如果把变量想象为盒子，那么无法解释 Python 中的赋值；应该把变量视作便利贴，这样示例中的行为就好解释了

 

 **注意：**

　　对引用式变量来说，说把变量分配给对象更合理，反过来说就有问题。毕竟，对象在赋值之前就创建了

## 6.2 ==和is的区别

```python
a = [1,2,3,4]
b = [1,2,3,4]

print(a is b)
print(a == b)


# 对于比较小的Python不会重新创建，小整数
a = 1
b = 1
print(id(a), id(b))
print(a == b)
print(a is b)


class People:
    pass

person = People()  # 类是全局唯一的
if type(person) is People:
    print ("yes")
```

***标识、相等性和别名***

　　Lewis Carroll 是 Charles Lutwidge Dodgson 教授的笔名。Carroll 先生指的就是 Dodgson 教授，二者是同一个人。🌰用 Python 表达了这个概念。

charles 和 lewis 指代同一个对象

```python
>>> charles = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 900}
>>> lewis = charles
>>> lewis is charles
True
>>> id(lewis), id(charles)
(4303312648, 4303312648)
>>> lewis['balance'] = 950
>>> charles
{'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}
```

　　然而，假如有冒充者（姑且叫他 Alexander Pedachenko 博士）生于 1832年，声称他是 Charles L. Dodgson。这个冒充者的证件可能一样，但是Pedachenko 博士不是 Dodgson 教授。这种情况如图

 ![img](E:\note\慕课网Python高级核心97讲\Untitled.assets\995184-20170820155045850-380872550.png)

​                                charles 和 lewis 绑定同一个对象，alex 绑定另一个具有相同内容的对象

alex 与 charles 比较的结果是相等，但 alex 不是charles

```python
>>> lewis
{'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}
>>> alex = {'name': 'Charles L. Dodgson', 'born': 1832, 'balance': 950}
>>> lewis == alex
True
>>> alex is not lewis
True
```

　　alex 指代的对象与赋值给 lewis 的对象内容一样，比较两个对象，结果相等，这是因为 dict 类的 __eq__ 方法就是这样实现的，但它们是不同的对象。这是 Python 说明标识不同的方式：a is notb。

　　示例体现了别名。在那段代码中，lewis 和 charles 是别名，即两个变量绑定同一个对象。而 alex 不是 charles 的别名，因为二者绑定的是不同的对象。alex 和 charles 绑定的对象具有相同的值（== 比较的就是值），但是它们的标识不同。



**在==和is之间选择**

　　== 运算符比较两个对象的值（对象中保存的数据），而 is 比较对象的标识。通常，我们关注的是值，而不是标识，因此 Python 代码中 == 出现的频率比 is 高。然而，在变量和单例值之间比较时，应该使用 is。目前，最常使用 is检查变量绑定的值是不是 None。下面是推荐的写法：

```python
x is None
```

否定的写法

```python
x is not None
```

***元组的相对不可变性***

　　元组与多数 Python 集合（列表、字典、集，等等）一样，保存的是对象的引用。 如果引用的元素是可变的，即便元组本身不可变，元素依然可变。也就是说，元组的不可变性其实是指 tuple 数据结构的物理内容（即保存的引用）不可变，与引用的对象无关。 

```python
>>> t1 = (1, 2, [30, 40])
>>> t2 = (1, 2, [30, 40])
>>> t1 == t2
True
>>> id(t1[-1])
4316861320
>>> t1[-1].append(1000)
>>> t1
(1, 2, [30, 40, 1000])
>>> t1 == t2
False
```

 🌰表明，元组的值会随着引用的可变对象的变化而变。元组中不可变的是元素的标识。

 

***默认做浅复制***

　　复制列表（或多数内置的可变集合）最简单的方式是使用内置的类型构造方法。例如：

```python
>>> l1 = [3, [55, 44], (7, 8, 9)]
>>> l2 = list(l1)
>>> l3 = l1[:]
>>> l2
[3, [55, 44], (7, 8, 9)]
>>> l3
[3, [55, 44], (7, 8, 9)]
>>> l1 == l2 == l3
True
>>> l2 is l1
False
>>> l3 is l1
False
```

为一个包含另一个列表的列表做浅复制；把这段代码复制粘贴到 Python Tutor ([http://www.pythontutor.com](http://www.pythontutor.com/))网站中，看看动画效果

```python
l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1)               #浅复制了l1
l1.append(100)              #l1列表在尾部添加数值100
l1[1].remove(55)            #移除列表中第1个索引的值
print('l1:', l1)
print('l2:', l2)
l2[1] += [33, 22]           #l2列表中第1个索引做列表拼接
l2[2] += (10, 11)           #l2列表中的第2个索引做元祖拼接
print('l1:', l1)
print('l2:', l2)
```

l2 是 l1 的浅复制副本

![img](E:\note\慕课网Python高级核心97讲\Untitled.assets\995184-20170820164201678-1436095273.png)

***为任意对象做深复制和浅复制*** 

　　浅复制没什么问题，但有时我们需要的是深复制（即副本不共享内部对象的引用）。copy 模块提供的 deepcopy 和 copy 函数能为任意对象做深复制和浅复制。

🌰 校车乘客在途中上车和下车

```python
 1 class Bus:
 2 
 3     def __init__(self, passengers=None):
 4         if passengers is None:
 5             self.passengers = []
 6         else:
 7             self.passengers = list(passengers)
 8 
 9     def pick(self, name):
10         self.passengers.append(name)
11 
12     def drop(self, name):
13         self.passengers.remove(name)
```

我们将创建一个 Bus 实例（bus1）和两个副本，一个是浅复制副本（bus2），另一个是深复制副本（bus3），看看在 bus1 有学生下车后会发生什么。

```python
 1 from copy import copy, deepcopy
 2 
 3 bus1 = Bus(['Alice', 'Bill', 'Claire', 'David'])
 4 bus2 = copy(bus1)                       #bus2浅复制的bus1
 5 bus3 = deepcopy(bus1)                   #bus3深复制了bus1
 6 print(id(bus1), id(bus2), id(bus3))     #查看三个对象的内存地址
 7 
 8 bus1.drop('Bill')                       #bus1的车上Bill下车了
 9 print('bus2:', bus2.passengers)         #wtf....bus2中的Bill也没有了，见鬼了！
10 print(id(bus1.passengers), id(bus2.passengers), id(bus3.passengers))    #审查 passengers 属性后发现，bus1和bus2共享同一个列表对象，因为 bus2 是 bus1 的浅复制副本
11 
12 print('bus3:', bus3.passengers)         #bus3是bus1 的深复制副本，因此它的 passengers 属性指代另一个列表
```

以上代码执行的结果为：

```python
4324829840 4324830176 4324830736
bus2: ['Alice', 'Claire', 'David']
4324861256 4324861256 4324849608
bus3: ['Alice', 'Bill', 'Claire', 'David']
```

循环引用：b 引用 a，然后追加到 a 中；deepcopy 会想办法复制 a

```python
>>> a = [10, 20]
>>> b = [a, 30]
>>> a.append(b)
>>> a
[10, 20, [[...], 30]]
>>> from copy import deepcopy
>>> c = deepcopy(a)
>>> c
[10, 20, [[...], 30]]
```



***函数的参数作为引用时***

 　Python 唯一支持的参数传递模式是共享传参（call by sharing）。多数面向对象语言都采用这一模式，包括 Ruby、Smalltalk 和 Java（Java 的引用类型是这样，基本类型按值传参）。共享传参指函数的各个形式参数获得实参中各个引用的副本。也就是说，函数内部的形参是实参的别名。

函数可能会修改接收到的任何可变对象

```python
>>> def f(a, b):
...     a += b
...     return a
... 
>>> x = 1
>>> y = 2
>>> f(x, y)
3
>>> x, y
(1, 2)
>>> a = [1, 2]
>>> b = [3, 4]
>>> f(a, b)
[1, 2, 3, 4]
>>> a, b
([1, 2, 3, 4], [3, 4])
>>> t = (10, 20)
>>> u = (30, 40)
>>> f(t, u)
(10, 20, 30, 40)
>>> t, u
((10, 20), (30, 40))
```

数字x没有变化，列表a变了，元祖t没变化

***不要使用可变类型作为参数的默认值***

　　可选参数可以有默认值，这是 Python 函数定义的一个很棒的特性，这样我们的 API 在进化的同时能保证向后兼容。然而，我们应该避免使用可变的对象作为参数的默认值。

一个简单的类，说明可变默认值的危险

```python
 1 class HauntedBus:
 2     '''
 3     备受折磨的幽灵车
 4     '''
 5 
 6     def __init__(self, passengers=[]):
 7         self.passengers = passengers
 8 
 9     def pick(self, name):
10         self.passengers.append(name)
11 
12     def drop(self, name):
13         self.passengers.remove(name)
14 
15 
16 bus1 = HauntedBus(['Alice', 'Bill'])
17 print('bus1上的乘客：', bus1.passengers)
18 bus1.pick('Charlie')            #bus1上来一名乘客Charile
19 bus1.drop('Alice')              #bus1下去一名乘客Alice
20 print('bus1上的乘客：', bus1.passengers)          #打印bus1上的乘客
21 
22 bus2 = HauntedBus()             #实例化bus2
23 bus2.pick('Carrie')             #bus2上来一名课程Carrie
24 print('bus2上的乘客：', bus2.passengers)
25 
26 bus3 = HauntedBus()
27 print('bus3上的乘客：', bus3.passengers)
28 bus3.pick('Dave')
29 print('bus2上的乘客：', bus2.passengers)        #登录到bus3上的乘客Dava跑到了bus2上面
30 
31 print('bus2是否为bus3的对象：', bus2.passengers is bus3.passengers)
32 print('bus1上的乘客：', bus1.passengers)
```

以上代码执行的结果为：

```python
bus1上的乘客： ['Alice', 'Bill']
bus1上的乘客： ['Bill', 'Charlie']
bus2上的乘客： ['Carrie']
bus3上的乘客： ['Carrie']
bus2上的乘客： ['Carrie', 'Dave']
bus2是否为bus3的对象： True
bus1上的乘客： ['Bill', 'Charlie']
```

　　实例化 HauntedBus 时，如果传入乘客，会按预期运作。但是不为 HauntedBus 指定乘客的话，奇怪的事就发生了，这是因为 self.passengers 变成了 passengers 参数默认值的别名。出现这个问题的根源是，默认值在定义函数时计算（通常在加载模块时），因此默认值变成了函数对象的属性。因此，如果默认值是可变对象，而且修改了它的值，那么后续的函数调用都会受到影响。

 ***防御可变参数***

　　如果定义的函数接收可变参数，应该谨慎考虑调用方是否期望修改传入的参数。

　　例如，如果函数接收一个字典，而且在处理的过程中要修改它，那么这个副作用要不要体现到函数外部？具体情况具体分析。这其实需要函数的编写者和调用方达成共识。

　　TwilightBus 实例与客户共享乘客列表，这会产生意料之外的结果。在分析实现之前，我们先从客户的角度看看 TwilightBus 类是如何工作的。

从 TwilightBus 下车后，乘客消失了

```python
 1 class TwilightBus:
 2     """让乘客销声匿迹的校车"""
 3 
 4     def __init__(self, passengers=None):
 5         if passengers is None:
 6             self.passengers = passengers
 7         else:
 8             self.passengers = passengers    #这个地方就需要注意了,这里传递的是引用的别名
 9 
10     def pick(self, name):
11         self.passengers.append(name)        #会修改构造放的列表，也就是会修改外部的数据
12 
13     def drop(self, name):
14         self.passengers.remove(name)        #会修改构造放的列表，也就是会修改外部的数据
15 
16 basketball_team = ['Sue', 'Tina', 'Maya', 'Diana', 'Pat']
17 bus = TwilightBus(basketball_team)
18 bus.drop('Tina')        #bus中乘客Tina下去了
19 bus.drop('Pat')         #bus中课程Pat下去了
20 
21 print(basketball_team)  #wtf....为毛线的basketball的里面这两个人也木有了~~MMP
```

以上代码执行的结果为： 

```python
['Sue', 'Maya', 'Diana']
```

解决方案，不直接引用外部的basketball_team，而是在内部创建一个副本，类似于下面的这种 🌰

```python
>>> a = [1, 2, 3]
>>> b = a
>>> c = list(a)
>>> b.append(10)
>>> a
[1, 2, 3, 10]
>>> b
[1, 2, 3, 10]
>>> c
[1, 2, 3]
```

c是a的副本，不会因为本身列表的变化而受影响，在上面的 🌰 中，只需要在构造函数中创建一个副本即可(self.passengers=list(passengers))

## 6.3 del语句与垃圾回收

```python
#cpython中垃圾回收的算法是采用 引用计数
a = object()
b = a
del a
print(b)  # 有结果
print(a)  # 报错
class A:
    def __del__(self):  # del是Python会执行这个函数的逻辑
        pass
```

　　del 语句删除名称，而不是对象。del 命令可能会导致对象被当作垃圾回收，但是仅当删除的变量保存的是对象的最后一个引用，或者无法得到对象时。 重新绑定也可能会导致对象的引用数量归零，导致对象被销毁。

```python
>>> import weakref
>>> s1 = {1, 2, 3}　　　　　　　　　　　　　　　　
>>> s2 = s1　　　　　　　　　　　　　　　　　　　　　#s1和s2是别名，指向同一个集合
>>> def bye():　　　　　　　　　　　　　　　　　　　#这个函数一定不能是要销毁的对象的绑定方法，否则会有一个指向对象的引用
...     print('Gone with the wind...')　　　　
... 
>>> ender = weakref.finalize(s1, bye)　　　　　#在s1引用的对象上注册bye回调　　　　　
>>> ender.alive　　　　　　　　　　　　　　　　　　#调用finalize对象之前，.alive属性的值为True
True
>>> del s1　　　　　　　　　　　　　　　　　　　　　#del不删除对象，而是删除对象的引用
>>> ender.alive
True
>>> s2 = 'spam'　　　　　　　　　　　　　　　　　 #重新绑定最后一个引用s2，让{1, 2, 3}无法获取，对象呗销毁了，调用bye回调，ender.alive的值编程了False
Gone with the wind...
>>> ender.alive
False
```

 

***弱引用***

　　正是因为有引用，对象才会在内存中存在。当对象的引用数量归零后，垃圾回收程序会把对象销毁。但是，有时需要引用对象，而不让对象存在的时间超过所需时间。这经常用在缓存中。

　　弱引用不会增加对象的引用数量。引用的目标对象称为所指对象（referent）。因此我们说，弱引用不会妨碍所指对象被当作垃圾回收。

 弱引用是可调用的对象，返回的是被引用的对象；如果所指对象不存在了，返回 None

```python
>>> import weakref
>>> a_set = {0, 1}　　　　
>>> wref = weakref.ref(a_set)　　　　　　　　　　　　　　　　　　#创建弱引用对象wref，下一行审查它
>>> wref
<weakref at 0x101ce03b8; to 'set' at 0x101cd8d68>
>>> wref()　　　　　　　　　　　　　　　　　　　　　　　　　　　　　#调用wref()返回的是被引用的对象，{0, 1}。因为这是控制台会话，所以{0, 1}会绑定给_变量
{0, 1}
>>> a_set = {2, 3, 4}　　　　　　　　　　　　　　　　　　　　　　 #a_set不在指代{0， 1}集合，因此集合的引用数量减少了，但是_变量仍然指代它
>>> wref()　　　　　　　　　　　　　　　　　　　　　　　　　　　　  #调用wref()已经返回了{0， 1}
{0, 1}
>>> wref() is None　　　　　　　　　　　　　　　　　　　　　　　　#计算这个表达式时，{0， 1}存在，因此wref()不是None，但是，随后_绑定到结果值False，现在{0，1}没有强引用
False
>>> wref() is None　　　　　　　　　　　　　　　　　　　　　　　　#因为{0， 1}对象不存在了，所以wref()返回了None
True
```

## 6.4 一个经典的参数错误

```python
def add(a, b):
    a += b
    return a

class Company:
    def __init__(self, name, staffs=[]):
        self.name = name
        self.staffs = staffs
    def add(self, staff_name):
        self.staffs.append(staff_name)
    def remove(self, staff_name):
        self.staffs.remove(staff_name)

if __name__ == "__main__":
    com1 = Company("com1", ["bobby1", "bobby2"])
    com1.add("bobby3")
    com1.remove("bobby1")
    print (com1.staffs)

    com2 = Company("com2")
    com2.add("bobby")
    print(com2.staffs)

    print (Company.__init__.__defaults__)  # 查看默认值

    com3 = Company("com3")
    com3.add("bobby5")
    print (com2.staffs)
    print (com3.staffs)
    print (com2.staffs is com3.staffs)  # 没有传入，使用默认的值，所以共用了

    a = 1
    b = 2
    
    e = [1,2]  # a是可变的哦
    f = [3,4]
    
    g = (1, 2)
    h = (3, 4)
    
    i = add(a, b)
    j = add(e, f)
    k = add(g, h)
    
    print(i)
    print(a, b)
    print("***"* 5)
    print(j)
    print(e, f)
    print("***"* 5)
    print(k)
    print(g, h)
    
"""
['bobby2', 'bobby3']
['bobby']
(['bobby'],)
['bobby', 'bobby5']
['bobby', 'bobby5']
True
3
1 2
***************
[1, 2, 3, 4]
[1, 2, 3, 4] [3, 4]
***************
(1, 2, 3, 4)
(1, 2) (3, 4)
"""      
```