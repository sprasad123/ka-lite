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
import datetime
import random

from django.core import management
from django.db import transaction
from selenium.webdriver.support import expected_conditions, ui 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import kalite.utils.testing.benchmark_base as benchmark_base
from main.models import ExerciseLog, VideoLog, UserLog
from securesync.models import Facility, FacilityUser, FacilityGroup
from utils.testing.browser import BrowserTestCase


class HelloWorld(benchmark_base.Common):

    def _setup(self):
        random.seed(time.time()) 

    def _execute(self):
        time.sleep(10. * random.random())

    def _get_post_execute_info(self):
        return "Hello world has finished"
        
class ValidateModels(benchmark_base.Common):

    def _execute(self):
        management.call_command('validate', verbosity=1)
        

class GenerateRealData(benchmark_base.Common):
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
        #management.call_command('flush', interactive=False)
        
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
        
        
class OneThousandRandomReads(benchmark_base.Common):
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

        
class OneHundredRandomLogUpdates(benchmark_base.Common):
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
            this_video.save()
            this_exercise = ExerciseLog.objects.get(id=self.exercise_list[int(random.random()*self.exercise_count)].id)
            this_exercise.save()

    def _get_post_execute_info(self):
        return {"total_records_updated": 100}


class OneHundredRandomLogUpdatesSingleTransaction(OneHundredRandomLogUpdates):
    """
    Same as above, but this time, only commit transactions at the end of the _execute phase.
    """
    @transaction.commit_on_success
    def _execute(self):
        super(OneHundredRandomLogUpdatesSingleTransaction, self)._execute()


class LoginLogout(benchmark_base.Common):

    def _setup(self, url="http://localhost:8008", username="admin", password="admin"):
        self.browser = webdriver.Firefox()
        self.url = url
        self.username = username
        self.password = password
        self.browser.get(self.url)
        wait = ui.WebDriverWait(self.browser, 30)
        wait.until(expected_conditions.title_contains(("Home")))
        wait = ui.WebDriverWait(self.browser, 30)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "nav_login")))
        random.seed(24601)
        time.sleep ((random.random()*20.0))  

    def _execute(self):
        elem = self.browser.find_element_by_id("nav_login")
        elem.send_keys(Keys.RETURN)
        
        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.title_contains(("Log in")))
        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "id_username")))         
        elem = self.browser.find_element_by_id("id_username")
        elem.send_keys(self.username)
        elem = self.browser.find_element_by_id("id_password")
        elem.send_keys(self.password + Keys.RETURN)
        
    def _get_post_execute_info(self):

        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "logout")))
        elem = self.browser.find_element_by_id("logout")
        elem.send_keys(Keys.RETURN)

        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.title_contains(("Home")))
        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "nav_login")))
        
        info = {}
        info["url"] = self.url
        info["username"] = self.username
        return info
        
    def _teardown(self):
        self.browser.close()


