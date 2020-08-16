

## 7.1 property动态属性

在面向对象编程中，我们一般把名词性的东西映射成属性，动词性的东西映射成方法。在python类中他们对应的分别是属性`self.xxx`和类方法。但有时我们需要的属性需要根据其他属性动态的计算，此时如果直接使用属性方法处理，会导致数据不同步。下面介绍`@property`方法来动态创建类属性。

```python
from datetime import date, datetime

class User:
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday
        self._age = 0
        
    def get_age(self):
        return datetime.now().year - self.birthday.year
    
    
    @property
    def age(self):
        return datetime.now().year - self.birthday.year
    
    
    @age.setter
    def age(self, value):
        self._age = value
        
if __name__ == "__main__":
    user = User("bobby", date(year=1987, month=1, day=1))
    print(user.get_age())
    user.age = 30
    print(user._age)
    print(user.age)
    
"""
33
30
33
"""
```

## 7.2   **``__getattr__``**、**``__getattribute__``**魔法函数

- **``object.__getattr__(self, name)`` **
  找不到attribute的时候，会调用getattr，返回一个值或AttributeError异常。 

  ```python
  #__getattr__, __getattribute__
  #__getattr__ 就是在查找不到属性的时候调用
  from datetime import date
  class User:
      def __init__(self,info={}):
          self.info = info
  
      def __getattr__(self, item):  # 查找不到属性的时候调用
          return self.info[item]
  
  if __name__ == "__main__":
      user = User(info={"company_name":"imooc", "name":"bobby"})
      print(user.name)    # __getattr__魔法函数的好处
      print(user.test)
  ```

  ![image-20200519223312288](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200519223312288.png)

- **``object.__getattribute__(self, name) ``**
  无条件被调用，通过实例访问属性首先就会调用。如果class中定义了``__getattr__()``，则``__getattr__()``不会被调用（除非显示调用或引发AttributeError异常）

```python
from datetime import date
class User:
    def __init__(self,info={}):
        self.info = info

    def __getattr__(self, item):  # 查找不到属性的时候调用
        return self.info[item]

    def __getattribute__(self, item):  # 查找属性时调用
        return "bobby"

if __name__ == "__main__":
    user = User(info={"company_name":"imooc", "name":"bobby"})
    print(user.name)
    print(user.test)
```

![image-20200519223403969](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200519223403969.png)

``object.__getattribute__(self, name) ``把持了所有属性访问的入口，能不重写就尽量不去覆盖他，因为一旦写不好会使整个类的属性访问给蹦掉。写框架的时候是极有可能用到这个方法的，因为某些时候会去控制整个类的实例的过程，以及类属性访问的过程。

## 7.3 属性描述符和属性查找过程

```python
#属性描述符

import numbers

#只要一个类实现了下面三种魔法函数中的一种，这个类就是属性描述符
class IntField:
    # 数据描述符
    def __get__(self, instance, owner):
        return self.value
    def __set__(self, instance, value):
        if not isinstance(value,numbers.Integral):
            raise ValueError("必须为int")
        if value < 0:
            raise ValueError("positive value need")
        self.value = value   # 把值保存再实例中
    def __delete__(self, instance):
        pass

class NonDataIntField:
    #只实现__get__方法，属性描述符，非数据属性描述符
    def __get__(self, instance, owner):
        return self.value

class User:
    age = IntField()
     # age = NonDataIntField()

if __name__ == '__main__':
    user = User()
    user.age = 24
    print(user.age)
    print(user.__dict__)
    # user.age = '24'  # 这会报错

'''
如果user是某个类的实例，那么user.age（以及等价的getattr(user,’age’)）
首先调用__getattribute__。如果类定义了__getattr__方法，
那么在__getattribute__抛出 AttributeError 的时候就会调用到__getattr__，
而对于描述符(__get__）的调用，则是发生在__getattribute__内部的。
user = User(), 那么user.age 顺序如下：

（1）数据描述符：如果“age”是出现在User或其基类的__dict__中， 且age是data descriptor（数据描述符）， 那么调用其__get__方法, 否则

（2）实例：如果“age”出现在user（实例）的__dict__中， 那么直接返回 obj.__dict__[‘age’]， 否则

（3）类： 如果“age”出现在User（类）或其基类的__dict__中

（3.1）非数据属性描述符：如果age是non-data descriptor，那么调用其__get__方法， 否则(比如age=1)

（3.2）返回 __dict__[‘age’]

（4）如果User有__getattr__方法，调用__getattr__方法，否则

（5）抛出AttributeError

'''
```

