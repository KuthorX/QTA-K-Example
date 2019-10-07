# 01 - 最简单的用例

## 代码解释

```python
# -*- coding: utf-8 -*-
```

这一句必须加，表示文件的编码方式。

```python
from testbase import testcase
```

第一个 testbase 表示 testbase 是一个包，而第二个 testbase 表示它是前者里的一个模块，我们可以用这个模块来构造一个 **测试用例类**：

```python
class SimpleTest(testcase.TestCase):
```

我们现在创建了一个 `SimpleTest` 类。它继承了刚刚导入的 `testcase` 模块里的 `TestCase` 类，所以我们可以开始使用 `TestCase` 提供的基本功能（之后会循序渐进地介绍更多的扩展功能）：

```python
    """
    用例描述
    """
    owner = "Tester"
    timeout = 5
    priority = testcase.TestCase.EnumPriority.High
    status = testcase.TestCase.EnumStatus.Design
```

被三对双引号括起来的是用例描述，它会显示在最后提到的测试报告里。

从 python 语言的角度来说，`owner` `timeout` `priority` `status` 都是这个类的属性，即都是它的成员之一。看不懂这句话暂时没关系，但是需要重点了解的是，这四个单词代表了 **QTA用例最基本的设置**：

- owner 用例负责人

    这个参数在测试报告里会展示，可以填写开发+测试，用于快速定位负责人
    
- timeout 超时时间（单位是分钟）

    这个参数一般我设定为 5，一些特殊情况可以设置长一些，建议多跑几次，以平均时间为参考来决定最终值

- priority 优先级（`testcase.TestCase.EnumPriority.` 后面接上 `BVT` `High` `Normal` `Low` 这 4 个值的其中一个）

    这个参数用于给用例打了一个 tag，可以在执行用例的时候筛选哪些优先级来执行。老实说我没怎么用这个参数，都是设置成了同样的值，毕竟每个大类下如果用例数不多，每条用例执行时间很短的情况下，没必要拆分优先级，因为全部跑也能很快跑完。其他开发者使用的时候注意要按照实际来调整。

- status 用例编写状态（`testcase.TestCase.EnumStatus.` 后面接上 `Design` `Implement` `Review` `Ready` `Suspend` 这 5 个值的其中一个）

    这个参数作用和 priority 一样，有时候一些用例暂时不用跑的时候，我会把它设置为 Suspend（挂起）。当然这只是一个思路，我同样也可以固定 status，然后把 priority 改成 Low，执行用例集的时候把 priority == Low 的过滤不执行即可。
    
    需要注意的是，用例是否执行 取决于执行用例集（或者叫计划）的时候的 **筛选项** 而 **不是 priority 和 status 本身的值**，也就是说即使 status == Suspend 也不能说这条用例一定不能被执行。这完全取决于你怎么设计。
    
    如何设计 **执行灵活度高** 的用例是另一个话题，这里先不做深入讨论。
    
回到代码，我们继续看之后定义的函数：

```python
    def run_test(self):
```

这里我们定义了一个 `run_test` 的函数（其实是重写了父类的同名函数），这个函数在用例被执行的时候会被调用。实际上，被调用的函数 **不止这一个** ，但是我们先只关注这个函数。

> 注意：run_test 函数名是固定的，不能修改！
    
```python
        self.start_step("Start Test")
```

这里我们调用了已经有内部实现了的 start_step 函数，它的作用是能在测试报告里，把每个校验逻辑直观地区分出来——这么说比较抽象，下一节里我会说明如何使用好这个 start_step 函数。

最后的 2 行代码如下：

```python
if __name__ == '__main__':
    SimpleTest().debug_run()
```

第一行表示定义了该 py 文件的 *模拟的程序入口*，可以不多深究。

第二行 `debug_run` 表示执行 `SimpleTest` 类的所有用例。

> 提示：现在看起来这个类好像只能有一个用例，**所有** 这个概念似乎没有用处？这里也先按下不表，之后会对这个函数和其他相关函数作进一步的讨论。


## 执行用例

用例编写好了，自然需要执行看看效果。

由于最后 2 行代码，执行 `python SimpleTest.py` 即可执行 `SimpleTest` 的所有用例。

但是，这样执行出来的结果不是很直观，而除了直接 `python SimpleTest.py` 以外，还有一个更友好直观的方式来调试用例：

回到项目根目录，有一个 `manage.py` 的文件，我们执行这条命令

`python manage.py runtest kExample.ch01 --report-type html`

在根目录下会生成一个本地的 html 报告，打开后可以看到用例的执行情况。

> 注意：在这一节的目录里有一个 result 子目录，里面是我执行命令后生成的报告，可以打开参考。

