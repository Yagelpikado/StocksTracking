from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StringType, ArrayType, DoubleType, LongType, IntegerType
from pyspark.sql.functions import from_json, col
from pyspark.sql.streaming import StreamingQueryListener
import sys, os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)
from env import KAFKA_BOOTSTRAP_SERVER, KAFKA_STREAMING_TOPIC
# Listener for tracking spark batches status and rows numbers
class SparkListener(StreamingQueryListener):
    def onQueryStarted(self, event):
        print(f"Query started: {event.id}")

    def onQueryProgress(self, event):
        progress = event.progress
        batch_id = progress['batchId']
        num_input_rows = progress['numInputRows']
        print(f"Batch {batch_id} processed, rows: {num_input_rows}")

    def onQueryTerminated(self, event):
        print(f"Query terminated: {event.id}")

# New spark session
spark_inst = SparkSession.builder.appName("KafkaSparkConsumer")\
    .master("local[*]").config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0")\
    .getOrCreate()
spark_inst.streams.addListener(SparkListener())

# Read webstock stream from kafka broker for my stock_stream topic
df = spark_inst.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVER) \
    .option("subscribe", KAFKA_STREAMING_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Convert binary value to string and parse JSON
schema = StructType()\
    .add("c", ArrayType(StringType())) \
    .add("p", DoubleType()) \
    .add("s", StringType()) \
    .add("t", LongType()) \
    .add("v", IntegerType())

# Convert kafka binary data to json/str
json_df = df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

# Remove unncessary columns and renaming columns
transformed_df = json_df.select(
    col("s").alias("stock_symbol"),
    col("p").alias("last_price"),
    (col("t") / 1000).cast("timestamp").alias("timestamp"),
    col("v").alias("volume")
)

# Print streaming data to console  
query = transformed_df.writeStream \
    .format("console") \
    .outputMode("append") \
    .start()

# TODO: try to take only batch0, filter it to the last day, group by symbol, show price difference for that day,
#       and then add differences for each day available
query.awaitTermination()
