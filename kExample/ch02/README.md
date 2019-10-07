# 02 - 网络请求 - Get 用例

现在要开始真正地编写自动化用例来应对业务需要了。

## 需求背景

假设有这两个接口，他们的功能是：

- GET，以 url param 形式输入 a 和 b，返回 a + b
- POST，以 application/json 形式输入 x 和 y，返回 x * y

测试 GET 接口的基础功能，不用测试异常输入场景。

## 代码解释

[./server/server.py](./server/server.py) 是一个基本实现了上述需求的 server，测试地址为 http://localhost:1996。

[./common/func.py](common/func.py) 包含了 3 个函数，分别用于处理 GET/POST 请求以及给请求 URL 增加一个随机参数（开发可以拿着这个随机参数去查整条请求链路逻辑），函数里有注释，可以直观地看出输入输出是什么。

> 提示：如果不同的用例会用到同样的函数，建议作为公共函数放在某个地方，即拿即用

我们重点来看 [GetTest.py](./GetTest.py)，开头结尾几行上一节都解释过，这里不再赘述，我们重点看中间 `run_test` 的实现：

```python
    self.start_step("Request interface")
    ...
    self.start_step("Check result")
```

可以看出，测试时把测试步骤分为了两个逻辑模块：

1. 请求接口
2. 判断接口返回是否正确

先看第 1 点：

```python
    a = 1
    b = 2
    request_url = "http://localhost:1996?a=%s&b=%s" % (a, b)
    request_url_au = add_uuid(request_url)
    code, text, exception = request_get(request_url_au)
    self.assert_("Request code is 200", code == 200)
    if not code == 200:
        return
```

逻辑可以分为三个部分：
1. 构造测试数据：赋值给参数 a、b
2. 执行网络请求：拼接 URL，添加随机参数，执行 GET 请求，获取返回结果
3. 检查返回结果：通过 QTA 的 `assert_` 函数（用法说明见点击 [这里](https://qta-testbase.readthedocs.io/zh/v5.4.32/testcheck.html)）来判断 HTTP 返回码是否符合预期，如果不符合则不继续执行之后的代码

> 注意：在 QTA 中，即使 `assert_` 断言失败了，测试代码仍然会继续执行。

再来看第 2 点：

```python
    c = int(text)
    self.assert_("c == a + b", c == a + b)
```

成功返回 200 后，可以直接将返回的字符串型的文本通过 python 内置的 `int` 函数转成整型，之后再执行一次断言即可。


## 执行用例

同上一节一样，执行：

`python manage.py runtest kExample.ch02.GetTest --report-type html`

即可获取到测试报告。

但是，等等，这里有很多的——

## 问题

1. 测试报告虽然显示每个测试步骤结果都是通过，但是完全看不到任何执行用例过程中的详细信息（特别是网络请求相关的信息），别人看的时候会一头雾水，不知道测了哪些点。
2. `assert_` 函数在通过的时候是 **不会打印检查信息** 的，只有在不通过的时候才会打印出 `Request code is 200 不通过` 这种提示，而且即使是这种提示，也并没有显示实际值，会导致难以排查问题。
3. 用例考虑不足。即使不考虑异常输入情况，也应该设计多几个常规用例。重点是，要如何实现？
4. 对服务端返回的数据过于信任。比如 `c = int(text)`，如果服务端返回了非数字，这里转换是会出异常的。虽然不捕获该异常用例也会失败，但是最好对这类情况做一些兼容处理。

所有用例通过固然是好事，但是这还 **远远不够**，我们要尽可能做到在非自动化维护者不看代码的情况下，只通过测试报告就能知道自动化到底做了什么。

在之后的几个章节中，我们会逐一解决上面的问题。
