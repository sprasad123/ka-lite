### Detailed results

Test commands are in TEST_RESULTS.md 

Returned dictionary strings will be recorded here.

#### Generate real data

{'comment': None, 'post_execute_info': {1: {'FacilityUser.objects.count': 20, 'UserLog.objects.count': 0, 'VideoLog.objects.count': 2319, 'Facility.objects.count': 1, 'FacilityGroup.objects.count': 2, 'ExerciseLog.objects.count': 1271}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 2365.028766155243}, 'iterations': 1, 'fixture': None, 'average_elapsed': 2365.028766155243, 'uname': ('Linux', 'pi4', '3.6.11+', '#474 PREEMPT Thu Jun 13 17:14:42 BST 2013', 'armv6l', ''), 'branch': 'benchmark_v2', 'class': 'Generate_real_data'}

{'comment': None, 'post_execute_info': {1: {'FacilityUser.objects.count': 20, 'UserLog.objects.count': 0, 'VideoLog.objects.count': 1752, 'Facility.objects.count': 1, 'FacilityGroup.objects.count': 2, 'ExerciseLog.objects.count': 983}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 1037.5836029052734}, 'iterations': 1, 'fixture': None, 'average_elapsed': 1037.5836029052734, 'uname': ('Linux', 'xubuntu', '3.2.0-35-generic', '#55-Ubuntu SMP Wed Dec 5 17:42:16 UTC 2012', 'x86_64', 'x86_64'), 'branch': 'benchmark_v2', 'class': 'Generate_real_data'}


#### One thousand random reads

{'comment': None, 'post_execute_info': {1: {'total_records_accessed': 1000}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 46.34690499305725}, 'iterations': 1, 'fixture': None, 'average_elapsed': 46.34690499305725, 'uname': ('Linux', 'pi4', '3.6.11+', '#474 PREEMPT Thu Jun 13 17:14:42 BST 2013', 'armv6l', ''), 'branch': 'benchmark_v2', 'class': 'One_thousand_random_reads'}

{'comment': None, 'post_execute_info': {1: {'total_records_accessed': 1000}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 2.4416251182556152}, 'iterations': 1, 'fixture': None, 'average_elapsed': 2.4416251182556152, 'uname': ('Linux', 'xubuntu', '3.2.0-35-generic', '#55-Ubuntu SMP Wed Dec 5 17:42:16 UTC 2012', 'x86_64', 'x86_64'), 'branch': 'benchmark_v2', 'class': 'One_thousand_random_reads'}


#### One hundred random log updates

{'comment': None, 'post_execute_info': {1: {'total_records_updated': 100}, 2: {'total_records_updated': 100}, 3: {'total_records_updated': 100}, 4: {'total_records_updated': 100}, 5: {'total_records_updated': 100}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 65.08287596702576, 2: 55.4726881980896, 3: 52.48413300514221, 4: 52.294827938079834, 5: 52.56275415420532}, 'iterations': 5, 'fixture': None, 'average_elapsed': 55.579455852508545, 'uname': ('Linux', 'pi4', '3.6.11+', '#474 PREEMPT Thu Jun 13 17:14:42 BST 2013', 'armv6l', ''), 'branch': 'benchmark_v2', 'class': 'One_hundred_random_log_updates'}

{'comment': None, 'post_execute_info': {1: {'total_records_updated': 100}, 2: {'total_records_updated': 100}, 3: {'total_records_updated': 100}, 4: {'total_records_updated': 100}, 5: {'total_records_updated': 100}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 33.15039777755737, 2: 36.549885988235474, 3: 34.0961799621582, 4: 36.21947693824768, 5: 34.84787893295288}, 'iterations': 5, 'fixture': None, 'average_elapsed': 34.97276391983032, 'uname': ('Linux', 'xubuntu', '3.2.0-35-generic', '#55-Ubuntu SMP Wed Dec 5 17:42:16 UTC 2012', 'x86_64', 'x86_64'), 'branch': 'benchmark_v2', 'class': 'One_hundred_random_log_updates'}

#### One hundred random log updates commit success

{}

{'comment': None, 'post_execute_info': {1: {'total_records_updated': 100}, 2: {'total_records_updated': 100}, 3: {'total_records_updated': 100}}, 'head': 'ba04ed7 Update TEST_RESULTS.md', 'individual_elapsed': {1: 16.341366052627563, 2: 17.70698094367981, 3: 22.9561870098114}, 'iterations': 3, 'fixture': None, 'average_elapsed': 19.001511335372925, 'uname': ('Linux', 'xubuntu', '3.2.0-35-generic', '#55-Ubuntu SMP Wed Dec 5 17:42:16 UTC 2012', 'x86_64', 'x86_64'), 'branch': 'benchmark_v2', 'class': 'One_hundred_random_log_updates_commit_success'}
