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

output_path = "s3://wangrob-docdb-glue-test-output-us-east-1/jobs/" + str(time.time()) + "/"
docdb_read_uri = "mongodb://docdb-instance.cht1ctqm99mr.us-east-1.docdb.amazonaws.com:27017"
docdb_write_uri = "mongodb://docdb-instance.cht1ctqm99mr.us-east-1.docdb.amazonaws.com:27017"

read_docdb_options = {
    "uri": docdb_read_uri,
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

write_docdb_options = {
    "uri": docdb_write_uri,
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

write_s3_options = {
    "path": output_path
}

# Get DynamicFrame from DocumentDB
dynamic_frame2 = glueContext.create_dynamic_frame.from_options(connection_type="documentdb",
                                                               connection_options=read_docdb_options)

print("read dynamic_frame2: %s" % dynamic_frame2)

# Write DynamicFrame to DocumentDB
glueContext.write_dynamic_frame.from_options(dynamic_frame2, connection_type="documentdb",
                                             connection_options=write_docdb_options)

print("wrote collection1 to DocDB")

# Write DynamicFrame to S3
glueContext.write_dynamic_frame.from_options(dynamic_frame2, connection_type="s3",
                                             connection_options=write_s3_options,
                                             format="json")

print("wrote json to S3")

job.commit()

