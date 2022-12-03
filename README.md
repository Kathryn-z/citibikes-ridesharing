# Surviving dreaded commute in NYC - A case study on Citi Bike and Ride-Sharing
- Kathryn (Yanchen) Zhou and Larry (Yihao) Zhong

## Data and Schema
- Name: Citi Bike Trip Histories
- Description: The dataset includes information about starting and ending dates/times, stations, user type and rideable type. The data was maintained by a group of interested private citizens. 
- Link to data: https://ride.citibikenyc.com/system-data
- Range: 2019.02 to 2022.05
- Schema from 2019.02 to 2021.01 (only includes the selected ones):
    - `tripduration`, `starttime`, `stoptime`, `start station latitude`, `start station longitude`, `end station latitude`, `end station longitude`
- Schema from 2021.02 to 2022.05 (only includes the selected ones):
    - `started_at`, `ended_at`, `start_lat`, `start_lng`, `end_lat`, `end_lng`

<br />

## data_ingest directory
- `DataIngest.sh` file is placed under peel directory: `project/input` and it reads and unzips all the monthly citibike data from the citibike data website. 
- All the csv files are saved to peel directory: `project/input` and uploaded to hdfs directory: `project/input`.
- Screenshots can be found under the `screenshots/data_ingest` folder.

<br />

## etl_code directory 
- #### Larry: teammate subdirectory
- #### Kathryn: my subdirectory
    - `CleanMapper.java`, `Clean.java`: this MR application extracted the selected columns according to the schema above. And it checked if there is any invalid trip records (for instance, the trip duration is less than 0 seconds). It used all the monthly .csv files as the input and combined them together into one final output with the selected columns.
    - `CleanExe.sh`: the script for running the MR application. 
    - The input (all the monthly .csv files) is stored in the directory: `project/input`.
    - The output in hdfs: `/user/yz6956/project/clean/part-r-00000`.

<br />

## profiling_code directory 
- #### Larry: teammate subdirectory
- #### Kathryn: my subdirectory
    - **All the input for the following MR applications is `/user/yz6956/project/clean/part-r-00000` in hdfs.**
    - **All the screenshots for the following MR applications is in directory: `screenshots/profiling_code`.**

    <br />

    - `CountRecsMapper.java`, `CountRecsReducer.java`, `CountRecs.java`: this MR application counted the number of trip records from 2019.02 to 2022.05.
    - `CountRecsExe.sh`: the script for running the MR application. 
    - The output in hdfs: `/user/yz6956/project/profiling_count/part-r-00000`.

    <br />

    - `CountTimeRecsMapper.java`, `CountTimeRecsReducer.java`, `CountTimeRecs.java`: this MR application counted the number of trip records from 2019.02 to 2022.05.
    - `CountTimeRecsExe.sh`: the script for running the MR application. 
    - The output in hdfs: `/user/yz6956/project/profiling_time/part-r-00000`.

    <br />

    - `CountEachMonthRecsMapper.java`, `CountEachMonthRecsReducer.java`, `CountEachMonthRecs.java`: this MR application counted the number of trip records for every hour (from 0 to 24) from 2019.02 - 2022.05. 
    - `CountEachMonthRecsExe.sh`: the script for running the MR application. 
    - The output in hdfs: `/user/yz6956/project/profiling_eachmonth/part-r-00000`.

    <br />

    - `CountMonthRecsMapper.java`, `CountMonthRecsReducer.java`, `CountMonthRecs.java`: this MR application counted the number of monthly trip records from 2019 to 2022. **Note that this is different from the `CountEachMonthRecs.java` MR application.**
    - `CountMonthRecsExe.sh`: the script for running the MR application. 
    - The output in hdfs: `/user/yz6956/project/profiling_month/part-r-00000`.

    <br />

    - `CountYearRecsMapper.java`, `CountYearRecsReducer.java`, `CountYearRecs.java`: this MR application counted the number of trip records per year from 2019 to 2022.
    - `CountYearRecsExe.sh`: the script for running the MR application. 
    - The output in hdfs: `/user/yz6956/project/profiling_year/part-r-00000`.

    <br />

<br />

