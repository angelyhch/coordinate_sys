from HTMLTestRunner.HTMLTestRunner import HTMLTestRunner
import unittest, os
from tests import test_coordinate

suite = unittest.TestSuite()
loader = unittest.TestLoader()

tests_dir = os.path.abspath(os.path.dirname(__file__))
suite.addTest(loader.discover(start_dir=tests_dir))

with open('report.html', 'w', encoding='utf-8') as fp:
    runner = HTMLTestRunner(stream=fp,
                            description='测试报告描述',
                            title='自动测试',
                            verbosity=2)

    runner.run(suite)