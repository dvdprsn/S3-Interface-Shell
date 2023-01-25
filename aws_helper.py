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
        if self.current_bucket == '':
            print("Must be in bucket!")
            return 1
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)
        try:
            # Upload the local file from user system to object path 'key'
            print("copy local to cloud (upload)")
            print(
                f"Local_file = {local_file} bucket_name = {bucket_name} key = {key}")

            self.s3.upload_file(
                local_file, bucket_name, key)
        except Exception as e:
            print("Error msg")
            print(e)
            return 1
        return 0

    # Copy cloud object to local file system
    def s3loccp(self, local_file, path):
        if self.current_bucket == '':
            print("Must be in bucket!")
            return 1
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)
        try:
            self.s3.download_file(bucket_name, key, local_file)
            print("Copy from cloud object to local files (Download)")
            print(
                f"Bucket Name = {bucket_name} Key = {key} local_file = {local_file}")

        except Exception as e:
            print(f"failed to download {e}")
            return 1
        return 0

    # Create bucket
    def create_bucket(self, path):
        bucket_name = split_path(1, self, path)
        try:
            # Check for bucket config defaults
            print("Create bucket")
            print(f"Bucket name = {bucket_name}")
            self.s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration={
                                  'LocationConstraint': 'ca-central-1'})
        except Exception as e:
            print("Error msg")
            print(e)
            return 1
        return 0

    # Create directory/folder
    def create_folder(self, path):
        if self.current_bucket == '':
            print("Must be in bucket!")
            return 1
        # Direct path (eg - /[bucketname]/video/cats)
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)

        try:
            self.s3.put_object(Bucket=bucket_name, Key=key)

            print("Creating a new folder!")
            print(f"bucket = {bucket_name} , key = {key}")
        except Exception as e:
            print({e})
            print("Cannont create directory")
            return 1
        return 0

    # change directory
    # ! MUST BE ABLE TO HANDLE ../PATH
    def chlocn(self, path):
        # Set default values
        new_cwd = self.cwd
        new_bucket = self.current_bucket
        # ! Error when at root and do 'chlocn cats'
        if len(path.parts) == 0:
            print("Error: must specify a path")
            return 1
        if path.parts[0] == '/' and len(path.parts) == 1 or path.parts[0] == '~':
            new_cwd = pathlib.Path('/')
            new_bucket = ''
            self.cwd = new_cwd
            self.current_bucket = new_bucket
            return 0
        elif '..' in path.parts:
            # Change this to for each part
            # Then if .. move to parent
            # else move into dir
            for i in range(len(path.parts)):
                if path.parts[i] == "..":
                    new_cwd = new_cwd.parent
                else:
                    new_cwd = new_cwd / path.parts[i]
            if len(new_cwd.parts) == 1:
                new_bucket = ''
        else:
            bucket_name = split_path(1, self, path)
            if bucket_name == '':
                print("Error: Must have a bucket specified")
                return 1
            key = split_path(0, self, path)
            new_path = pathlib.Path('/'+bucket_name+'/'+key)

            new_bucket = bucket_name
            new_cwd = new_path
        print(f"{new_cwd}")
    # ! Check if new bucket and cwd exists before setting
        if object_exists(self, new_cwd) == 0:

            self.cwd = new_cwd
            self.current_bucket = new_bucket
            return 0
        print("Error: Failed to find directory or bucket")
        return 1

    def cwlocn(self):
        print(f"{self.cwd}")

    # list buckets, directories, objects

    # copy objects
    def s3copy(self, path, new_path):
        if self.current_bucket == '':
            print("Must be in bucket!")
            return 1
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)
        copy_source = {'Bucket': bucket_name, 'Key': key}

        dest_bucket_name = split_path(1, self, new_path)
        dest_key = split_path(0, self, new_path)
        if (new_path.suffix == '' and path.suffix != '') or (new_path.suffix != '' and path.suffix == ''):
            print("Error could not copy, must maintain a file extention")
            return 1
        try:
            self.s3.copy_object(Bucket=dest_bucket_name,
                                CopySource=copy_source, Key=dest_key)

            print(f"src bucket: {bucket_name} src key: {key}")
            print(f"dest bucket: {dest_bucket_name} dest key: {dest_key}")
        except Exception as e:
            print(f"Failed to copy file to new S3 loc {e}")
            return 1
        return 0

    # delete object
    def s3delete(self, path):
        if self.current_bucket == '':
            print("Must be in bucket!")
            return 1
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)

        try:
            print("Delete obj")
            print(f"Path = {key}, current bucket= {bucket_name}")
            self.s3_res.Object(bucket_name, key).delete()

        except Exception as e:
            print(f"Unable to delete path {e}")

    # Delete bucket
    # ? Should we empty bucket then delete or just throw error for buckets with content?

    def delete_bucket(self, path):
        bucket_name = split_path(1, self, path)
        # Grab bucket_name from the path stucture thats passed in
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
            print("Delete bucket")
            print(f"bucket name = {bucket_name}")
        except Exception as e:
            print("Cannont delete bucket!")
            print(e)
            return 1
        return 0

    def list_all(self, path, perms):
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)

        if bucket_name != '':
            try:
                my_bucket = self.s3_res.Bucket(bucket_name)
                for object_summary in my_bucket.objects.filter(Prefix=key):
                    if perms == 1:
                        print(
                            f"{object_summary.key} --> {self.s3_res.ObjectAcl(bucket_name, object_summary.key).grants}")
                    else:
                        print(object_summary.key)
            except Exception as e:
                print(f"{e}")
                return 1
        else:
            list_buckets(self)
 # Will use for moving locations in file system and validating that new loc exists


def list_buckets(aws):
    print("Buckets: ")
    s3 = aws.s3_res
    try:
        for bucket in s3.buckets.all():
            print(bucket.name)
    except Exception as e:
        print(f"{e}")


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
    except Exception as e:
        print(f"{e}")

    if key != "":
        try:
            for obj in bucket.objects.all():
                if key in obj.key:
                    return 0
        except Exception as e:
            print(e)
            return 1
    else:
        return 0
    return 1


def split_path(b_out, aws, path):
    if len(path.parts) == 0:
        bucket_name = aws.current_bucket
        key = str(pathlib.Path(*aws.cwd.parts[2:]))
    elif len(path.parts) == 1 and path.parts[0] == '/':
        bucket_name = ''
        key = '/'
    elif path.parts[0] == '/':
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
        if key == './' or key == ".":
            return ''
        return key
