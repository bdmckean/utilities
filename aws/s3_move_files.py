import boto3
s3 = boto3.resource('s3')

source_bucket = 'aii-pipeline'j:q
:q


copy_source = {
    'Bucket': 'aii-pipeline',
    'Key': 'mykey'
}
s3.meta.client.copy(copy_source, 'otherbucket', 'otherkey')
