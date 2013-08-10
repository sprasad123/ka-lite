
"""
Very temporary test harness

python ./kalite/benchmark/run_selenium_student.py &

"""

#!/usr/bin/env python2

import os
import sys
import random

# Set up the paths
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path = [script_dir + "/../../../ka-lite/kalite/../python-packages/"] + sys.path
sys.path = [script_dir + "/../../../ka-lite/kalite/../"] + sys.path
sys.path = [script_dir + "/../../../ka-lite/kalite"] + sys.path

#import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'kalite.settings'

import benchmark_test_cases
import settings


class SeleniumStudent(object):
    def __init__(self):
        print "-----------------------"
        print "SeleniumStudent sequence"
        print "-----------------------"
        bench = benchmark_test_cases.SeleniumStudent(comment="Test some real database access"
                                                , username="stevewall"
                                                , password="student"
                                                , url="http://192.168.1.24:8008"
                                                , starttime="00:00"
                                                , duration=15
                                                , behaviour_profile=(random.random()*200))
        print bench.execute()

SeleniumStudent()