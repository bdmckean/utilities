CREATE TABLE s3_file_info(
   id           serial PRIMARY KEY NOT NULL,
   s3_bucket    TEXT    NOT NULL,
   s3_key       TEXT    NOT NULL,
   file_size    BIGINT     NOT NULL,
   modify_date  DATE    NOT NULL,
   storage_class TEXT 
);
