official https://nlp.johnsnowlabs.com/docs/en/installhttps://nlp.johnsnowlabs.com/docs/en/install
https://phoenixnap.com/kb/install-spark-on-windows-10 

step 1: Install spark
https://spark.apache.org/downloads.html.

step 2: 
create dir: mkdir hadoop mkdir bin or C:\hadoop\bin 
place winutils.exe download  https://github.com/cdarlint/winutils/blob/master/hadoop-2.7.3/bin/winutils.exe;
create dir C:\Spark extract download spark 

step 3:
windows type edit the system variable
set enviroment variable 

variable: HADOOP_HOME
value: C:\Spark\spark-3.0.1-bin-hadoop2.7

variable: SPARK_HOME
value: C:\Spark\spark-3.0.1-bin-hadoop2.7

Install Java 
variable: JAVA_HOME
value C:\Program Files\Java\jdk-15.0.1

Go into Path and New  
%SPARK_HOME%\bin
%HADOOP_HOME%\bin

Create Environment for spark_nlp
$ java -version
# should be Java 8 (Oracle or OpenJDK)

$ conda create -n sparknlp python=3.7 -y
$ conda activate sparknlp
$ pip install spark-nlp==3.3.4 pyspark==3.1.2

again set environment variable for pyspark 
variable name PYTHONPATH
C:\Spark\spark-3.0.1-bin-hadoop2.7/python/lib/py4j-0.10.9-src.zip

To open jupyter with Pyspark

set enviroment 
variable name: PYSPARK_DRIVER_PYTHON
variable value: jupyter

variable name: PYSPARK_DRIVER_PYTHON_OPTS
variable value: notebook


anaconda prompt 
conda activate sparknlp

enter : pyspark 
this will open jupyter notebook

2: To find and initialize spark 
import findspark
findspark.init() 

if issue like unable to find spark then just restart your pc 
activate conda enviroment sparknlp
enter pyspark
execute 2:

For checking sparknlp
from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline
import sparknlp
sparknlp.start()


print("Spark NLP version: ", sparknlp.version())
print("Apache Spark version: ", spark.version)




### Issues
TypeError: 'JavaPackage' object is not callable

ref : https://github.com/JohnSnowLabs/spark-nlp#usage

used and Worked in my case 
pyspark --packages com.johnsnowlabs.nlp:spark-nlp_2.12:3.3.4

spark = SparkSession.builder \
    .appName("Spark NLP")\
    .master("local[4]")\
    .config("spark.driver.memory","16G")\
    .config("spark.driver.maxResultSize", "0") \
    .config("spark.kryoserializer.buffer.max", "2000M")\
    .config("spark.jars.packages", "com.johnsnowlabs.nlp:spark-nlp_2.12:3.3.4")\
    .getOrCreate()
     
 