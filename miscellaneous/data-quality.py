from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
sc = SparkContext('local[*]')
spark = SparkSession \
    .builder \
    .appName("how to read csv file") \
    .getOrCreate()

# Read Data
df = spark.read.csv('C:\\Users\\DELL\\Downloads\\AMFI_metadata.csv',header=True)
# Show Data
print(df.describe().show())
# Identidy Nulls
column = df.columns
print(column)
for col_name in column:
    count_null = df.where(col(col_name).isNull()).count()
    print("Count of NULL in {0} : {1}".format(col_name,count_null))
