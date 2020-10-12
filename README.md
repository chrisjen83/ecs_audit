# ECS Audit Exporter

ECS Audit Exporter is a python script designed to export via the  ECS Management API all audit events which have occurred in a 24hr period on the day the script runs within a specific namespace.

All audit information is exported and written to an S3 bucket in a JSON file format.  The file name will have the date the information was exported and use the audit prefix.

To run this script you will need to have an ECS management user with the sysadmin privileges and have an S3 bucket created with an object user who can write to that bucket.

## Preparation
This script will run on any operating system which can support python 3.8, if you are running this script on a non-Linux based system an alternative scheduler will need to be selected.

This script will need the following modules installed via PIP:

* JSON
* Boto3
* Python-ECSClient

## Installation
1. Clone this GitHub repository to the machine you will run the script on. Make sure that audit.py and master_audit_config.ini is in the same folder.

2. To configure this script to run you will need to fill out all setting’s in the master_audit_config.ini.  audit.py will require that all settings are filled out for the script to run correctly.
```
[MANAGEMENT]
USERNAME:
PASSWORD:
ENDPOINT: https://<IP OR FQDN>:4443
TOKEN_ENDPOINT: https://<IP OR FQDN>:4443/login

[S3]
ACCESSKEY:
SECRET:
BUCKET:
ENDPOINT: https:<IP OR FQDN>//:9021
SSL_VERIFY: False

[AUDIT]
NAMESPACE: <ECS NAMESPACE TO READ AUDIT LOGS FROM>
MAXEVENTS: 1000
```

3. Once you have filled out all settings in the master_audit_config.ini you will need to rename master_audit_config.ini to audit_config.ini keeping it in the same folder as audit.py.

> Note: This script will rely on the Timezone set on the ECS cluster and not the machine this script is running on.

4. Lastly for this script to run on a daily schedule you will need to add this script to a CRON process on your server.

> Note: You can run this script on demand from the command line by typing ` # python audit.py`.  If you run this command repeatedly within the same 24hr period the same information will be exported.


