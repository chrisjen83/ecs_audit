#!/usr/bin/env python

# This is a script to take the audit logs for a specific namespace in Dell EMC
# ECS into a bucket.  This script will capture a full 24hrs of audit logs and
# write to a json file.

from ecsclient.client import Client
from ecsclient.common.monitoring import events
import datetime
import requests
import boto3
import json
import configparser

# Reading in config.ini into the script to be used to connect to ECS.
config = configparser.ConfigParser()
config.read('audit_config.ini')

mgnt_user = config['MANAGEMENT']['USERNAME']
mgnt_pass = config['MANAGEMENT']['PASSWORD']
mgnt_endpoint = config['MANAGEMENT']['ENDPOINT']
token_endpoint = config['MANAGEMENT']['TOKEN_ENDPOINT']

s3_accesskey = config['S3']['ACCESSKEY']
s3_secret = config['S3']['SECRET']
s3_bucket = config['S3']['BUCKET']
s3_endpoint = config['S3']['ENDPOINT']
ssl_verify = config['S3']['SSL_VERIFY']

audit_namespace = config['AUDIT']['NAMESPACE']
audit_maxevents = config['AUDIT']['MAXEVENTS']


# This creates the Management API authentication and token caching to use later
client = Client('3',
                username=mgnt_user,
                password=mgnt_pass,
                token_endpoint=token_endpoint,
                ecs_endpoint=mgnt_endpoint)

class S3JsonBucket:
    def __init__(self, bucket_name):
        self.bucket = boto3.resource(service_name='s3', verify=False, aws_access_key_id=s3_accesskey,
                            aws_secret_access_key=s3_secret, endpoint_url=s3_endpoint).Bucket(bucket_name)

    def load(self, key):
        return json.load(self.bucket.Object(key=key).get()["Body"])

    def dump(self, key, obj):
        return self.bucket.Object(key=key).put(Body=json.dumps(obj), ContentType = 'application/json')

def export_it():
    jsbucket = S3JsonBucket('{}'.format(s3_bucket))
    datetime_object = datetime.date.today()

    # Connect to the ECS Management API and request the audit logs for a specific namespace in a 24hr period
    ev = events.Events(client)
    auditOut = ev.get_audit_events('{}T00:00'.format(datetime_object), '{}T23:59'.format(datetime_object), '{}'.format(audit_namespace), '{}'.format(audit_maxevents))

    # Dump the data from the audit API into a JSON file and upload to an S3 bucket.
    jsbucket.dump('audit/audit-{}.json'.format(datetime_object), auditOut)

    # JSON will be read back and compared to original output request
    read_data = jsbucket.load('audit/audit-{}.json'.format(datetime_object))
    assert read_data == auditOut

export_it()

# Remove cached Token, this will for a re-login next time
client.remove_cached_token()
