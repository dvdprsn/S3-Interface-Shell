import boto3

class AWS:
    def __init__(self):
        self.client = None
        self.pwd = ''
        self.current_bucket = ''
        
        print("Welcome to AWS S3 Storage Shell (S5)")
        try:
            self.client = boto3.client('s3')
        except Exception as e:
            print("You could not be connected to your S3 storage")
            print("Please review procedures for authenticating your account on AWS S3")
            exit(0)
        print(f"You are now connected to your S3 storage on region {self.client.meta.region_name}")
        
    # Copy local file to cloud location
    def locs3cp(self):
        pass
    
    # Copy cloud object to local file system
    def s3loccp(self):
        pass
    
    # Create bucket
    def create_bucket(self, bucket_name):
        try:
            self.client.create_bucket(Bucket=bucket_name)
        except Exception as e:
            print("Error msg")
            return 1
        return 0
    
    # Create directory/folder
    def create_folder(self, path):
        path_list = path.split('/')

        # TODO must be a way to clean this up
        if path[0] == "/":
            bucket_name = path_list[1]
            path_list.pop(0)
            path_list.pop(0)
            key = '/'.join(path_list)
            key += '/'
        else:
            bucket_name = self.current_bucket
            key = self.pwd.split('/')
            key.pop(0)
            key.pop(0)
            key = '/'.join(key)
            key += '/' + path + '/'
                
        # print(f"bucket = {bucket_name} , key = {key}")
        try:
            self.client.put_object(Bucket=bucket_name, Key=key)
        except Exception as e:
            print({e})
            print("Cannont create directory")
            return 1
        return 0 
    
    # change directory
    def chlocn(self, path):
        if path == '/' or path == '~':
            self.pwd = ''
            return 0
        elif path == '..':
            pwd_list = self.pwd.split('/')
            pwd_list.pop()
            self.pwd = '/'.join(pwd_list)
            return 0
        
        if self.pwd == "":
            path_list = path.split('/')
            path_list.pop(0)
            for path_elem in path_list:
                pass
            # TODO left off here
        # path_list = path.split('/')
        # pass
    
    # current working directory or location
    def cwlocn(self):
        print(f"/{self.pwd}")

    # list buckets, directories, objects
    def list_buckets(self):
        print("Buckets: ")
        response = self.client.list_buckets()['Buckets']
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
    def delete_bucket(self, bucket_name):
        try:
            self.client.delete_bucket(Bucket=bucket_name)
        except Exception as e:
            print("Cannont create bucket")
            return 1
        return 0 

    def list_contents(self, bucket_name):
        for key in self.client.list_objects(Bucket=bucket_name)['Contents']:
            print(key['Key'])
    
    
def main():
    s3_client = AWS()
    
    # ! Testing for creating folders
    s3_client.create_folder('/dpears04b01/images/cats')
    s3_client.current_bucket = 'dpears04b01'
    s3_client.pwd = '/dpears04b01/temp'
    s3_client.create_folder('cat-videos')
    
    s3_client.chlocn("..")
    # s3_client.cwlocn()
    # s3_client.list_buckets()
    # s3_client.list_contents()
    
    # ! Main loop
    # while True:
    #     cmd = input("S3> ")
    #     if cmd == "exit" or cmd == "quit":
    #         print("Exiting S5")
    #         exit(0)
        
    #     if "create_bucket" in cmd:
    #         cmd = cmd.replace('/','').split(" ")
    #         print(cmd[1])
    #         s3_client.create_bucket(cmd[1])
            
    #     if "create_folder" in cmd:
    #         cmd = cmd.split(" ")
    #         s3_client.create_folder(cmd[1])
            
if __name__ == "__main__":
    main()