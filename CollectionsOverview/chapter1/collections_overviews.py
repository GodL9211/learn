#!usr/bin/env python
#-*- coding:utf-8 _*-
# __author__：连海峰
# __time__：2018/11/18 14:27

from collections import namedtuple

User = namedtuple("User", ["name", "age", "height"])
user = User(name="haifeng", age=25, height=175)
user_tuple = ("boby", 26, 175)
user2 = User(*user_tuple, "master---")