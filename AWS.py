#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#*********************************************************************
#
#   NAME:
#       AWS.py
#
#   AUTHOR:
#       Josiah Earl
#
#   DESCRIPTION:
#       AWS Test Scripts
#
#
#*********************************************************************
'''

#---------------------------------------------------------------------
#                               IMPORTS
#---------------------------------------------------------------------

import argparse
import ast
import boto3
import logging
import os
import sys

#---------------------------------------------------------------------
#                               CONSTANTS
#---------------------------------------------------------------------

# Get the current directory of this script
THIS_DIR = os.path.dirname(__file__)

# Log file at a specific path
#log_file = '/tmp/script_logs/base_template_log.log'

# Log file in current directory
log_file = '{this_dir}/aws_scripts.log'.format(this_dir=THIS_DIR)

# Local file debugging output
FORMAT = '%(asctime)s %(levelname)s %(lineno)s \t%(message)s'
logging.basicConfig(filename=log_file, format=FORMAT, level=(logging.INFO))


#---------------------------------------------------------------------
#                               CLASSES
#---------------------------------------------------------------------

# *********************************************************************
#
# Class Name:
#   EC2_class
#
# Description:
#   EC2 Class Object
#
# *********************************************************************
class EC2_class(object):

    def __init__(self, instanceid):
        try:
            logging.info('Initializing class variables in EC2_class...')

            # Define self variables based on passed arguments that can be used within class
            self.instance = instanceid

            #instantiate an EC2 client
            self.EC2_Client = boto3.client('ec2')
        except Exception as exc:
            logging.error('Error occurred in EC2 init function: {}'.format(exc.message))

            raise EC2InitException(exc.message)

    def describe_instances(self):
        """
        This method describes all EC2 instances
        """
        try:
            logging.info('Running describe_instances...')

            # Call describe_instanaces
            response = self.EC2_Client.describe_instances()

            logging.info('Result of describe_instances: {}...'.format(response))

            print(response)
        except Exception as exc:
            logging.error('Error occurred in EC2 describe_instances function: {}'.format(exc.message))

            # Capture any exceptions thrown and raise an exception specific to this class method
            raise DescribeInstancesException(exc.message)

    def start_instance(self):
        """
        This method starts an EC2 instance
        """
        try:
            logging.info('Running start_instance on instance {}...'.format(self.instance))

            # Start an EC2 instance
            response = self.EC2_Client.start_instances(
                InstanceIds=['{}'.format(self.instance)],
                DryRun=False
            )

            logging.info('Result of start_instance: {}...'.format(response))

            print(response)
        except Exception as exc:
            logging.error('Error occurred in EC2 start_instance function: {}'.format(exc.message))

            # Capture any exceptions thrown and raise an exception specific to this class method
            raise StartInstancesException(exc.message)

    def stop_instance(self):
        """
        This method stops an EC2 instance
        """
        try:
            logging.info('Running stop_instance on instance: {}...'.format(self.instance))

            # Stop an EC2 instance
            response = self.EC2_Client.stop_instances(
                InstanceIds=['{}'.format(self.instance)],
                DryRun=False
            )

            logging.info('Result of stop_instance: {}...'.format(response))

            print(response)
        except Exception as exc:
            logging.error('Error occurred in EC2 stop_instance function: {}'.format(exc.message))

            # Capture any exceptions thrown and raise an exception specific to this class method
            raise StopInstancesException(exc.message)

# *********************************************************************
#
# Class Name:
#   S3_class
#
# Description:
#   S3 Class Object
#
# *********************************************************************
class S3_class(object):

    def __init__(self):
        # Define self variables based on passed arguments that can be used within class

        try:
            logging.info('Initializing class variables in S3_class...')

            # Instantiate an S3 client
            self.S3 = boto3.client('s3')
        except Exception as exc:
            logging.error('Error occurred in S3_class init function: {}'.format(exc.message))

            raise S3InitException(exc.message)

    def create_bucket(self, bucket_name):
        """
        This method creates an S3 bucket
        """
        try:
            logging.info('Running create_bucket in S3_class...')

            # Create an S3 bucket
            response = self.S3.create_bucket(Bucket='{}'.format(bucket_name),
                                  CreateBucketConfiguration={'LocationConstraint': 'us-east-2'})

            logging.info('Result of create_bucket: {}...'.format(response))

            print(response)
        except Exception as exc:
            logging.error('Error occurred in S3 create_bucket function: {}'.format(exc.message))

            # Capture any exceptions thrown and raise an exception specific to this class method
            raise CreateBucketException(exc.message)

    def list_buckets(self):
        """
        This method lists S3 buckets in an AWS instance
        """
        try:
            logging.info('Running list_buckets in S3_class...')

            # Call S3 to list current buckets
            response = self.S3.list_buckets()

            # Get a list of all bucket names from the response
            buckets = [bucket['Name'] for bucket in response['Buckets']]

            # Print out the bucket list
            print("Bucket List: {}".format(buckets))

            logging.info('Result of list_buckets: {response}\n\nBucket List: {bucket_list}...'.format(response=response, bucket_list=buckets))

            print(response)
        except Exception as exc:
            logging.error('Error occurred in S3 list_buckets function: {}'.format(exc.message))

            # Capture any exceptions thrown and raise an exception specific to this class method
            raise CreateBucketException(exc.message)


# *********************************************************************
#
# Class Name:
#   CF_class
#
# Description:
#   CloudFormation Class Object
#
# *********************************************************************
class CF_class(object):

    def __init__(self):
        # Define self variables based on passed arguments that can be used within class
        try:
            logging.info('Initializing class variables in CF_class...')

            # Instantiate cloudformation client
            self.CF_Client = boto3.client('cloudformation')

            # Open CloudFormation EC2 config file and store in self.CF_EC2_Template
            with open(os.path.normpath(os.path.join(THIS_DIR, 'cf_ec2.yaml')), 'r') as file:
                self.CF_EC2_Template = file.read()

            # Open CloudFormation Route53 EC2 config file and store in self.CF_Template
            with open(os.path.normpath(os.path.join(THIS_DIR, 'cf_ec2_route53.yaml')), 'r') as file:
                self.CF_EC2_Route53_Template = file.read()

            # Open CloudFormation ECS config file and store in self.CF_Template
            with open(os.path.normpath(os.path.join(THIS_DIR, 'cf_ecs_stack.yaml')), 'r') as file:
                self.CF_ECS_Template = file.read()

            # Open Route53 paramters file and store in self.route53_config
            with open(os.path.normpath(os.path.join(THIS_DIR, 'route53_config.json')), 'r') as file:
                self.route53_config = ast.literal_eval(file.read())
        except Exception as exc:
            logging.error('Error occurred in CF_class init function: {}'.format(exc.message))

            raise CloudFormationInitException(exc.message)

    def build_cf_ec2_stack(self):
        """
        This method builds a CF stack based on a CF template
        """
        try:
            logging.info('Building EC2 cloudformation stack...')

            response = self.CF_Client.create_stack(
                StackName='teststack',
                TemplateBody=self.CF_EC2_Template,
                Parameters=[
                    {
                        'ParameterKey': 'KeyName',
                        'ParameterValue': 'testkeypair'
                    },
                    {
                        'ParameterKey': 'InstanceType',
                        'ParameterValue': 't2.micro'
                    },
                ]
            )

            logging.info('Result of stack building: {}...'.format(response))

            print(response)
        except Exception as exc:
            logging.error('Error occurred in CF_class build_cf_ec2_stack function: {}'.format(exc.message))

            # Capture any exceptions thrown and raise an exception specific to this class method
            raise BuildCFStackException(exc.message)

    def build_cf_ec2_route53_stack(self):
        """
        This method builds a CF stack with route53 based on a CF template.
        Note: You need to create a Hosted Zone in AWS before running this method.
        """
        try:
            logging.info('Building EC2 cloudformation stack with Route 53 route...')

            response = self.CF_Client.create_stack(
                StackName='testroute53stack',
                TemplateBody=self.CF_EC2_Route53_Template,
                Parameters=self.route53_config
            )

            logging.info('Result of stack building: {}...'.format(response))

            print(response)
        except Exception as exc:
            logging.error('Error occurred in CF_class build_cf_ec2_route53_stack function: {}'.format(exc.message))

            # Capture any exceptions thrown and raise an exception specific to this class method
            raise BuildCFStackException(exc.message)

    def build_cf_ecs_stack(self):
        """
        This method builds a CF ECS stack
        """
        try:
            logging.info('Building ECS cloudformation stack...')

            response = self.CF_Client.create_stack(
                StackName='testecsstack',
                TemplateBody=self.CF_ECS_Template,
                Parameters=[
                    {
                        'ParameterKey': 'InstanceType',
                        'ParameterValue': 't2.micro'
                    },
                ],
                Capabilities=['CAPABILITY_IAM']
            )

            logging.info('Result of stack building: {}...'.format(response))

            print(response)
        except Exception as exc:
            logging.error('Error occurred in CF_class build_cf_ecs_stack function: {}'.format(exc.message))

            # Capture any exceptions thrown and raise an exception specific to this class method
            raise BuildCFStackException(exc.message)

    def destroy_cf_stack(self):
        """
        This method destroys a CF stack
        """
        try:
            logging.info('Running destroy_cf_stack...')

            response = self.CF_Client.delete_stack(
                StackName='testecsstack'
            )

            logging.info('Result of destroy_cf_stack: {}...'.format(response))

            print(response)
        except Exception as exc:
            logging.error('Error occurred in CF_class destroy_cf_stack function: {}'.format(exc.message))

            # Capture any exceptions thrown and raise an exception specific to this class method
            raise BuildCFStackException(exc.message)

class BaseException(Exception):
    """A base exception that all other exceptions should inherit from."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class EC2InitException(BaseException):
    """A child exception for the EC2 class init method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class DescribeInstancesException(BaseException):
    """A child exception for the describe_instances method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class StartInstancesException(BaseException):
    """A child exception for the start_instance method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class StopInstancesException(BaseException):
    """A child exception for the stop_instance method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class S3InitException(BaseException):
    """A child exception for the S3 class init method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class CreateBucketException(BaseException):
    """A child exception for the create_bucket method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class ListBucketsException(BaseException):
    """A child exception for the list_buckets method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class CloudFormationInitException(BaseException):
    """A child exception for the CF Init method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class BuildCFStackException(BaseException):
    """A child exception for the CF build_stack method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below

class DestroyCFStackException(BaseException):
    """A child exception for the CF destroy_stack method."""
    # If you want to include additional logic or fucntions within this inherited exception, do this below


#---------------------------------------------------------------------
#                               PROCEDURES
#---------------------------------------------------------------------


# *********************************************************************
#
# Procedure Name:
#   create_argparser
#
# Description:
#   Procedure that creates an argparser object from passed arguments
#
# *********************************************************************
def create_argparser(parser=None):

    if parser is None:
        parser = argparse.ArgumentParser()

    # Add arguments per the below example
    """parser.add_argument(
        '--service_name',
        help='The name of the service you are requesting status for'
    )"""

    return parser

# *********************************************************************
#
# Procedure Name:
#   main
#
# Description:
#   Entrypoint procedure that runs all other procedures
#
# *********************************************************************
def main(args=None):
    try:
        logging.info('Starting procedures...')

        if args:
            # Create parser
            parser = create_argparser()

            # Parse args (if exist)
            parsed_args = parser.parse_args(args)

        logging.info('Creating class objects...')

        # Create EC2 class object
        ec2_class_obj = EC2_class('<instance ID here>')

        # Create S3 class object
        s3_class_obj = S3_class()

        # Create CloudFormation class object
        cf_class_obj = CF_class()

        # Call class methods
        # Uncomment below lines to run methods

        #ec2_class_obj.describe_instances()
        #ec2_class_obj.stop_instance()
        #ec2_class_obj.start_instance()
        #s3_class_obj.create_bucket('testbucket12r1o2ur2')
        #s3_class_obj.list_buckets()
        #cf_class_obj.build_cf_ec2_stack()
        #cf_class_obj.build_cf_ec2_route53_stack()
        #cf_class_obj.build_cf_ecs_stack()
        #cf_class_obj.destroy_cf_stack()

        logging.info('Done!')
    except Exception as exc:
        logging.error('Error occurred in Main function: {}'.format(exc.message))

        print('Error encountered: {}'.format(exc.message))
        sys.exit(1)


# Entrypoint of script
if __name__ == "__main__":
    # If using arguments, change to main(sys.argv[:1])
    main(sys.argv[:0])