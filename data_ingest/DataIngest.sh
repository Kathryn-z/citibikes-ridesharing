for i in 02 03 04 05 06 07 08 09 10 11 12 
do
    curl -O https://s3.amazonaws.com/tripdata/2019$i-citibike-tripdata.csv.zip
    unzip 2019$i-citibike-tripdata.csv.zip
done

for i in 01 02 03 04 05 06 07 08 09 10 11 12 
do
    curl -O https://s3.amazonaws.com/tripdata/2020$i-citibike-tripdata.csv.zip
    curl -O https://s3.amazonaws.com/tripdata/2021$i-citibike-tripdata.csv.zip
    unzip 2020$i-citibike-tripdata.csv.zip
    unzip 2021$i-citibike-tripdata.csv.zip
done

for i in 01 02 03 04 05
do
    curl -O https://s3.amazonaws.com/tripdata/2022$i-citibike-tripdata.csv.zip
    unzip 2022$i-citibike-tripdata.csv.zip
done

rm -f *.zip