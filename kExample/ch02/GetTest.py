# -*- coding: utf-8 -*-
from testbase import testcase
from kExample.ch02.common.func import *


class GetTest(testcase.TestCase):
    """
    测试 get 请求
    """
    owner = "Tester"
    timeout = 5
    priority = testcase.TestCase.EnumPriority.High
    status = testcase.TestCase.EnumStatus.Design

    def run_test(self):
        self.start_step("Request interface")
        a = 1
        b = 2
        request_url = "http://localhost:1996?a=%s&b=%s" % (a, b)
        request_url_au = add_uuid(request_url)
        code, text, exception = request_get(request_url_au)
        self.assert_("Request code is 200", code == 200)
        if not code == 200:
            return

        self.start_step("Check result")
        c = int(text)
        self.assert_("c == a + b", c == a + b)



if __name__ == '__main__':
    GetTest().debug_run()
