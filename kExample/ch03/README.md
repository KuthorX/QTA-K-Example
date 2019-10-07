# 03 - 网络请求 - Get 用例 Fix - log_info

我们先回顾下上节的需求背景

## 需求背景

假设有这两个接口，他们的功能是：

- GET，以 url param 形式输入 a 和 b，返回 a + b
- POST，以 application/json 形式输入 x 和 y，返回 x * y

测试 GET 接口的基础功能，不用测试异常输入场景。

## 问题

先来解决这个问题：

> 测试报告虽然显示每个测试步骤结果都是通过，但是完全看不到任何执行用例过程中的详细信息（特别是网络请求相关的信息），别人看的时候会一头雾水，不知道测了哪些点。

所幸的是，QTA 的 `TestCase` 提供了 `log_info` 来解决这个问题：

我们修改一下 [GetTest.py](GetTest.py) 和 [./common/func.py](./common/func.py)

```python
# GetTest.py
    self.start_step("Request interface")
    a = 1
    b = 2
    self.log_info("a: %s, b: %s" % (a, b))
    request_url = "http://localhost:1996?a=%s&b=%s" % (a, b)
    request_url_au = add_uuid(request_url)
    self.log_info("request_url_au: %s" % request_url_au)
    code, text, exception = request_get(request_url_au)
    self.log_info("code: %s; text: %s; exception: %s" % (code, text, exception))
    assert_result = self.assert_("Request code is 200", code == 200)
    if not assert_result:
        self.log_info("Request interface FAIL! Don't run anymore.")
        return

    self.start_step("Check result")
    c = int(text)
    self.log_info("c: %s" % c)
    self.assert_("c == a + b", c == a + b)
```

```python
# ./common/func.py
def request_get(url, headers=None, proxies=None, if_print_curl_str=True, test_case=None):
    ...
    print(curl_str)
    # 这样就能在报告里显示 curl url 了
    if test_case:
        test_case.log_info(curl_str)
    ...
def request_post(url, headers=None, post_data=None, proxies=None, if_print_curl_str=True, test_case=None):
...
```

再次执行

`python manage.py runtest kExample.ch03.GetTest --report-type html`

查看报告，会发现多了很多有用的信息。

如果我们细心一点，会发现在命令执行后，curl str 会被打印一次在控制台——这在上一节的时候也是如此。这意味着，`log_info` 函数此时不会把日志输出到控制台（在 `--report-type stream` 的时候会）。如果我们想既输出到控制台又输出到 html 要怎么办呢？这个问题留到下一节解决。
 