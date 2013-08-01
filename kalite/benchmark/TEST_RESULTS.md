## Benchmark tests and results

### I/O performance benchmarks

#### Generate real data

This benchmark empties the database and then runs generaterealdata.  This benchmark measures I/O insert performance, and, to a lesser extent computation power.

* RaspberryPi benchmark result: **1.5 records per second**
* Intel E5500/Sata/3gb ram comparison: **2.7 records per second**

```
./stop.sh
./kalite/manage.py shell
>>> import benchmark.benchmark_test_cases as btc
>>> btc.GenerateRealData().execute()
```

#### One thousand random reads

Using the database created by *Generate real data*, tests data reading speed from the VideoLog and ExerciseLog models.

This benchmark measures SELECT speed and will probably use cached reads if enough memory is available.

* RaspberryPi benchmark result: **21.6 records per second**
* Intel E5500/Sata/3gb ram comparison: **410 records per second**

```
$./stop.sh
$./kalite/manage.py shell
>>> import benchmark.benchmark_test_cases as btc
>>> btc.OneThousandRandomReads().execute()
```

#### One hundred random log updates

Using the database created by *Generate real data*, this benchmark tests updating the VideoLog and ExerciseLog models.

This benchmark principally measures UPDATE speed and will normally generate physical I/O

* RaspberryPi benchmark result: **1.8 records per second**
* Intel E5500/Sata/3gb ram comparison: **2.9 records per second**

```
$./stop.sh
$./kalite/manage.py shell
>>> import benchmark.benchmark_test_cases as btc
>>> btc.OneHundredRandomLogUpdates().execute(iterations=5)
```

#### One hundred random log updates commit success

Same as above, but all one hundred updates are done in a sigle transaction
and should be quicker 

* RaspberryPi benchmark result: **2.0 records per second**
* Intel E5500/Sata/3gb ram comparison: **5.3 records per second**

```
$./stop.sh
$./kalite/manage.py shell
>>> import benchmark.benchmark_test_cases as btc
>>> btc.OneHundredRandomLogUpdatesSingleTransaction().execute(iterations=5)
```