# -*- coding: utf-8 -*-
from testbase import testcase


class SimpleTest(testcase.TestCase):
    """
    用例描述
    """
    owner = "Tester"
    timeout = 5
    priority = testcase.TestCase.EnumPriority.High
    status = testcase.TestCase.EnumStatus.Design

    def run_test(self):
        self.start_step("Start Test")


if __name__ == '__main__':
    SimpleTest().debug_run()

