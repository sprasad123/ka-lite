
"""

Very temporary test harness

USAGE:
$ ./manage.py shell

import benchmark.temporary_test_runner
benchmark.temporary_test_runner.Run_me()

and if you don't mind data being written permanently to your db, this one can be used
# IMPORTANT THE ONE BELOW WILL PERMANENTLY ADD STUDENTS and FACILITIES TO YOUR DB !!!!
# IMPORTANT THE ONE BELOW WILL PERMANENTLY ADD STUDENTS and FACILITIES TO YOUR DB !!!!

benchmark.temporary_test_runner.Generate_data_in_live()
"""
import benchmark_test_cases

class Run_me(object):
    def __init__(self):


        print "=========================="
        print "temporary benchmark runner"
        print "=========================="

        print "-------------------------------"
        print "Hello world test (2 iterations)"
        print "-------------------------------"

        bench = benchmark_test_cases.Hello_world(comment="Random sleeps")
        result_dict = bench.execute(iterations=2)
        print result_dict
        print "Average elapsed (sec):", str(result_dict['average_elapsed'])

        print "------------------------------------"
        print "Validate models test (10 iterations)"
        print "------------------------------------"

        bench = benchmark_test_cases.Validate_models(comment="Validation x 10")
        result_dict = bench.execute(iterations=10)

        print "Average elapsed (sec):", str(result_dict['average_elapsed'])

        print "dictionary returned is:"
        print result_dict

class Generate_data_in_live(object):
    def __init__(self):
        # IMPORTANT THE ONE BELOW WILL PERMANENTLY ADD STUDENTS and FACILITIES TO YOUR DB !!!!
        print "-----------------------"
        print "Generate facility users"
        print "-----------------------"

        bench = benchmark_test_cases.Generate_facility_users(comment="Test some real database access")
        result_dict = bench.execute()
        print "Elapsed (sec):", str(result_dict['average_elapsed'])


