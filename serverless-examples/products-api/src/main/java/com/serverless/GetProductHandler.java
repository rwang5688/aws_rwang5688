package com.serverless;

import java.util.Collections;
import java.util.Map;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.serverless.dal.Product;


public class GetProductHandler implements RequestHandler<Map<String, Object>, ApiGatewayResponse> {

	private static final Logger logger = LogManager.getLogger(GetProductHandler.class);

	@Override
	public ApiGatewayResponse handleRequest(Map<String, Object> input, Context context) {
        logger.info("received: {}", input);
        try {
            // get the 'pathParameters' from input
            Map<String, String> pathParameters =  (Map<String, String>)input.get("pathParameters");
            String productId = pathParameters.get("id");

            // get the Product by id
            Product product = new Product().get(productId);

            // send the response back
            if (product != null) {
                return ApiGatewayResponse.builder()
                        .setStatusCode(200)
                        .setObjectBody(product)
                        .setHeaders(Collections.singletonMap("X-Powered-By", "AWS Lambda & Serverless"))
                        .build();
            } else {
                return ApiGatewayResponse.builder()
                        .setStatusCode(404)
                        .setObjectBody("Product with id: '" + productId + "' not found.")
                        .setHeaders(Collections.singletonMap("X-Powered-By", "AWS Lambda & Serverless"))
                        .build();
            }
        } catch (Exception ex) {
            logger.error("Error in retrieving product: " + ex);

            // send the error response back
            Response responseBody = new Response("Error in retrieving product: ", input);
            return ApiGatewayResponse.builder()
                    .setStatusCode(500)
                    .setObjectBody(responseBody)
                    .setHeaders(Collections.singletonMap("X-Powered-By", "AWS Lambda & Serverless"))
                    .build();
        }
    }

}

