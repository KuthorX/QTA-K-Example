# 04 - 网络请求 - Get 用例 Fix - MyTestCase

我们这节要解决这两个问题：

1. `assert_` 函数在通过的时候是 **不会打印检查信息** 的，只有在不通过的时候才会打印出 `Request code is 200 不通过` 这种提示，而且即使是这种提示，也并没有显示实际值，会导致难以排查问题。
2. 想让 `log_info` 想既输出到控制台又输出到 html。

## 回顾需求背景

假设有这两个接口，他们的功能是：

- GET，以 url param 形式输入 a 和 b，返回 a + b
- POST，以 application/json 形式输入 x 和 y，返回 x * y

测试 GET 接口的基础功能，不用测试异常输入场景。

## 解决

如果自己重新实现一遍 `assert_` 和 `log_info` 的逻辑显然是十分麻烦的。关键问题在于，我们要做到即使 QTA 内部实现有变，也能游刃有余地修改存量的自动化用例。

一个比较常规的方法是加一些 *wrapper* ：

```python
    def print_and_log(self, strs, if_need_print=True, if_need_log=True):
        """
        A wrapper for log_info
        :param strs: 
        :param if_need_print: 
        :param if_need_log: 
        :return: 
        """
        if if_need_print:
            print(strs)
        if if_need_log:
            self.log_info(strs)
        
    def assert_w(self, hints, assert_statement, if_need_print=True, if_need_log=True):
        """
        Another assert_
        :param hints: 
        :param assert_statement: 
        :param if_need_print: 
        :param if_need_log: 
        :return: 
        """
        self.print_and_log("Assert: ", if_need_print, if_need_log)
        self.print_and_log(hints, if_need_print, if_need_log)
        if not assert_statement:
            self.fail(hints)
```

首先，我们定义了两个函数：

- `print_and_log`，这个函数默认会把传入的字符串 `print` 且也会 `log_info`
    > 注意：这里没有说 `print` 一定会输出到控制台，`log_info` 一定会输出到 html 报告里。这取决于 *输出重定向*。

- `assert_w`，这个函数实现中并没有调用 `assert_`，而是在断言语句（原 `assert_` 的第二个参数）不符合预期的时候，直接调用了 QTA 提供的 `fail` 函数，这个函数会直接让当前执行步骤失败。同时，默认情况下断言的提示（原 `assert_` 的第一个参数）会被 `print_and_log` 出来。
    > 注意：这里其实也可以用 `assert_` 函数实现，不过用 `fail` 会更直观一些。

然后，我们把这两个函数放到一个公共的类 [MyTestCase.py](./common/MyTestCase.py):

```python
from testbase import testcase


class MyTestCase(testcase.TestCase):
    ...

    def print_and_log(self, strs, if_need_print=True, if_need_log=True):
        ...
        
    def assert_w(self, hints, assert_statement, if_need_print=True, if_need_log=True):
        ...
```

最后，修改 [GetTest.py](./GetTest.py):

```python
from kExample.ch04.common.MyTestCase import MyTestCase

...

    def run_test(self):
        self.start_step("Request interface")
        a = 1
        b = 2
        self.print_and_log("a: %s, b: %s" % (a, b))
        request_url = "http://localhost:1996?a=%s&b=%s" % (a, b)
        request_url_au = add_uuid(request_url)
        self.print_and_log("request_url_au: %s" % request_url_au)
        code, text, exception = request_get(request_url_au)
        self.print_and_log("code: %s; text: %s; exception: %s" % (code, text, exception))
        self.assert_w("Request code is 200", code == 200)
        if not code == 200:
            self.print_and_log("Request interface FAIL! Don't run anymore.")
            return

        self.start_step("Check result")
        c = int(text)
        self.print_and_log("c: %s" % c)
        self.print_and_log("a + b: %s" % (a + b))
        self.assert_w("c == a + b", c == a + b)
```

把原来调用 `log_info` 和 `assert_` 的地方分别修改为新函数即可。

> 提示：[func.py](./common/func.py) 的 `log_info` 也可以修改为新函数，读者可以试一试。

现在执行

`python manage.py runtest kExample.ch04.GetTest --report-type html`

会发现即使 `assert_w` 成功，也会有相应的提醒了；同时控制台也有和 `log_info` 参数一样的输出了。
