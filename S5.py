import os
import sys
import pathlib
import aws_helper

# Check Response from S3 requests to make the errors since they wont always throw


def main():
    s3_client = aws_helper.AWS()
    # Testing Paths, Direct and relative
    path = pathlib.Path('/dpears04b02/videos/cats/test/readme.md')
    path2 = pathlib.Path('extra/read/all/about')
    path_exists = pathlib.Path('/dpears04b02/videos')
    # ! Testing for creating folders

    s3_client.cwd = pathlib.Path('/dpears04b02')
    s3_client.current_bucket = 'dpears04b02'
    s3_client.create_folder(path_exists)
    # s3_client.s3delete(path_exists)

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
