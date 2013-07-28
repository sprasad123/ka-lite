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
    >>> btc.Hello_world(comment="text", fixture="/foo/bar.json").execute(iterations=2)

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
from main.models import ExerciseLog, VideoLog, UserLog
from securesync.models import Facility, FacilityUser, FacilityGroup

class Hello_world(benchmark_base.Common):

    def _setup(self):
        random.seed(time.time()) 

    def _get_post_execute_info(self):
        return "Hello world has finished"
                
    def _execute(self):
        time.sleep(10. * random.random())
        
class Validate_models(benchmark_base.Common):

    def _execute(self):
        management.call_command('validate', verbosity=1)
        

class Generate_real_data(benchmark_base.Common):
    """
    generaterealdata command is both i/o and moderately cpu intensive
    The i/o in this task is primarily INSERT
    Note: if more excercises or videos are added, this benchmark will
    take longer!
    """
    
    def _setup(self):
        self.max_iterations = 1
        management.call_command('clean_pyc')
        management.call_command('compile_pyc')
        management.call_command('flush', interactive=False)
        
    def _execute(self):
        management.call_command('generaterealdata')

    def _get_post_execute_info(self):
        info = {}
        info['ExerciseLog.objects.count'] = ExerciseLog.objects.count()
        info['VideoLog.objects.count'] = VideoLog.objects.count()
        info['UserLog.objects.count'] = UserLog.objects.count()
        info['Facility.objects.count'] = Facility.objects.count()
        info['FacilityUser.objects.count'] = FacilityUser.objects.count()
        info['FacilityGroup.objects.count'] = FacilityGroup.objects.count()
        return info
        
    def _teardown(self):
        from main.models import ExerciseLog, VideoLog, UserLog
        
        
class One_thousand_random_reads(benchmark_base.Common):
    """
    One thousand random accesses of the video and exercise logs (500 of each)
    The IO in the test is primarily SELECT and will normally be cached in memory
    """
    
    def _setup(self):
        random.seed(24601)
        management.call_command('clean_pyc')
        management.call_command('compile_pyc')
        #give the platform a chance to cache the logs
        self.exercise_list = ExerciseLog.objects.get_query_set()
        self.video_list = VideoLog.objects.get_query_set()
        self.exercise_count = ExerciseLog.objects.count()
        self.video_count = VideoLog.objects.count()
           
    def _execute(self):
        for x in range(500):
            VideoLog.objects.get(id=self.video_list[int(random.random()*self.video_count)].id)
            ExerciseLog.objects.get(id=self.exercise_list[int(random.random()*self.exercise_count)].id)          

    def _get_post_execute_info(self):
        return {"total_records_accessed": 1000}


        
class One_hundred_random_log_updates(benchmark_base.Common):
    """
    One hundred random accesses and updates tothe video and exercise logs (50 of each)
    The I/O here is SELECT and UPDATE - update will normally generate physical media access
    """
    
    def _setup(self):
        random.seed(24601)
        management.call_command('clean_pyc')
        management.call_command('compile_pyc')
        #give the platform a chance to cache the logs
        self.exercise_list = ExerciseLog.objects.get_query_set()
        self.video_list = VideoLog.objects.get_query_set()
        self.exercise_count = ExerciseLog.objects.count()
        self.video_count = VideoLog.objects.count()        
    def _execute(self):
        for x in range(50):
            this_video = VideoLog.objects.get(id=self.video_list[int(random.random()*self.video_count)].id)
            #this_video.total_seconds_watched += 1
            this_video.save()
            this_exercise = ExerciseLog.objects.get(id=self.exercise_list[int(random.random()*self.exercise_count)].id)
            #this_exercise.attempts += 1
            this_exercise.save()
            

    def _get_post_execute_info(self):
        return {"total_records_updated": 100}