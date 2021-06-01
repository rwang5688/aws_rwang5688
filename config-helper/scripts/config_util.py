import os
import logging
import boto3
from botocore.exceptions import ClientError


def get_config_client(profile_name, region_name):
    print('get_config_client: profile_name=%s, region_name=%s' % (profile_name, region_name))

    session = boto3.Session(profile_name=profile_name)
    config = session.client('config',
        region_name=region_name)
    return config


def get_deployed_config_rule_names(profile_name, region_name, config_rule_names):
    deployed_config_rule_names = []

    config = get_config_client(profile_name, region_name)
    if config is None:
        print('get_deployed_config_rule_names: Failed to get config client.')
        return deployed_config_rule_names

    next_token = ''
    page_number = 1
    try:
        while True:
            response = config.describe_config_rules(ConfigRuleNames=config_rule_names, NextToken=next_token)
        
            deployed_config_rules_on_page = response['ConfigRules']
            print('DEBUG: get_deployed_config_rule_names: found %d rules' % len(deployed_config_rules_on_page))
            for deployed_config_rule_on_page in deployed_config_rules_on_page:
                deployed_config_rule_name = deployed_config_rule_on_page['ConfigRuleName']
                #print('DEBUG: get_deployed_config_rule_names: add rule name - %s', deployed_config_rule_name)
                deployed_config_rule_names.append(deployed_config_rule_name)

            print('DEBUG: get_deployed_config_rule_names: finished page %d' % page_number)
            if 'NextToken' in response:
                next_token = response['NextToken']
                #print('DEBUG: get_deployed_config_rule_names: next token = %s', next_token)
                page_number = page_number + 1
            else:
                break
    except ClientError as e:
        logging.error("get_deployed_config_rule_names: unexpected error:")
        logging.exception(e)
        return deployed_config_rule_names

    return deployed_config_rule_names


def delete_config_rules(profile_name, region_name, config_rule_names_to_delete):
    config = get_config_client(profile_name, region_name)
    if config is None:
        print('delete_config_rules: Failed to get config client.')
        return False

    try:
        for config_rule_name_to_delete in config_rule_names_to_delete:
            print('DEBUG: delete_config_rules: delete rule name - %s', config_rule_name_to_delete)
            config.delete_config_rule(ConfigRuleName=config_rule_name_to_delete)
    except ClientError as e:
        logging.error("delete_config_rules: unexpected error:")
        logging.exception(e)
        return False

    return True

