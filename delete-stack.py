##delete a stack with given stack name##
from __future__ import division, print_function, unicode_literals
import sys
from os import environ
import logging
import argparse
import time
import boto3
import botocore
from botocore.exceptions import ClientError
LOGGER = logging.getLogger(__name__)
LOGFORMAT = "%(levelname)s: %(message)s"
LOGGER = logging.getLogger("Launch RDS CFT")
LOGLEVEL = environ.get("logLevel", "INFO")
logging.basicConfig(format=LOGFORMAT, level=LOGLEVEL)
LOGGER.setLevel(logging.getLevelName(LOGLEVEL))

parser = argparse.ArgumentParser()
parser.add_argument('--name', type=str, required=True)
parser.add_argument('--region', type=str, required=True)
args = parser.parse_args()

client = boto3.client('cloudformation', region_name = args.region)

def main():
    ###delete stack###
    stack_name = args.name
    params = {
        'StackName': stack_name,
    }
    if _stack_exists(stack_name):
        LOGGER.info("Deleting {}".format(stack_name))
        response = client.delete_stack(
            StackName=args.name
        )
        try:
            stackstatus = "DELETE_IN_PROGRESS"
            while (stackstatus == "DELETE_IN_PROGRESS"):
                LOGGER.info("DELETE IN PROGRESS")
                status = client.describe_stacks(
                    StackName=stack_name
                )
                stackstatus = status['Stacks'][0]['StackStatus']
        except ClientError as error:
            LOGGER.info("Deleted {}".format(stack_name))  
    else:
        raise Exception(stack_name+ "Stack Name does not exist")
    
def _stack_exists(stack_name):
    stacks = client.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False

if __name__ == '__main__':
    main()
