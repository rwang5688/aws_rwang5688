package com.serverless.dal;


import com.amazonaws.services.dynamodbv2.AmazonDynamoDB;
import com.amazonaws.services.dynamodbv2.AmazonDynamoDBClientBuilder;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBMapper;
import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBMapperConfig;


public final class DynamoDBConnection {
    private static DynamoDBConnection db_connection = null;
    private AmazonDynamoDB db = null;
    private DynamoDBMapper mapper = null;

    private DynamoDBConnection() {
        this.db = AmazonDynamoDBClientBuilder.standard()
            .withRegion(Regions.US_WEST_2)
            .build();
    }

    public static DynamoDBConnection getInstance() {
        if (db_connection == null)
            db_connection = new DynamoDBConnection();

        return db_connection;
    }

    public AmazonDynamoDB getDb() {
        if (db_connection == null)
            db_connection = getInstance();

        return db_connection.db;
    }

    public DynamoDBMapper createDbMapper(DynamoDBMapperConfig mapperConfig) {
        if (this.db != null)
            mapper = new DynamoDBMapper(this.db, mapperConfig);

        return this.mapper;
    }
}

