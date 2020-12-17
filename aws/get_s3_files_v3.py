""" scans everything in s3, gets info and writes to a file """
import boto3
import datetime

s3 = boto3.resource("s3")
s3client = boto3.client("s3")


timestamp = datetime.datetime.today().isoformat(timespec="seconds")

# Make list of all s3 files
out_file = "s3_file_list_v3_{0}.txt".format(timestamp)
# Keep track of total size used in each buicket
bucket_file = "s3_bucket_list_v3_{0}.txt".format(timestamp)
# print(response)

# Limit is set lower to test operation on a few files
limit = 10000000000
# limit = 10
count = 0
bucket_size = 0


bucket_f = open(bucket_file, "w")
with open(out_file, "w") as out_f:
    s3 = boto3.resource("s3")
    for bucket in s3.buckets.all():
        print("Name: {}".format(bucket.name))
        print("Creation Date: {}".format(bucket.creation_date))
        print(count)

        for item in bucket.objects.all():
            timestamp = item.last_modified.isoformat(timespec="seconds").split("+")[0]
            info = "s3://{0}|/{1}|{2}|{3}|{4}\n".format(
                bucket.name, item.key, item.size, timestamp, item.storage_class
            )

            # print(info)
            if int(item.size) > 0:
                bucket_size += item.size
                out_f.write(info)
            count += 1
            if count > limit:
                break
        bucket_line = "{0}|{1:15.2f}|GB\n".format(
            bucket.name, bucket_size / 1024 / 1024 / 1024
        )
        bucket_f.write(bucket_line)
        bucket_f.flush()
        out_f.flush()
        bucket_size = 0
        if count > limit:
            break

print(count, limit)
