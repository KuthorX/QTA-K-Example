# 05 - 网络请求 - Get 用例 Fix - DataDrive 数据驱动

我们这节要解决一个重点问题：

> 用例考虑不足。即使不考虑异常输入情况，也应该设计多几个常规用例。重点是，要如何实现？

这其实是个十分通用的场景：当有很多用例，他们自动化的逻辑相同，但是输入数据不同（更复杂的还有，输出数据会随着输入数据的不同而不同，导致自动化逻辑也会不同）的时候，怎么用 QTA 去处理？

## 回顾需求背景

假设有这两个接口，他们的功能是：

- GET，以 url param 形式输入 a 和 b，返回 a + b
- POST，以 application/json 形式输入 x 和 y，返回 x * y

测试 GET 接口的基础功能，不用测试异常输入场景。

## 解决

一种常规方法是，定义多个 `TestCase`

```python
class GetTest01(MyTestCase):
    ...
    def run_test(self):
        self.start_step("Request interface")
        a = 1
        b = 2
        ...

class GetTest02(MyTestCase):
    ...
    def run_test(self):
        self.start_step("Request interface")
        a = 0
        b = 100
        ...

class GetTest03(MyTestCase):
    ...
    def run_test(self):
        self.start_step("Request interface")
        a = 0
        b = -10
        ...
```

但是这样重复代码还是特别多。我们可以用 QTA 的 [**数据驱动**](https://qta-testbase.readthedocs.io/zh/v5.4.32/datadrive.html) 来实现：

我们修改一下 [GetTest.py](./GetTest.py):

```python
...
from testbase import datadrive
...
test_data = [
    {"a": 1, "b": 2},
    {"a": -1, "b": -1},
    {"a": 1, "b": 0},
    {"a": 0, "b": -1},
    {"a": 0, "b": 0},
]
...
@datadrive.DataDrive(test_data)
class GetTest(MyTestCase):
    def run_test(self):
        case_data = self.casedata
        self.start_step("Request interface")
        a = case_data["a"]
        b = case_data["b"]
        self.print_and_log("a: %s, b: %s" % (a, b))
...
```

1. 定义测试数据集 `test_data`
2. 在 `class GetTest...` 上使用装饰器 `datadrive.DataDrive()` ，同时传入 `test_data`
3. 在 `run_test` 中，通过 `self.casedata` 拿到测试用例集的当前元素（比如 `{"a": 1, "b": 2}` ），然后就可以直接拿里面的数据实现之前的逻辑了
    > 提示：传入 `datadrive.DataDrive()` 的 `test_data` 可以是 list/dict 类型
                                                                                                   
    > 注意：即使是 list 类型，QTA 也 ***不会按照顺序*** 把数据按照顺序传递给 `TestCase` ，这是当前 QTA 的实现

执行：

`python manage.py runtest kExample.ch05.GetTest --report-type html`

通过报告，可以看到有 5 条自动化用例被执行了。

> 提示：如果需要调试单个用例，可以执行：
> <br/>
> `python manage.py runtest kExample.ch05.GetTest/0 --report-type html`
> <br/>
> 这样每次都只会跑 `{"a": 1, "b": 2}` 用例数据。

多数据的问题解决了，但是还有可以优化的地方：看测试报告，会发现测试用例名称都是 `kExample.ch05.GetTest.GetTest/0` 、`kExample.ch05.GetTest.GetTest/1` ...... 即每个子用例名称都是数据在 `test_data` 里的索引，我们希望看测试报告的时候，能够通过用例名称快速看出这个用例的测试数据是什么。

一种实现方式是使用 dict 类型的 `test_data` （见 [GetTestUsingDict.py](./GetTestUsingDict.py) ）：

```python
test_data = {
    "a_p1_b_p2": {"a": 1, "b": 2},
    "a_n1_b_n1": {"a": -1, "b": -1},
    ...
}
```

执行 `python manage.py runtest kExample.ch05.GetTestUsingDict --report-type html` ，我们发现我们能根据子用例名称快速定位到想要查看的子报告。

> 注意：用例名称目前不支持 & = 空格 - 等特殊字符，这些特殊字符在执行的时候都会被替换为 _ ，所以我在表示正数的时候会加 p(positive)，负数的时候会加 n(negative)

当然，手动去填一个个子用例名称还是十分麻烦，更好的做法是定义一个 `gen_test_data` 函数（见 [GetTestUsingGenFunc.py](./GetTestUsingGenFunc.py) ）：

```python
...
def gen_test_data():
    def get_symbol(num):
        symbol = ""
        if num > 0:
            symbol = "p"
        elif num < 0:
            symbol = "n"
        return symbol

    test_data = {}
    a = [0, -1, 1]
    b = [0, -1, 1]
    for _a in a:
        for _b in b:
            _a_symbol = get_symbol(_a)
            _b_symbol = get_symbol(_b)
            name = "a_%s%s_b_%s%s" % (_a_symbol, abs(_a), _b_symbol, abs(_b))
            test_data[name] = {"a": _a, "b": _b}
    return test_data


test_data = gen_test_data()
...
```

执行 `python manage.py runtest kExample.ch05.GetTestUsingGenFunc --report-type html` ，可以看到我们很轻松地就生成了 9 条用例。

而执行 `python manage.py runtest kExample.ch05.GetTestUsingGenFunc/a_0_b_0 --report-type html` ，则可以只执行 `{"a": 0, "b": 0}` 的用例。

不过我们看着不同的用例有着相同的 *用例描述* “测试 get 请求” 还是不太满意，我们再用 `__attrs__` 参数让这些用例的 *用例描述* 都不一样（参考 [GetTestUsingGenFuncAttr.py](./GetTestUsingGenFuncAttr.py)）：

```python
def gen_test_data():
    def get_symbol(num):
    ...
    for _a in a:
        for _b in b:
            ...
            test_data[name] = {"a": _a, "b": _b, "__attrs__": {"__doc__": "a = %s ; b = %s" % (_a, _b)}}
    ...
```

执行 `python manage.py runtest kExample.ch05.GetTestUsingGenFuncAttr --report-type html` ，打开报告，不同用例的区分程度更高了。使用这种方法较 子用例名称 的好处是，可以添加特殊字符。当然，由于每个用例名称不能相同，生成的时候还是要注意一下避免产生重复的 key 。

> 提示：现实业务中，可能存在有 5 个参数分别有 5 个不同的值的接口。如果它们能任意组合，那么会有 3125 种组合，也就是有 3125 条自动化用例。用 `数据驱动`+`gen_test_data` 的方式，可以剩下很大的工作量。
> <br/>
> 当然，这只是理想情况。实际业务中，有的参数值组合可能并不兼容（处理输入逻辑不一致），有的组合的预期结果会和别的不一样（处理输出逻辑不一致）。对于这些场景，可以在 `test_data` 里通过添加额外的参数，然后在 `run_test` 里根据参数值的不同进行不同的处理来实现；如果这导致整个 `run_test` 过于复杂，也可以拆分成更多的子函数甚至拆成更多的 `XXXTestCase` 来实现。它们各有优劣，读者应该自己斟酌后再实施。

最后说一下一直没有解释的最后两行代码吧：

```python
if __name__ == '__main__':
    GetTest().debug_run()
```

直接执行该文件，因为 `debug_run` 的作用，`GetTest` 就会跑遍所有的用例，如果想跑单个用例，可以这么写：

```python
if __name__ == '__main__':
    GetTest().debug_run_one("a_0_b_0")
```



