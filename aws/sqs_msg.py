import boto3
import json 

# Create SQS client
sqs = boto3.client('sqs')


queue_url = 'https://sqs.us-east-1.amazonaws.com/874847117436/test-charlie-ingest-queue'
#queue_url = 'https://sqs.us-east-1.amazonaws.com/874847117436/charlie-ingest-queue'
#msg = '{"message": "satellite_ingest_started", "satellite": "charlie", "ingest_id": 7, "manifest_file": "s3://zz-test-aii-data/v1/dev/space/charlie/tar_files/2021-03-19T08:59:05/manifest.json"}'
msg = '{"message": "satellite_ingest_started", "satellite": "charlie", "ingest_id": 24, "manifest_file": "s3://zz-test-aii-data/v1/dev/space/charlie/tar_files/2021-03-22T08:57:35/manifest.json"}'
do_all = False
if do_all:
    recieve = True
    delete = True
    send = True
else:
    recieve = False
    delete = False
    send = True

#recieve = True
#delete = True
#send = False

if recieve:
    # Receive message from SQS queue
    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=[
            'SentTimestamp'
        ],
        MaxNumberOfMessages=1,
        MessageAttributeNames=[
            'All'
        ],
        VisibilityTimeout=0,
        WaitTimeSeconds=0


    )
    message = response['Messages'][0]
    receipt_handle = message['ReceiptHandle']

    msg = message['Body']
    print('Received message: %s' % message)

if delete:
    # Delete received message from queue
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    print('Dleted message: %s' % message)

if send:
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=(msg)
    )

    print(f"Sent message again {response['MessageId']}")