class SeleniumStudent(benchmark_base.Common):
    
    """student username/password will be passed in
        behaviour of this student will be determined by
        seed value - seeds will typically be between 1 and 40 representing
        each student in the class, but actually it is not important
        starttime is the django (Chicago) time!!!!  Using start time allows us to cue-up a bunch of students
         and then release them into the wild.
        behaviour profile is a seed to decide which activities the student will carry out.
          Students with the same profile will follow the same behaviour.
        
    """ 
    def _setup(self, url="http://localhost:8008", username="stevewall",
                password="student", starttime="00:00", duration=30, behaviour_profile=15):

        def wait_until_starttime(starttime):
            time.sleep((random.random() * 10.0) + 10) #sleep 
            now = datetime.datetime.today()
            if now.hour >= int(starttime[:2]):
                if now.minute >= int(starttime[-2:]):
                    return False
            return True
        while wait_until_starttime(starttime): pass #wait until lesson starttime
        
        self.endtime = time.time() + (duration * 60.)
        self.browser = webdriver.Firefox()
        self.host_url = url
        self.browser.get(self.host_url)
        wait = ui.WebDriverWait(self.browser, 30)
        wait.until(expected_conditions.title_contains(("Home")))
        wait = ui.WebDriverWait(self.browser, 30)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "nav_login")))
        random.seed(24601 + behaviour_profile) # seed the seed

        elem = self.browser.find_element_by_id("nav_login")
        elem.send_keys(Keys.RETURN)
        time.sleep(5+random.random()*60.) # stagger 
        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.title_contains(("Log in")))
        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "id_username")))         
        elem = self.browser.find_element_by_id("id_username")
        elem.send_keys(username)
        time.sleep(3)
        elem = self.browser.find_element_by_id("id_password")
        elem.send_keys(password)
        time.sleep(3)
        elem.send_keys(Keys.RETURN)
        time.sleep(5)

        # self.activity simulates the classroom activity for the student
        # All students begin with activity "begin".
        # A random 2dp number < 1.0 is then generated, and the next step is decided, working
        #  left to right through the list.
        # This allows a pseudo-random system usage - the behaviour_profile seeds the random
        #  number generator, so identical behaviour profiles will follow the same route through
        #  the self.activity sequence.
        #
        # we are hard-coded here for the following videos, so they need to be downloaded before beginning:
        #  o Introduction to carrying when adding
        #  o Example: Adding two digit numbers (no carrying)
        #  o Subtraction 2
        #  o Example: 2-digit subtraction (no borrowing)
        #  o Level 2 Addition
    
        self.activity = {}
        self.activity["begin"]= {
                "method":self._pass, "duration": 10,
                "args":{},
                "nextstep":[(.10, "begin"), (.25, "watch"), (.98, "exercise"), (.99, "end")]
                 }
                 
        self.activity["watch"]= {
                "method":self._pass, "duration":1,
                "args":{},
                "nextstep":[(.95, "w1"),(.99, "exercise")]
                 }
        self.activity["w1"]= {
                "method":self._get_path, "duration":2,
                "args":{"path":"/math/"},
                "nextstep":[(.99, "w2")]
                 }
        self.activity["w2"]= {
                "method":self._get_path, "duration":2,
                "args":{"path":"/math/arithmetic/"},
                "nextstep":[(.99, "w3")]
                }
        self.activity["w3"]= {
                "method":self._get_path, "duration":2,
                "args":{"path":"/math/arithmetic/addition-subtraction/"},
                "nextstep":[(.99, "w4")]
                 }
        self.activity["w4"]= {
                "method":self._get_path, "duration":2,
                "args":{"path":"/math/arithmetic/addition-subtraction/two_dig_add_sub/"},
                "nextstep":[(.99, "w5")]
                 }
        self.activity["w5"]= {
                "method":self._get_path, "duration":1,
                "args":{"path":"/math/arithmetic/"},
                "nextstep":[(.20, "wv1"), (.40, "wv2"), (.60, "wv3"), (.80, "wv4"), (.99, "wv5")]
            }
            
        self.activity["wv1"]= {
                "method":self._get_path, "duration":3,
                "args":{"path":"/math/arithmetic/addition-subtraction/two_dig_add_sub/v/addition-2/"},
                "nextstep":[(.99, "wv1_1")]
                 }
        self.activity["wv1_1"]= {
                "method":self._do_vid, "duration":750,
                "args":{},
                "nextstep":[(.10, "wv1_1"), (.20, "wv2"), (.99, "begin")]
                 }
                 
        self.activity["wv2"]= {
                "method":self._get_path, "duration":3,
                "args":{"path":"/math/arithmetic/addition-subtraction/two_dig_add_sub/v/adding-whole-numbers-and-applications-1/"},
                "nextstep":[(.99, "wv2_1")]
                 }
        self.activity["wv2_1"]= {
                "method":self._do_vid, "duration":95,
                "args":{},
                "nextstep":[(.10, "wv2_1"), (.70, "eadd2"), (.99, "begin")]
                 }

        self.activity["wv3"]= {
                "method":self._get_path, "duration":3,
                "args":{"path":"/math/arithmetic/addition-subtraction/two_dig_add_sub/v/subtraction-2/"},
                "nextstep":[(.99, "wv3_1")]
                 }
        self.activity["wv3_1"]= {
                "method":self._do_vid, "duration":760,
                "args":{},
                "nextstep":[(.10, "wv3_1"), (.30, "wv4"), (.90, "esub2"), (.99, "begin")]
                 }

        self.activity["wv4"]= {
                "method":self._get_path, "duration":3,
                "args":{"path":"/math/arithmetic/addition-subtraction/two_dig_add_sub/v/subtracting-whole-numbers/"},
                "nextstep":[(.99, "wv4_1")]
                 }
        self.activity["wv4_1"]= {
                "method":self._do_vid, "duration":175,
                "args":{},
                "nextstep":[(.10, "wv4_1"), (.30, "wv5"), (.90, "esub2"), (.99, "begin")]
                 }

        self.activity["wv5"]= {
                "method":self._get_path, "duration":3,
                "args":{"path":"/math/arithmetic/addition-subtraction/two_dig_add_sub/v/level-2-addition/"},
                "nextstep":[(.99, "wv5_1")]
                 }
        self.activity["wv5_1"]= {
                "method":self._do_vid, "duration":580,
                "args":{},
                "nextstep":[(.10, "wv5_1"), (.70, "eadd2"), (.80, "begin")]
                 }

        self.activity["exercise"]= {
                "method":self._pass, "duration":1,
                "args":{},
                "nextstep":[(.60, "eadd2"),(.99, "esub2")]
                 }                 
        self.activity["eadd2"]= {
                "method":self._click, "duration":3,
                "args":{"find_by":By.ID, "find_text":"nav_practice"},
                "nextstep":[(.99, "neadd2_1")]
                 }
        self.activity["neadd2_1"]= {
                "method":self._get_path, "duration":3,
                "args":{"path":"/exercisedashboard/?topic=addition-subtraction"},
                "nextstep":[(.99, "neadd2_2")]
                 }
        self.activity["neadd2_2"]= {
                "method":self._get_path, "duration":3,
                "args":{"path":"/math/arithmetic/addition-subtraction/two_dig_add_sub/e/addition_2/"},
                "nextstep":[(.99, "do_eadd2")]
                 }
        self.activity["do_eadd2"]= {
                "method":self._do_exer, "duration":5,
                "args":{},
                "nextstep":[(.03, "begin"), (.75, "do_eadd2"), (.99, "esub2")]
                 }
                        
        self.activity["esub2"]= {
                "method":self._click, "duration":2,
                "args":{"find_by":By.ID, "find_text":"nav_practice"},
                "nextstep":[(.99, "nesub2_1")]
                 }
        self.activity["nesub2_1"]= {
                "method":self._get_path, "duration":3,
                "args":{"path":"/exercisedashboard/?topic=addition-subtraction"},
                "nextstep":[(.99, "nesub2_2")]
                 }
        self.activity["nesub2_2"]= {
                "method":self._get_path, "duration":2,
                "args":{"path":"/math/arithmetic/addition-subtraction/two_dig_add_sub/e/subtraction_2/"},
                "nextstep":[(.99, "do_esub2")]
                 }
        self.activity["do_esub2"]= {
                "method":self._do_exer, "duration":5,
                "args":{},
                "nextstep":[(.03, "begin"), (.75, "do_esub2"), (.91, "watch"), (.99, "eadd2")]
                 }
                 
        self.activity["end"] = {
                "method":self._click, "duration":1,
                "args":{"find_by":By.ID, "find_text":"logout"},
                "nextstep":[(.99, "end")]
                 }
                       
    def _execute(self):
        current_activity = "begin"
        while (self.endtime >= time.time() and current_activity != "end"):
            result=self.activity[current_activity]["method"](self.activity[current_activity]["args"])
            if "duration" in self.activity[current_activity]:
                time.sleep(self.activity[current_activity]["duration"])
            
            next_activity_random = round(random.random(),2) 
            for threshold, next_activity in self.activity[current_activity]["nextstep"]:
                if threshold >= next_activity_random:
                    #print next_activity_random, "next_activity =", next_activity
                    current_activity = next_activity
                    break

    def _pass(self, args):
        pass

    def _click(self, args):
        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.element_to_be_clickable((args["find_by"], args["find_text"])))
        if args["find_by"] == By.ID:
            elem = self.browser.find_element_by_id(args["find_text"])
        elif args["find_by"] == By.PARTIAL_LINK_TEXT:
            elem = self.browser.find_element_by_partial_link_text(args["find_text"])
        elem.send_keys(Keys.RETURN)

    def _do_exer(self, args):
        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '#solutionarea input[type=text]'))) 
        elem = self.browser.find_element_by_css_selector('#solutionarea input[type=text]')
        elem.click()
        elem.send_keys("12345") # a wrong answer, but we don't care
        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "check-answer-button")))         
        elem = self.browser.find_element_by_id("check-answer-button")
        elem.send_keys(Keys.RETURN)
        time.sleep(4.5)

    def _do_vid(self, args):
        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "div#video-element.video-js div.vjs-big-play-button"))) 
        elem = self.browser.find_element_by_css_selector("div#video-element.video-js div.vjs-big-play-button")
        elem.click()
        
    def _get_path(self, args):
        self.browser.get(self.host_url + args["path"])

    def _get_post_execute_info(self):
        #we are done! class over, lets get out of here
        #10% students will shut browser and forget to logout
        if random.random() < 0.1:
            return True

        wait = ui.WebDriverWait(self.browser, 60)
        wait.until(expected_conditions.element_to_be_clickable((By.ID, "logout")))
        elem = self.browser.find_element_by_id("logout")
        elem.send_keys(Keys.RETURN)

    def _teardown(self):
        self.browser.close()