示例1：

![image-20200519231522159](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200519231522159.png)

示例2：

![image-20200519231652102](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200519231652102.png)

示例3：

![image-20200519232051158](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200519232051158.png)

示例4：

![image-20200519232231001](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200519232231001.png)

## 7.4 __new__和__init__的区别

- 我们通常把``__init__``称为构造函数。其实，用于构建实例的方法是特殊方法``__new__``：这是个类方法（使用特殊方式处理，因此不必使用@classmethod装饰器），必须返回一个实例。返回的实例会作为第一个参数（即self）传给``__init__``方法。因为调用``__init__``方法时要传入实例，而且禁止返回任何值，所以``__init__``方法其实是“初始化方法”。真正的构造方法是``__new__``。
- 从``__new__``方法到``__init__``方法，是最常见的。但不是唯一的。``__new__``方法也可以返回其他类的实例，此时，解释器不会调用``__init__``方法。

```python
class User:
    def __new__(cls, *args, **kwargs):
        print("in new")         #in new
        print(cls)              #cls是当前class对象    <class '__main__.User'>
        print(type(cls))        #<class 'type'>
        return super().__new__(cls)   #必须返回class对象，才会调用__init__方法

    def __init__(self,name):
        print("in init")        #in init
        print(self)             #self是class的实例对象      <__main__.User object at 0x00000000021B8780>
        print(type(self))       #<class '__main__.User'>
        self.name = name

# new是用用来控制对象的生成过程，在对象生成之前
# init是用来完善对象的
# 如果new方法不返回对象，则不会调用init函数
if __name__ == '__main__':
    user = User(name="derek")
```

![image-20200519232608646](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200519232608646.png)

![image-20200519233754398](E:\note\慕课网Python高级核心97讲\Untitled.assets\image-20200519233754398.png)

## 7.5 自定义元类

- 通过传入不同的字符串动态的创建不同的类

  ```python
  def create_class(name):
      if name == "user":
          class User:
              def __str__(self):
                  return "user"
          return User
      elif name == "company":
          class Company:
              def __str__(self):
                  return "company"
          return Company
  if __name__ == '__main__':
      Myclass = create_class("user")
      my_obj = Myclass()
      print(my_obj)    #user
      print(type(my_obj))     #<class '__main__.create_class.<locals>.User'>
  ```

  

- 用type创建

  ```python
  # 一个简单type创建类的例子
  #type(object_or_name, bases, dict)
  #type里面有三个参数，第一个类名，第二个基类名，第三个是属性
  User = type("User",(),{"name":"haifeng"})
  
  my_obj = User()
  print(my_obj.name)    #haifeng
  ```

  ```python
  # 不但可以定义属性，还可以定义方法
  def say(self):     #必须加self
      return "i am haifeng"
  
  User = type("User",(),{"name":"haifeng","say":say})
  
  my_obj = User()
  print(my_obj.name)     #haifeng
  print(my_obj.say())    #i am haifeng
  ```

  ```python
  # 让type创建的类继承一个基类
  
  def say(self):     #必须加self
      return "i am haifeng"
  
  class BaseClass:
      def answer(self):
          return "i am baseclass"
  
  #type里面有三个参数，第一个类名，第二个基类名，第三个是属性
  User = type("User",(BaseClass,),{"name":"haifeng","say":say})
  
  if __name__ == '__main__':
  
      my_obj = User()
      print(my_obj.name)          # haifeng
      print(my_obj.say())         # i am haifeng
      print(my_obj.answer())      # i am baseclass
  ```

