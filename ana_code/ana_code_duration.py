from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.sql.window import Window

df = spark.read.option("delimiter", ",").option("header", "false").csv("/user/yz6956/project/clean/part-r-00000").toDF("start_time","end_time", "start_lat", "start_lng", "end_lat", "end_lng")

# transform to timestamp
df = df.withColumn("start_time", to_timestamp(col("start_time"), 'yyyy-MM-dd HH:mm:ss'))
df = df.withColumn("end_time", to_timestamp(col("end_time"), 'yyyy-MM-dd HH:mm:ss'))

# calculate the trip duration
df = df.withColumn("Trip Duration", floor((col("end_time").cast("long") - col("start_time").cast("long"))/60))

# Extract and create columns "Year", "Month", "Day" and "Hour"
df = df.withColumn('Year', year(df.start_time))
df = df.withColumn('Month', month(df.start_time))
df = df.withColumn('Date', dayofmonth(df.start_time))
df = df.withColumn('Day', dayofweek(df.start_time))
df = df.withColumn('Hour', hour(df.start_time))

# Extract and a create column for different hours (time range) in a day
df = df.withColumn('Time Range (0-24)', when((df['Hour']=='6') | (df['Hour']=='7') | (df['Hour']=='8'),'3. 6-9').\
    when((df['Hour']=='9') | (df['Hour']=='10') | (df['Hour']=='11'),'4. 9-12').\
    when((df['Hour']=='12') | (df['Hour']=='13') | (df['Hour']=='14'),'5. 12-15').\
    when((df['Hour']=='15') | (df['Hour']=='16') | (df['Hour']=='17'),'6. 15-18').\
    when((df['Hour']=='18') | (df['Hour']=='19') | (df['Hour']=='20'),'7. 18-21').\
    when((df['Hour']=='21') | (df['Hour']=='22') | (df['Hour']=='23'),'8. 21-24').\
    when((df['Hour']=='0') | (df['Hour']=='1') | (df['Hour']=='2'),'1. 0-3').\
otherwise('2. 3-6'))

# Display the result
df.show(5, False)

# groupby year
df_year = df.groupby("Year").agg(
    count("start_time").alias("Total Amount of Trip"),\
    avg("Trip Duration").alias("Avg Duration Per Trip (minutes)"),\
    round(max("Trip Duration")).alias("Max Trip Duration (minutes)"))

df_year = df_year.sort(asc("Year"))

w = Window.partitionBy().orderBy("Year")

df_year = df_year.withColumn("Prev_y", lag(df_year['Avg Duration Per Trip (minutes)']).over(w))
df_year = df_year.withColumn("Avg Duration per Trip YoY Percentage", when(isnull(df_year['Avg Duration Per Trip (minutes)'] - df_year.Prev_y), 0)
                              .otherwise((df_year['Avg Duration Per Trip (minutes)'] - df_year.Prev_y))/df_year.Prev_y * 100)
df_year = df_year.drop('Prev_y')

# Display the result
df_year.show(5, False)

df_year.coalesce(1).write.option("header",True).csv("/user/yz6956/project/ana_duration_year")

# groupby year and month
df_month = df.groupby("Year","Month").agg(
    count("start_time").alias("Total Amount of Trip"),\
    avg("Trip Duration").alias("Avg Duration Per Trip (minutes)"),\
    round(max("Trip Duration")).alias("Max Trip Duration (minutes)"))

df_month = df_month.sort(asc("Year"),"Month")

w2 = Window.partitionBy().orderBy("Year", "Month")

df_month = df_month.withColumn("Prev", lag(df_month['Avg Duration Per Trip (minutes)']).over(w2))
df_month = df_month.withColumn("Avg Duration Per Trip MoM Percentage", when(isnull(df_month['Avg Duration Per Trip (minutes)'] - df_month.Prev), 0)
                              .otherwise((df_month['Avg Duration Per Trip (minutes)'] - df_month.Prev))/df_month.Prev * 100)
df_month = df_month.drop('Prev')

# Display the result
df_month.show(5, False)

df_month.coalesce(1).write.option("header",True).csv("/user/yz6956/project/ana_duration_month")

# groupby time
df_time = df.groupby("Time Range (0-24)").agg(
    count("start_time").alias("Total Amount of Trip"),
    avg("Trip Duration").alias("Avg Duration Per Trip (minutes)"),\
    round(max("Trip Duration")).alias("Max Trip Duration (minutes)"))

df_time = df_time.sort(asc("Time Range (0-24)"))

w3 = Window.partitionBy().orderBy("Time Range (0-24)")

df_time = df_time.withColumn("Prev", lag(df_time['Avg Duration Per Trip (minutes)']).over(w3))
df_time = df_time.withColumn("Avg Duration Per Trip HoH Percentage", when(isnull(df_time['Avg Duration Per Trip (minutes)'] - df_time.Prev), 0)
                              .otherwise((df_time['Avg Duration Per Trip (minutes)'] - df_time.Prev))/df_time.Prev * 100)
df_time = df_time.drop('Prev')

# Display the result
df_time.show(5, False)

df_time.coalesce(1).write.option("header",True).csv("/user/yz6956/project/ana_duration_time")

exit()