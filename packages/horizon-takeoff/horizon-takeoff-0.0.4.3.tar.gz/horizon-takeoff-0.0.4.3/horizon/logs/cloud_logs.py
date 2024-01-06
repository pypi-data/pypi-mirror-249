# ------ UNDER DEVELOPMENT

import boto3

# Initialize the CloudWatch Logs client
cloudwatch = boto3.client(
    "logs", region_name="us-east-1"
)  # Replace 'us-east-1' with your desired region

# Specify the log group name and log stream name for your SageMaker endpoint
log_group_name = "/aws/sagemaker/Endpoints/takeoff-endpoint"
log_stream_name = "AllTraffic/i-0a3687981090f"

# Retrieve the CloudWatch logs
response = cloudwatch.get_log_events(
    logGroupName=log_group_name,
    logStreamName=log_stream_name,
    limit=10,  # Adjust the limit as needed
)

# Print the log events
for event in response["events"]:
    print(event["timestamp"], event["message"])
