# Data Engineering Personal Project

The purpose of this project is to prove my ability to create a scalable ETL pipeline from scratch and maintain it properly.
In general, the pipeline is seperated into steps:
    - getting raw data and sending it into kafka topics
    - Automating processing using Airflow and Spark
    - Loading the processed data to different DB's (MSSQL, Elasticsearch, MongoDB)
    - Flask application with authentication for filtered quering by users
    - Back up to a cloud service


### step 1 - raw data to kafka
I used data from Finnhub's API about the stock market:
Rest API - for getting specific info regardin popular companies in the market.
WebSocket - for constant data of stocks prices.

This data is sepereted into topics and produced into kafka

### step 2 - consume data from kafka using spark
After set retention limit to kafka and ensuring that the process runs smoothly, I used local spark on a small scale to simulate the production process.
Spark consume data from the desired kafka topic and process, filter and organize the constant flow of stocks prices into readable df.