''' scans everything in s3, gets info and writes to a file '''
import boto3

s3 = boto3.resource('s3')
s3client = boto3.client('s3')


timestamp = datetime.datetime.today().isoformat(timespec='seconds')

out_file = 's3_file_list_{0}.txt'.format(timestamp)

response = s3client.list_buckets()
# print(response)


with open (out_file, 'w') as out_f:
    for bucket in response["Buckets"]:
        # Create a paginator to pull 1000 objects at a time
        paginator = s3client.get_paginator('list_objects')
        pageresponse = paginator.paginate(Bucket=bucket["Name"])
        out_f.write('+++++\n')
        out_f.write(str(bucket) + '\n')
        out_f.write('+++++\n')

        # PageResponse Holds 1000 objects at a time and will continue to repeat in chunks of 1000.
        for pageobject in pageresponse:
            out_f.write('----\n')
            out_f.write('----\n')
            if 'Contents' in pageobject:
                for item in pageobject["Contents"]:
                    #print (item)
                    timestamp = item['LastModified'].isoformat(timespec='seconds').split('+')[0]
                    info = "s3://{0}/{1}|{2}\n".format(bucket["Name"],item['Key'],timestamp)
                    #print(info)
                    out_f.write(info)

