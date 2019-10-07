# -*- coding: utf-8 -*-

from testbase import testcase


class MyTestCase(testcase.TestCase):
    def run_test(self):
        """
        Abstract function
        :return:
        """
        pass

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
