bucket = "aii-data"
prefix = "v1"
s3_client = boto3.client("s3")
response = s3_client.list_objects(Bucket=bucket, Prefix=prefix)
for file in response["Contents"]:
    if file["StorageClass"] == "STANDARD":
        name = file["Key"].rsplit("/", 1)
        if name[1] != "":
            file_name = name[1]
            obj = s3_client.get_object(Bucket=bucket, Key=prefix + file_name)
            body = obj["Body"]
            lns = []
            i = 0
            with gzip.open(body, "rt") as gf:
                for ln in gf:
                    i += 1
                    lns.append(ln.rstrip())
                    if i == 10:
                        break
