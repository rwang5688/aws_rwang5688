import os
import json
import copy
import uuid
from pathlib import Path
import config_util


def get_env_var(env_var_name):
    env_var = ''
    if env_var_name in os.environ:
        env_var = os.environ[env_var_name]
    else:
        print('get_env_var: Failed to get %s' % env_var_name)
    return env_var


def get_env_vars():
    global default_profile_name
    global default_target_region

    default_profile_name = get_env_var('PROFILE_NAME')
    if default_profile_name == '':
        return False

    default_target_region = get_env_var('TARGET_REGION')
    if default_target_region == '':
        return False
    
    # success
    return True


def parse_arguments():
    import argparse
    global config_json_file_name

    parser = argparse.ArgumentParser()
    parser.add_argument('config_json_file_name', help='config json file name.')

    args = parser.parse_args()
    config_json_file_name = args.config_json_file_name

    if config_json_file_name is None:
        print('parse_arguments: config_json_file_name is missing.')
        return False

    # success
    return True


def get_json_data(file_name):
    with open(file_name) as f:
        data = json.load(f)
        return data
    return None


def main():
    print('\nStarting list_config_rules.py ...')

    success = get_env_vars()
    if not success:
        print('get_env_vars failed.  Exit.')
        return

    print('Env vars:')
    print('default_profile_name: %s' % default_profile_name)
    print('default_target_region: %s' % default_target_region)

    success = parse_arguments()
    if not success:
        print('parse_arguments failed.  Exit.')
        return

    print('Args:')
    print('config_json_file_name: %s' % config_json_file_name)

    config_json = get_json_data(config_json_file_name)
    if config_json is None:
        print('get_json_data failed.  Exit.')
        return

    print('%s:' % config_json_file_name)
    print(config_json)

    config_rule_names = config_json['ConfigRuleNames']
    if config_rule_names is None:
        print('ConfigRuleNames does not exist.  Setting to empty array.')
        config_rule_names = []
 
    profile_name = config_json['ProfileName']
    if profile_name is None:
        print('ProfileName does not exist.  Setting to default_profile_name.')
        profile_name = default_profile_name
    
    target_region = config_json['TargetRegion']
    if target_region is None:
        print('TargetRegion does not exist.  Setting to default_target_region.')
        target_region = default_target_region

    deployed_config_rule_names = config_util.get_deployed_config_rule_names(profile_name, target_region, config_rule_names)

    print("deployed_config_rule_names:")
    print(deployed_config_rule_names)
    num_deployed_config_rule_names = len(deployed_config_rule_names)
    print("Total # of deployed rules: %d" % num_deployed_config_rule_names)


if __name__ == '__main__':
    main()

