""" Individual benchmark test cases

    Each benchmark is coded as a separate class

    an _execute method must be specified, this method
    is the actual test which needs to be timed in the benchmark.

    The _execute method can be called >1 time per run
     so it is important that the _execute method is normally re-runnable
     To force a method as not re-runnable,
      set self.max_iterations = 1 in _setup or _execute method

    optional _setup and _teardown methods will be called
     before and after the test, but these methods will not
     affect the benchmark timings

    EXAMPLE USAGE:

    $ ./manage.py shell
    
    >>> import benchmark.benchmark_test_cases as btc
    >>> mytest = btc.Hello_world(comment="some text", fixture="/foo/bar.json")
    >>> print mytest.execute(iterations=2)

    IMPORTANT: the fixture argument does NOT install the fixture - this argument
     is only used to record the fixture name in the result dictionary

    example result_dict:

{
'comment': 'some text',
'head': 'f11cf0e Merge pull request #247 from gimick/autostart_on_linux',
'individual_elapsed': {1: 7.616177082061768, 2: 7.196689128875732},
'iterations': 2,
'fixture': '/foo/bar.json',
'average_elapsed': 7.40643310546875,
'uname': ('Linux', 'xubuntu', '3.2.0-35-generic', '#55-Ubuntu SMP Wed Dec 5 17:42:16 UTC 2012', 'x86_64', 'x86_64'),
'branch': 'benchmark_v2',
'class': 'Hello_world'
}


 """
import time
import random

from django.core import management

import kalite.utils.testing.benchmark_base as benchmark_base


class Hello_world(benchmark_base.Common):

    def _setup(self):
        random.seed(time.time()) 
        
    def _execute(self):
        time.sleep(10. * random.random())
        
class Validate_models(benchmark_base.Common):

    def _execute(self):
        management.call_command('validate', verbosity=1)
        

class Generate_real_data(benchmark_base.Common):
    """
    generaterealdata command is both i/o and moderately cpu intensive

    Note: if more excercises or videos are added, this benchmark will
    take longer!

    expected record counts:
    FacilityUser = 20
    ExcerciseLog = 1185
    VideoLog = 2082
    UserLog = 0
    
    E5500 = {'comment': None, 'head': 'e578087 benchmark: initial commit', 'individual_elapsed': {1: 1183.6675910949707}, 'iterations': 1, 'fixture': None, 'average_elapsed': 1183.6675910949707, 'uname': ('Linux', 'xubuntu', '3.2.0-35-generic', '#55-Ubuntu SMP Wed Dec 5 17:42:16 UTC 2012', 'x86_64', 'x86_64'), 'branch': 'benchmark_v2', 'class': 'Generate_real_data'}

    """
    def _setup(self):
        self.max_iterations = 1
        management.call_command('clean_pyc')
        management.call_command('compile_pyc')
        management.call_command('flush', interactive=False)
        
    def _execute(self):
        management.call_command('generaterealdata')

    def _teardown(self):
        from main.models import ExerciseLog, VideoLog, UserLog
        
        
