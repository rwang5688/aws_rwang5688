import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext, SparkConf
from awsglue.context import GlueContext
from awsglue.job import Job
import time

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

job = Job(glueContext)
job.init(args['JOB_NAME'], args)

output_path = "s3://<bucket>/<folder>/" + str(time.time()) + "/"
documentdb_uri = "mongodb://<host name>:27017"
documentdb_write_uri = "mongodb://<host name>:27017"

read_docdb_options = {
    "uri": documentdb_uri,
    "database": "test",
    "collection": "profiles",
    "username": "<username>",
    "password": "<password>",
    "ssl": "true",
    "ssl.domain_match": "false",
    "partitioner": "MongoSamplePartitioner",
    "partitionerOptions.partitionSizeMB": "10",
    "partitionerOptions.partitionKey": "_id"
}

write_documentdb_options = {
    "uri": documentdb_write_uri,
    "database": "test",
    "collection": "collection1",
    "username": "<username>",
    "password": "<password>",
    "ssl": "true",
    "ssl.domain_match": "false",
    "partitioner": "MongoSamplePartitioner",
    "partitionerOptions.partitionSizeMB": "10",
    "partitionerOptions.partitionKey": "_id"
}

# Get DynamicFrame from DocumentDB
dynamic_frame2 = glueContext.create_dynamic_frame.from_options(connection_type="documentdb",
                                                               connection_options=read_docdb_options)

# Write DynamicFrame to DocumentDB
glueContext.write_dynamic_frame.from_options(dynamic_frame2, connection_type="documentdb",
                                             connection_options=write_documentdb_options)

job.commit()

