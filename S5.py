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

    def locs3cp(self):
        pass

    # Copy cloud object to local file system
    def s3loccp(self):
        pass

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
        if path.parts[0] == '/':
            bucket_name = path.parts[1]
            key = str(pathlib.Path(*path.parts[2:])) + '/'
        # Relative Path (eg - video/cats)
        else:
            full_path = self.cwd / path
            bucket_name = self.current_bucket
            key = str(pathlib.Path(*full_path.parts[2:])) + '/'

        # print(f"bucket = {bucket_name} , key = {key}")
        try:
            # pass
            self.s3.put_object(Bucket=bucket_name, Key=key)
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
        print(f"/{self.cwd}")

    # list buckets, directories, objects
    def list_buckets(self):
        print("Buckets: ")
        response = self.s3.list_buckets()['Buckets']
        print(response)
        # for bucket in response['Buckets']:
        #     print(f'  {bucket["Name"]}')

    # copy objects
    def s3copy(self):
        pass

    # delete object
    def s3delete(self):
        pass

    # Delete bucket
    # ? Should we empty bucket then delete or just throw error for buckets with content?
    def delete_bucket(self, bucket_name):
        try:
            self.s3.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            print("Cannont create bucket!")
            print(e)
            return 1
        return 0

    def list_contents(self, bucket_name):
        for key in self.s3.list_objects(Bucket=bucket_name)['Contents']:
            print(key['Key'])


def main():
    s3_client = AWS()
    # Testing Paths, Direct and relative
    path = pathlib.Path('/dpears04b02/videos/cats/test')
    path2 = pathlib.Path('extra/read/all/about')

    # * Step back one USE LATER
    # print(path.parent)

    # ! Testing for creating folders
    s3_client.create_folder(path)

    s3_client.cwd = pathlib.Path('/dpears04b02')
    s3_client.current_bucket = 'dpears04b02'
    s3_client.create_folder(path2)

    # ! Main loop
    # while True:
    #     cmd = input("S3> ")
    #     if cmd == "exit" or cmd == "quit":
    #         print("Exiting S5")
    #         exit(0)
    #
    #     if "create_bucket" in cmd:
    #         s3_client.create_bucket(pathlib.Path(cmd))
    #
    #     if "create_folder" in cmd:
    #         s3_client.create_folder(pathlib.Path(cmd))


if __name__ == "__main__":
    main()
