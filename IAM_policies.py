###install the necessary dependencies to run script successfully
#sudo apt install python3-pip / boto3 depends on Python pip package
#pip install boto3
#sudo apt install awscli
#"aws configure" to add access and secret keys
#"aws iam list-policies" to check the iam policy dictionary list
#export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID to set environment variable
#export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY to set environment variable
#export AWS_DEFAULT_REGION=YOUR_AWS_DEFAULT_REGION to set environemnt variable

_____________________________________________________________________________________________

#import the necessary libraries and print the system path.
#simple way to interact with API's and other services in AWS
import boto3
import csv
import os
#not necessary but good for resource access 
import sys
#prints the list of directories that Python parses through to find modules and packages to return the data/function being called  
print(sys.path)

# Set your AWS credentials (export first to define variables first)
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY'] 

#create a boto3 client for IAM
iam_client = boto3.client("iam", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
# list the IAM policies
policies = iam_client.list_policies()["Policies"]
#create a paginator to iterate over the roles.
paginator = iam_client.get_paginator('list_roles')
#define csv_file outside of function so that the whole script can access it not just the function 
csv_file = None

#creates a response iterator is an object used to iterate through a large response set that may not be able to save to memory
#defines parameters for paginate method 
response_iterator = paginator.paginate(
    #sets role name to iam to see all the iam roles and their policies
    RoleName='iam',
    #dictionary that configures the pagination method
    PaginationConfig={
        'MaxItems': 123,
        'PageSize': 123,
        'StartingToken': 'string'
    }
)

#Creates a CSV file with variable to reference later from a list of IAM policies.
def CreateCSVfile_IAM_policies(policies, output_file="iam_policies.csv"):
  
  #can refer to variable = global csv_file if needed
  
  #handles if there is an error 
  try:
    csv_file = open(output_file, "w", encoding = "UTF8", newline='')
    writer = csv.writer(csv_file)

    # Write the header row.
    writer.writerow(["Policy Name", "Policy ID", "Arn"])

    #handles if there are errors / will print out the error / built in IOError class
  except IOError as e:
      print("Error opening CSV file:", e)
      #exit the script with error message above
      sys.exit(1)

    # Iterate through the policies and write each policy to the CSV file.
  for policy in policies:
        writer.writerow([policy["PolicyName"], policy["PolicyId"], policy["Arn"]])
  
print('CSV Created')

# If policies list is not empty, the function creates the CSV file. file will close automatically close when the function is returned so resources can be accessed
if policies:
    CreateCSVfile_IAM_policies(policies)
