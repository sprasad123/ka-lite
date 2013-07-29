## Benchmark test results

## I/O performance benchmarks

### Generate real data

This benchmark empties the database and then runs generaterealdata.  This benchmark measures I/O insert performance, and, to a lesser extent computation power.

* RaspberryPi benchmark result: **1.5 records per second**
* Intel E5500/Sata/3gb ram comparison: **2.7 records per second**

```
./stop.sh
./kalite/manage.py shell
>>> import benchmark.benchmark_test_cases as btc
>>> btc.Generate_real_data().execute()
```

{'comment': None, 'post_execute_info': {1: {'FacilityUser.objects.count': 20, 'UserLog.objects.count': 0, 'VideoLog.objects.count': 2319, 'Facility.objects.count': 1, 'FacilityGroup.objects.count': 2, 'ExerciseLog.objects.count': 1271}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 2365.028766155243}, 'iterations': 1, 'fixture': None, 'average_elapsed': 2365.028766155243, 'uname': ('Linux', 'pi4', '3.6.11+', '#474 PREEMPT Thu Jun 13 17:14:42 BST 2013', 'armv6l', ''), 'branch': 'benchmark_v2', 'class': 'Generate_real_data'}


{'comment': None, 'post_execute_info': {1: {'FacilityUser.objects.count': 20, 'UserLog.objects.count': 0, 'VideoLog.objects.count': 1752, 'Facility.objects.count': 1, 'FacilityGroup.objects.count': 2, 'ExerciseLog.objects.count': 983}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 1037.5836029052734}, 'iterations': 1, 'fixture': None, 'average_elapsed': 1037.5836029052734, 'uname': ('Linux', 'xubuntu', '3.2.0-35-generic', '#55-Ubuntu SMP Wed Dec 5 17:42:16 UTC 2012', 'x86_64', 'x86_64'), 'branch': 'benchmark_v2', 'class': 'Generate_real_data'}


### One thousand random reads

Using the database created by *Generate real data*, tests data reading speed from the VideoLog and ExerciseLog models.

This benchmark measures SELECT speed and will probably use cached reads if enough memory is available.

* RaspberryPi benchmark result: **21.6 records per second**
* Intel E5500/Sata/3gb ram comparison: **410 records per second**

```
$./stop.sh
$./kalite/manage.py shell
>>> import benchmark.benchmark_test_cases as btc
>>> btc.One_thousand_random_reads().execute()
```

{'comment': None, 'post_execute_info': {1: {'total_records_accessed': 1000}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 46.34690499305725}, 'iterations': 1, 'fixture': None, 'average_elapsed': 46.34690499305725, 'uname': ('Linux', 'pi4', '3.6.11+', '#474 PREEMPT Thu Jun 13 17:14:42 BST 2013', 'armv6l', ''), 'branch': 'benchmark_v2', 'class': 'One_thousand_random_reads'}


{'comment': None, 'post_execute_info': {1: {'total_records_accessed': 1000}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 2.4416251182556152}, 'iterations': 1, 'fixture': None, 'average_elapsed': 2.4416251182556152, 'uname': ('Linux', 'xubuntu', '3.2.0-35-generic', '#55-Ubuntu SMP Wed Dec 5 17:42:16 UTC 2012', 'x86_64', 'x86_64'), 'branch': 'benchmark_v2', 'class': 'One_thousand_random_reads'}


### One hundred random log updates

Using the database created by *Generate real data*, this benchmark tests updating the VideoLog and ExerciseLog models.

This benchmark principally measures UPDATE speed and will normally generate physical I/O

* RaspberryPi benchmark result: 1.8 records per second
* Intel E5500/Sata/3gb ram comparison: 2.9 records per second

```
$./stop.sh
$./kalite/manage.py shell
>>> import benchmark.benchmark_test_cases as btc
>>> btc.One_hundred_random_log_updates().execute(iterations=5)
```

{'comment': None, 'post_execute_info': {1: {'total_records_updated': 100}, 2: {'total_records_updated': 100}, 3: {'total_records_updated': 100}, 4: {'total_records_updated': 100}, 5: {'total_records_updated': 100}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 65.08287596702576, 2: 55.4726881980896, 3: 52.48413300514221, 4: 52.294827938079834, 5: 52.56275415420532}, 'iterations': 5, 'fixture': None, 'average_elapsed': 55.579455852508545, 'uname': ('Linux', 'pi4', '3.6.11+', '#474 PREEMPT Thu Jun 13 17:14:42 BST 2013', 'armv6l', ''), 'branch': 'benchmark_v2', 'class': 'One_hundred_random_log_updates'}


{'comment': None, 'post_execute_info': {1: {'total_records_updated': 100}, 2: {'total_records_updated': 100}, 3: {'total_records_updated': 100}, 4: {'total_records_updated': 100}, 5: {'total_records_updated': 100}}, 'head': 'ab622ef more i/o benchmarks + tweak base class.', 'individual_elapsed': {1: 33.15039777755737, 2: 36.549885988235474, 3: 34.0961799621582, 4: 36.21947693824768, 5: 34.84787893295288}, 'iterations': 5, 'fixture': None, 'average_elapsed': 34.97276391983032, 'uname': ('Linux', 'xubuntu', '3.2.0-35-generic', '#55-Ubuntu SMP Wed Dec 5 17:42:16 UTC 2012', 'x86_64', 'x86_64'), 'branch': 'benchmark_v2', 'class': 'One_hundred_random_log_updates'}