## ana_code directory
- ### Analysis focusing on Citibike Trip Duration
    - input file is `/user/yz6956/project/clean/part-r-00000` in hdfs.
    - `ana_code_duration.py`: I used pyspark to analyze all the data, espeically focusing on how the time duration of the citibike trips differ in different years, different months, and different time ranges. 
        - output file 1 in hdfs: `user/yz6956/project/ana_duration_year/part-00000-88a422ed-0e55-458c-9712-125970b83afd-c000.csv`
            - This dataframe uses year as the index/row. This means that there are 4 rows in ascending order: 2019, 2020, 2021 and 2022.
            - The column `Total Amount of Trip`: the total amount of citibike trips for every year
            - The column `Avg Duration Per Trip (minutes)`: the average time duration of the citibike trips for every year, which is calculated using the `avg()` function. 
            - The column `Max Trip Duration (minutes)`: the maximum time duration of the citibike trips for every year, which is calculated using the `max()` function.
            - The column `Avg Duration per Trip YoY Percentage`: the Year over Year percentage change of average duration of trips for each year starting from 2020. 
        - output file 2 in hdfs: `user/yz6956/project/ana_duration_month/part-00000-8d65e3db-1305-4ee9-ba80-b6ffe9cd69ef-c000.csv`
            - This dataframe uses year-month in asending order as the index/row. (2019 2 -> 2019 3 -> ... -> 2022 5)
            - The column `Total Amount of Trip`: the total amount of citibike trips for every year-month
            - The column `Avg Duration Per Trip (minutes)`: the average time duration of the citibike trips for every year-month, which is calculated using the `avg()` function. 
            - The column `Max Trip Duration (minutes)`: the maximum time duration of the citibike trips for every year-month, which is calculated using the `max()` function.
            - The column `Avg Duration per Trip MoM Percentage`: the Month over Month percentage change of average duration of trips for each month starting from 2019-03. 
        - output file 3 in hdfs: `user/yz6956/project/ana_duration_time/part-00000-2579252c-4c26-4d9f-aefb-571c4d7b6ce2-c000.csv`
            - This dataframe uses the eight time ranges in asending order as the index/row. I divided the 24 hours into 8 time ranges to better analyze when people tend to use citibikes more during the day. Namely, 0am-3am -> 3am-6am -> ... -> 9pm-12am. For simiplicity reason, I added index before the time range and used 0-24 to represent different hours. 
            - The column `Total Amount of Trip`: the total amount of citibike trips for every time range
            - The column `Avg Duration Per Trip (minutes)`: the average time duration of the citibike trips for every time range, which is calculated using the `avg()` function. 
            - The column `Max Trip Duration (minutes)`: the maximum time duration of the citibike trips for every time range, which is calculated using the `max()` function.
            - The column `Avg Duration per Trip HoH Percentage`: the Hour over Hour percentage change of hourly average duration of trips for each time range starting from 3am-6am. 
        
    - `ana_durationExe.sh`: the script for running `ana_code_duration.py`

- ### Analysis focusing on Citibike Trip Amount
    - input file is `/user/yz6956/project/clean/part-r-00000` in hdfs.
    - `ana_code_count.py`: I used pyspark to analyze all the data, espeically focusing on how the amount of citibike trips differ in different years, different months, and different time ranges. 
        - output file 1 in hdfs: `user/yz6956/project/ana_count_year/part-00000-5a37b528-0469-4cad-839a-df2d404c4919-c000.csv`
            - This dataframe uses year as the index/row. This means that there are 4 rows in ascending order: 2019, 2020, 2021 and 2022.
            - The column `Total Amount of Trip`: the total amount of citibike trips for every year
            - The column `Avg Monthly Amount of Trip`: the average monthly amount of trips for every year, which is calculated by the total amount of trips / number of months of that year. (11 months for 2019 and 5 months for 2022)
            - The column `Avg Daily Amount of Trip`: the average daily amount of trips for every year, which is calculated by the total amount of trips / number of days of that year.
            - The column `Monthly Avg Amount of Trip YoY Percentage`: the Year over Year percentage change of monthly average amount of trips for each year starting from 2020. 
            - The column `Daily Avg Amount of Trip YoY Percentage`: the Year over Year percentage change of daily average amount of trips for each year starting from 2020. 
        - output file 2 in hdfs: `user/yz6956/project/ana_count_month/part-00000-233eadf7-55f5-4647-84cb-c57418408c91-c000.csv`
            - This dataframe uses year-month in asending order as the index/row. (2019 2 -> 2019 3 -> ... -> 2022 5)
            - The column `Total Amount of Trip`: the total amount of citibike trips for that year-month
            - The column `Avg Daily Amount of Trip`: the average daily amount of trips for every year-month, which is calculated by the total amount of trips / number of days of that month.
            - The column `Daily Avg Amount of Trip MoM Percentage`: the Month over Month percentage change of daily average amount of trips for each month starting from 2019-03. 
        - output file 3 in hdfs: `user/yz6956/project/ana_count_time/part-00000-d24898c9-330a-408c-ad37-4bee5b8826f5-c000.csv`
            - This dataframe uses the eight time ranges in asending order as the index/row. Namely, 0am-3am -> 3am-6am -> ... -> 9pm-12am. For simiplicity reason, I added index before the time range and used 0-24 to represent different hours. 
            - The column `Total Amount of Trip`: the total amount of citibike trips for that time range
            - The column `Avg Hourly Amount of Trip`: the average hourly amount of trips, which is calculated by the total amount of trips / 3 since every time range consists of 3 hours.
            - The column `Daily Avg Amount of Trip HoH Percentage`: the Hour over Hour percentage change of hourly average amount of trips starting from 3am-6am. 

    - `ana_countExe.sh`: the script for running `ana_code_count.py`

<br />

## screenshots directory
- data_ingest: extracting and unziping all the monthly .csv citibike data from the website and put them into hdfs directory. 
- etl_code: running clean MR application.
- profiling_code: 
    - CountRecs: running CountRecs MR application.
    - CountTimeRecs: running CountTimeRecs MR application.
    - CountEachMonthRecs: running CountEachMonthRecs MR application.
    - CountMonthRecs: running CountMonthRecs MR application.
    - CountYearRecs: running CountYearRecs MR application.
- ana_code: 
    - ana_duration: screenshots of running `ana_code_duration.py`.
    - ana_count: screenshots of running `ana_code_count.py`.