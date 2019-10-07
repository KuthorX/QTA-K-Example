# -*- coding: utf-8 -*-
from testbase import testcase
from kExample.ch05.common.func import *
from kExample.ch05.common.MyTestCase import MyTestCase
from testbase import datadrive


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


@datadrive.DataDrive(test_data)
class GetTest(MyTestCase):
    """
    测试 get 请求
    """
    owner = "Tester"
    timeout = 5
    priority = testcase.TestCase.EnumPriority.High
    status = testcase.TestCase.EnumStatus.Design

    def run_test(self):
        case_data = self.casedata
        self.start_step("Request interface")
        a = case_data["a"]
        b = case_data["b"]
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


if __name__ == '__main__':
    GetTest().debug_run()
