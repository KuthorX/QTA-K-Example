# -*- coding: utf-8 -*-
from testbase import testcase
from kExample.ch05.common.func import *
from kExample.ch05.common.MyTestCase import MyTestCase
from testbase import datadrive

test_data = [
    {"a": 1, "b": 2},
    {"a": -1, "b": -1},
    {"a": 1, "b": 0},
    {"a": 0, "b": -1},
    {"a": 0, "b": 0},
]


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
