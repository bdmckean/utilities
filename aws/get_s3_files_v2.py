''' scans everything in s3, gets info and writes to a file '''
import boto3

def enumerate_s3():
    s3 = boto3.resource('s3')
    for bucket in s3.buckets.all():
        print("Name: {}".format(bucket.name))
        print("Creation Date: {}".format(bucket.creation_date))
        for object in bucket.objects.all():
            print("Object: {}".format(object))
            print("Object bucket_name: {}".format(object.bucket_name))
            print("Object key: {}".format(object.key))
            print("Object keys {}".format(object.__dict__))
            break
        this_bucket = s3.Bucket(bucket)
        for object in bucket.objects.all():
            print(object.key, object.storage_class, object.size, object.last_modified)
            print(object.__dict__)
            break
        break

def main():
    print("start")
    enumerate_s3()


if __name__ == '__main__':
    main()
