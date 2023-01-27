import configparser
import os
import pathlib
import boto3


class AWS:

    def __init__(self):

        self.cwd = pathlib.Path('/')
        self.current_bucket = ''

        config = configparser.ConfigParser()
        config.read("S5-S3.conf")
        # Configured for the default profile!!
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
        # if self.current_bucket == '':
        #     print("Must be in bucket!")
        #     return 1
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)
        try:
            # Upload the local file from user system to object path 'key'
            print("copy local to cloud (upload)")
            # print(
            # f"Local_file = {local_file} bucket_name = {bucket_name} key = {key}")

            self.s3.upload_file(
                local_file, bucket_name, key)
        except Exception as e:
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
        bucket_name = split_path(1, self, path)
        key = split_path(0, self, path)
        try:
            self.s3.put_object(Bucket=bucket_name, Key=key)
            print("Creating a new folder!")
        except Exception as e:
            print(f"{e}")
            print("Cannont create directory")
            return 1
        return 0

    # change directory
    def chlocn(self, path):
        # Set default values
        new_cwd = self.cwd
        new_bucket = self.current_bucket
        # Cannot change path to nowhere
        if len(path.parts) == 0:
            print("Error: must specify a path")
            return 1
        # Change path back to root
        if path.parts[0] == '/' and len(path.parts) == 1 or path.parts[0] == '~':
            new_cwd = pathlib.Path('/')
            new_bucket = ''
            self.cwd = new_cwd
            self.current_bucket = new_bucket
            return 0
        # If issued path contains steps up in the directory
        elif '..' in path.parts:
            # Iterate over the path
            for i in range(len(path.parts)):
                # Move up in directory structure
                if path.parts[i] == "..":
                    new_cwd = new_cwd.parent
                else:
                    new_cwd = new_cwd / path.parts[i]
            # If we step back far enough remove bucket
            if len(new_cwd.parts) == 1:
                new_bucket = ''
        # For standard cases
        else:
            bucket_name = split_path(1, self, path)
            if bucket_name == '':
                print("Error: Must have a bucket specified")
                return 1
            key = split_path(0, self, path)
            new_path = pathlib.Path('/'+bucket_name+'/'+key)

            new_bucket = bucket_name
            new_cwd = new_path
    # ! Check if new bucket and cwd exists before setting
        if pathlib.Path(new_cwd).suffix != '':
            print("Error - must select a folder not a file!")
            return 1
        if object_exists(self, new_cwd) == 0:
            self.cwd = new_cwd
            self.current_bucket = new_bucket
            return 0
        print("Error: Failed to find directory or bucket")
        return 1

    def cwlocn(self):
        print(f"{self.cwd}")

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

            # print(f"src bucket: {bucket_name} src key: {key}")
            # print(f"dest bucket: {dest_bucket_name} dest key: {dest_key}")
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
            # Headobject should ensure that only the top of the directory can be deleted
            try:
                self.s3.head_object(Bucket=bucket_name, Key=key)
            except:
                print("Failed to locate file")
                return 1
            self.s3_res.Object(bucket_name, key).delete()
        except Exception as e:
            print(f"Unable to delete path {e}")
            return 1
        return 0
    # Delete bucket

    def delete_bucket(self, path):
        bucket_name = split_path(1, self, path)
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
            print("Delete bucket")
            # print(f"bucket name = {bucket_name}")
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
                res = self.s3.list_objects(
                    Bucket=bucket_name, Prefix=key, Delimiter='/')
                try:
                    for o in res.get("CommonPrefixes"):
                        if perms == 1:
                            print("TODO")
                        else:
                            print(o.get("Prefix").replace(key, ""))
                except:
                    pass
                try:
                    for o in res.get("Contents"):

                        if perms == 1:
                            print(
                                f"{o.get('Key').replace(key, '')}  {o.get('LastModified')}  {o.get('Size')} bytes")
                        else:
                            print(o.get("Key").replace(key, ""))
                except:
                    pass
            except Exception:
                return 1
        else:
            list_buckets(self, perms)

# List all the buckets in the users S3 account


def list_buckets(aws, verbose):
    # Get S3 resource
    s3 = aws.s3_res
    try:
        # Output all the buckets in the S3 dir
        for bucket in s3.buckets.all():
            if verbose == 1:
                print(
                    f"{bucket.name} --> {s3.BucketAcl(bucket.name).grants[0]['Permission']}")
            else:
                print(bucket.name)
    except Exception as e:
        print(f"{e}")

# For system command execution


def exec_sys_cmd(command):
    try:
        os.system(command)
    except Exception as e:
        print(f"{e}")
        return 1
    return 0


def object_exists(aws, path):
    # split bucketname and key from the input path
    bucket_name = split_path(1, aws, path)
    key = split_path(0, aws, path)
    # get bucket resource
    bucket = aws.s3_res.Bucket(bucket_name)
    # Simple error check, returns None if the bucket doesnt exists
    if not bucket.creation_date:
        return 1
    # For when we move around within a buckets contents
    if key != "":
        try:
            # aws.s3.head_object(Bucket=bucket_name, Key=key)
            # ! KEEP AN EYE ON THIS MIGHT NOT WORK
            for obj in bucket.objects.all():
                if key in obj.key:
                    return 0
            return 1
        except Exception as e:
            print(e)
            return 1
    return 0


def split_path(b_out, aws, path):
    # if path is empty - use only for list_all
    if len(path.parts) == 0:
        bucket_name = aws.current_bucket
        key = str(pathlib.Path(*aws.cwd.parts[2:])) + '/'
    # if path is the root
    elif len(path.parts) == 1 and path.parts[0] == '/':
        bucket_name = ''
        key = '/'
    # If its a direct path
    elif path.parts[0] == '/':
        bucket_name = path.parts[1]
        key = str(pathlib.Path(*path.parts[2:]))
        # Append slash if its a folder
        if path.suffix == '':
            key += '/'
    # Relative Path (eg - video/cats)
    else:
        full_path = aws.cwd / path
        bucket_name = aws.current_bucket
        key = str(pathlib.Path(*full_path.parts[2:]))
    # append slash if its a folder
        if path.suffix == '':
            key += '/'
    # change output depending on flag
    if b_out == 1:
        return bucket_name
    else:
        # Cleans the output
        if key == './' or key == ".":
            return ''
        return key
