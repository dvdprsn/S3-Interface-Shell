import configparser
import os
import sys
import pathlib
import boto3


class AWS:

    def __init__(self):

        self.s3 = None
        self.s3_res = None
        self.cwd = pathlib.Path('/')
        self.current_bucket = ''

        config = configparser.ConfigParser()
        config.read("S5-S3.conf")
        aws_access_key_id = config['default']['aws_access_key_id']
        aws_secret_access_key = config['default']['aws_secret_access_key']

        print("Welcome to AWS S3 Storage Shell (S5)")
        try:
            session = boto3.Session(
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key
            )
            self.s3 = session.client('s3')
            self.s3_res = session.resource('s3')
        except Exception as e:
            print("You could not be connected to your S3 storage")
            print("Please review procedures for authenticating your account on AWS S3")
            print(e)
            exit(0)
        print(
            f"You are now connected to your S3 storage on region {self.s3.meta.region_name}")

    # Copy local file to cloud location
    def locs3cp(self, local_file, path):
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)
        try:
            # Upload the local file from user system to object path 'key'
            self.s3.upload_file(
                local_file, bucket_name, key)
        except Exception as e:
            print("Error msg")
            print(e)
            return 1
        return 0

    # Copy cloud object to local file system
    def s3loccp(self, local_file, path):
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)
        try:
            self.s3.download_file(bucket_name, key, local_file)
        except Exception as e:
            print(f"failed to download {e}")
            return 1
        return 0

    # Create bucket
    def create_bucket(self, path):
        bucket_name = path.parts[1]
        try:
            # Check for bucket config defaults
            self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                                  'LocationConstraint': 'ca-central-1'})
        except Exception as e:
            print("Error msg")
            print(e)
            return 1
        return 0

    # Create directory/folder
    def create_folder(self, path):
        # Direct path (eg - /[bucketname]/video/cats)
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)

        try:
            # self.s3.put_object(Bucket=bucket_name, Key=key)
            print("Creating a new folder!")
            print(f"bucket = {bucket_name} , key = {key}")
        except Exception as e:
            print({e})
            print("Cannont create directory")
            return 1
        return 0

    # change directory
    def chlocn(self, path):
        # Has not entered bucket dir
        if len(self.cwd.parts) == 1:
            # Check if bucket exists before changing
            print(self.s3.head_bucket(Bucket="dpears04b2"))

        # Once we have validated that the path exists we can append
        # ! This will need to be changed depending on type of change
        self.cwd = self.cwd / path
        pass

    # current working directory or location
    def cwlocn(self):
        print(f"{self.cwd}")

    # list buckets, directories, objects
    def list_buckets(self):
        print("Buckets: ")
        response = self.s3.list_buckets()['Buckets']
        print(response)
        # for bucket in response['Buckets']:
        #     print(f'  {bucket["Name"]}')

    # copy objects
    def s3copy(self, path, new_path):
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)
        copy_source = {'Bucket': bucket_name, 'Key': key}

        dest_bucket_name = split_path(1, self, new_path)
        dest_key = split_path(0, self, new_path)
        try:
            # self.s3.copy_object(Bucket=dest_bucket_name,
            #                     CopySource=copy_source, Key=dest_key)
            # self.s3.delete_object(Bucket=bucket_name, Key=key)

            print(f"src bucket: {bucket_name} src key: {key}")
            print(f"dest bucket: {dest_bucket_name} dest key: {dest_key}")
        except Exception as e:
            print(f"Failed to copy file to new S3 loc {e}")
            return 1
        return 0

    # delete object
    def s3delete(self, path):
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)

        try:
            print(f"Path = {key}, current bucket= {bucket_name}")
            self.s3_res.Object(bucket_name, key).delete()
        except Exception as e:
            print(f"Unable to delete path {e}")

    # Delete bucket
    # ? Should we empty bucket then delete or just throw error for buckets with content?

    def delete_bucket(self, bucket_name):
        # Grab bucket_name from the path stucture thats passed in
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            print("Cannont delete bucket!")
            print(e)
            return 1
        return 0

    def list_contents(self, bucket_name):
        for key in self.s3.list_objects(Bucket=bucket_name)['Contents']:
            print(key['Key'])

 # Will use for moving locations in file system and validating that new loc exists


def exec_sys_cmd(command):
    try:
        os.system(command)
    except Exception as e:
        print(f"{e}")
        return 1
    return 0


def object_exists(aws, path):

    bucket_name = split_path(1, aws, path)
    key = split_path(0, aws, path)
    try:
        bucket = aws.s3_res.Bucket(bucket_name)

        for obj in bucket.objects.all():
            # print(f"comparing {key} v. {obj.key}")
            if key in obj.key:
                print("File path exists in system")
                return 0
    except Exception as e:
        print(e)
    return 1


def split_path(b_out, aws, path):

    if path.parts[0] == '/':
        bucket_name = path.parts[1]
        key = str(pathlib.Path(*path.parts[2:]))
        # Append slash if its a folder
        if path.suffix == '':
            key = key + '/'

    # Relative Path (eg - video/cats)
    # ! ERROR CHECK IF REL PATH IS USED BUT NO DRIVE IS SELECTED
    else:
        full_path = aws.cwd / path
        bucket_name = aws.current_bucket
        key = str(pathlib.Path(*full_path.parts[2:]))
    # append slash if its a folder
        if path.suffix == '':
            key = key + '/'

    if b_out == 1:
        return bucket_name
    else:
        return key
