 import findspark

findspark.init()
from pyspark.sql import SparkSession


from jobs.stream_tumbling import consume_raw_logs

# all the necessary jars
working_directory = "jars/*"


def consume_csv():
    df = (
        spark.read.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "topic_csv")
        .option("startingOffsets", "earliest")
        .load()
    )
    return df


def consume_xml(spark):
    df = (
        spark.read.format("kafka")
        .option("kafka.bootstrap.servers", "localhost:9092")
        .option("subscribe", "topic_xml")
        .option("startingOffsets", "earliest")
        .load()
    )
    return df


if __name__ == "__main__":

    spark = (
        SparkSession.builder.appName("logStream")
        .config("spark.driver.extraClassPath", working_directory)
        .getOrCreate()
    )

    userinput = str(input("Enter 1 for txt\nEnter 2 for csv \nEnter 3 for xml\n"))

    if userinput == "1":
        consume_raw_logs()
    elif userinput == "2":
        consume_csv(spark)
    elif userinput == "3":
        consume_xml(spark)
    else:
        print("Invalid input")

