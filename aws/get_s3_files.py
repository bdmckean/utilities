''' scans everything in s3, gets info and writes to a file '''
import boto3
import datetime

s3 = boto3.resource('s3')
s3client = boto3.client('s3')


timestamp = datetime.datetime.today().isoformat(timespec='seconds')

out_file = 's3_file_list_{0}.txt'.format(timestamp)
bucket_file = 's3_bucket_list_{0}.txt'.format(timestamp)
response = s3client.list_buckets()
#print(response)

limit = 1000000000
#limit = 10
count = 0
bucket_size = 0

bucket_f = open(bucket_file, 'w')
with open (out_file, 'w') as out_f:
    for bucket in response["Buckets"]:
        print(bucket)
        #life_cycle = s3.BucketLifecycle(bucket)
        #print(life_cycle) 
        #life_cycle.load()

        print(count)
        # Create a paginator to pull 1000 objects at a time
        paginator = s3client.get_paginator('list_objects')
        pageresponse = paginator.paginate(Bucket=bucket["Name"])
        #out_f.write('+++++\n')
        #out_f.write(str(bucket) + '\n')
        #out_f.write('+++++\n')

        # PageResponse Holds 1000 objects at a time and 
        # will continue to repeat in chunks of 1000.
        for pageobject in pageresponse:
            #out_f.write('----\n')
            #out_f.write('----\n')
            if 'Contents' in pageobject:
                for item in pageobject["Contents"]:
                    #print (item)
                    key = s3.Object( bucket["Name"], item['Key'])
                    storage_class = key.storage_class

                    timestamp = item['LastModified'].isoformat(timespec='seconds').split('+')[0]
                    info = "s3://{0}|/{1}|{2}|{3}|{4}\n".format(
                        bucket["Name"],
                        item['Key'],
                        item['Size'],
                        timestamp,
                        storage_class)

                    #print(info)
                    if int(item['Size']) > 0:
                        bucket_size += item['Size']
                        out_f.write(info)
                    count += 1
                    if count > limit:
                        break
                if count > limit:
                    break
            if count > limit:
                break
        bucket_line = '{0}|{1:15.2f}|GB\n'.format(
            bucket["Name"],
            bucket_size / 1024 / 1024 / 1024)
        bucket_f.write(bucket_line)
        bucket_f.flush()
        out_f.flush()
        bucket_size = 0        
        if count > limit:
            break

print(count, limit)
