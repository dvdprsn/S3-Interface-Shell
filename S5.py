# import os
# import sys
import pathlib
import aws_helper
import shlex

# Check Response from S3 requests to make the errors since they wont always throw


def main():
    s3_client = aws_helper.AWS()

    # ! TODOS:
    # Create a help cmd
    # Add better error checking for inputs
    # Ensure that a bucket is selected before other cmds are execd
    # Expand error messages
    #
    # ! Main loop
    while True:
        cmd_og = input("S3> ")
        # We use shlex here to ensure that paths like '/test/example path/readme.md'
        # is not split over the space in the path so long as it is put in quotes
        # ex. chlocn "/bucket-name/image folder/cats"

        cmd = shlex.split(cmd_og)
        if cmd[0] == "exit" or cmd == "quit":
            print("Exiting S5")
            exit(0)
        elif "create_bucket" in cmd:
            # path
            s3_client.create_bucket(pathlib.Path(cmd[1]))
        elif "create_folder" in cmd:
            # path
            s3_client.create_folder(pathlib.Path(cmd[1]))
        elif "locs3cp" in cmd:
            # local_file, path
            s3_client.locs3cp(pathlib.Path(cmd[1]), pathlib.Path(cmd[2]))
        elif "s3loccp" in cmd:
            # local_file, path
            s3_client.s3loccp(pathlib.Path(cmd[2]), pathlib.Path(cmd[1]))
        elif "chlocn" in cmd:
            # path
            s3_client.chlocn(pathlib.Path(cmd[1]))
        elif "cwlocn" in cmd:
            # nothing
            s3_client.cwlocn()
        elif "list" in cmd:
            # NOT DONE YET
            # ! TODO
            s3_client.list_buckets()
        elif "s3copy" in cmd:
            # path, new_path
            s3_client.s3copy(pathlib.Path(cmd[1]), pathlib.Path(cmd[2]))
        elif "s3delete" in cmd:
            # path
            s3_client.s3delete(pathlib.Path(cmd[1]))
        elif "delete_bucket" in cmd:
            # bucket_name
            s3_client.delete_bucket(pathlib.Path(cmd[1]))
        else:
            aws_helper.exec_sys_cmd(cmd_og)


if __name__ == "__main__":
    main()