- 什么是元类， 元类是创建类的类   对象<-class(对象)<-type

  元类就是创建类的类，比如上面的type

  在实际编码中，我们一般不直接用type去创建类，而是用元类的写法，自定义一个元类metaclass去创建

  ```python
  # 把User类创建的过程委托给元类去做，这样代码的分离性比较好
  
  class MetaClass(type):
      def __new__(cls, *args, **kwargs):
          return super().__new__(cls,*args, **kwargs)
  
  class User(metaclass=MetaClass):
      def __init__(self,name):
          self.name = name
  
      def __str__(self):
          return "test"
  
  if __name__ == '__main__':
      #python中类的实例化过程，会首先寻找metaclass，通过metaclass去创建User类
      my_obj = User(name="haifeng")
      print(my_obj)    # test
      print(my_obj.name)  # haifeng
  ```

- object是type的实例，而type是object的子类。

  所有类都是type的实例，元类是type的子类。元类可以通过实现``__init__``实现定制实例。

  

## 7.6 元类实现ORM

```python
# 需求
import numbers


class Field:
    pass

class IntField(Field):
    # 数据描述符
    def __init__(self, db_column, min_value=None, max_value=None):
        self._value = None
        self.min_value = min_value
        self.max_value = max_value
        self.db_column = db_column
        if min_value is not None:
            if not isinstance(min_value, numbers.Integral):
                raise ValueError("min_value must be int")
            elif min_value < 0:
                raise ValueError("min_value must be positive int")
        if max_value is not None:
            if not isinstance(max_value, numbers.Integral):
                raise ValueError("max_value must be int")
            elif max_value < 0:
                raise ValueError("max_value must be positive int")
        if min_value is not None and max_value is not None:
            if min_value > max_value:
                raise ValueError("min_value must be smaller than max_value")

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError("int value need")
        if value < self.min_value or value > self.max_value:
            raise ValueError("value must between min_value and max_value")
        self._value = value


class CharField(Field):
    def __init__(self, db_column, max_length=None):
        self._value = None
        self.db_column = db_column
        if max_length is None:
            raise ValueError("you must spcify max_lenth for charfiled")
        self.max_length = max_length

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("string value need")
        if len(value) > self.max_length:
            raise ValueError("value len excess len of max_length")
        self._value = value


class ModelMetaClass(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        if name == "BaseModel":
            return super().__new__(cls, name, bases, attrs, **kwargs)
        fields = {}
        for key, value in attrs.items():
            if isinstance(v alue, Field):
                fields[key] = value
        attrs_meta = attrs.get("Meta", None)
        _meta = {}
        db_table = name.lower()
        if attrs_meta is not None:
            table = getattr(attrs_meta, "db_table", None)
            if table is not None:
                db_table = table
        _meta["db_table"] = db_table
        attrs["_meta"] = _meta
        attrs["fields"] = fields
        del attrs["Meta"]
        return super().__new__(cls, name, bases, attrs, **kwargs)


class BaseModel(metaclass=ModelMetaClass):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return super().__init__()

    def save(self):
        fields = []
        values = []
        for key, value in self.fields.items():
            db_column = value.db_column
            if db_column is None:
                db_column = key.lower()
            fields.append(db_column)
            value = getattr(self, key)
            values.append(str(value))

        sql = "insert {db_table}({fields}) value({values})".format(db_table=self._meta["db_table"],
                                                                   fields=",".join(fields), values=",".join(values))
        pass

class User(BaseModel):
    name = CharField(db_column="name", max_length=10)
    age = IntField(db_column="age", min_value=1, max_value=100)

    class Meta:
        db_table = "user"


if __name__ == "__main__":
    user = User(name="bobby", age=28)
    # user.name = "bobby"
    # user.age = 28
    user.save()
```