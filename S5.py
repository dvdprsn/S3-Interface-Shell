# import os
# import sys
import pathlib
import aws_helper
import shlex
import readline

# Check Response from S3 requests to make the errors since they wont always throw


def print_help():

    print("----Command Help----")
    print("exit -> terminate shell")
    print(
        "locs3cp [local path] [S3 path] -> copy local file to remote S3 location")
    print("s3loccp [S3 path] [local path] -> copy remote S3 file to local")
    print("chlocn [path] -> navigate directory space")
    print("cwlocn -> output current working directory")
    print("list [-l] -> list current directory contents or specify")
    print("s3copy [org path] [new path] -> move file within S3 remote space")
    print("s3delete [path] -> delete an object from the bucket")
    print("delete_bucket [path]-> delete a bucket")
    print("create_bucket [path] -> create a new bucket")
    print("create_folder [path] -> create a new folder")
    print("for any other input command is continueed to system shell")
    print("--------")


def main():
    s3_client = aws_helper.AWS()

    # ! TODOS:
    # Create a help cmd
    # Add better error checking for inputs
    # Ensure that a bucket is selected before other cmds are execd
    # Expand error messages
    # Catch return values to output detailed error msg after cmd
    # ! Main loop
    while True:
        cmd_og = input(f"{s3_client.cwd} % S3> ")
        # We use shlex here to ensure that paths like '/test/example path/readme.md'
        # is not split over the space in the path so long as it is put in quotes
        # ex. chlocn "/bucket-name/image folder/cats"

        cmd = shlex.split(cmd_og)
        if cmd[0] == "exit" or cmd[0] == "quit":
            print("Exiting S5")
            exit(0)
        elif "create_bucket" in cmd:
            if len(cmd) < 2:
                print("invalid argument length")
                continue
            # path
            s3_client.create_bucket(pathlib.Path(cmd[1]))
        elif "create_folder" in cmd:
            # path
            if len(cmd) < 2:
                print("invalid argument length")
                continue
            s3_client.create_folder(pathlib.Path(cmd[1]))
        elif "locs3cp" in cmd:
            # local_file, path
            if len(cmd) < 3:
                print("invalid argument length")
                continue
            s3_client.locs3cp(pathlib.Path(cmd[1]), pathlib.Path(cmd[2]))
        elif "s3loccp" in cmd:
            # local_file, path
            if len(cmd) < 3:
                print("invalid argument length")
                continue
            s3_client.s3loccp(pathlib.Path(cmd[2]), pathlib.Path(cmd[1]))
        elif "chlocn" in cmd:
            # path
            if len(cmd) < 2:
                print("invalid argument length")
                continue
            s3_client.chlocn(pathlib.Path(cmd[1]))
        elif "cwlocn" in cmd:
            # nothing
            s3_client.cwlocn()
        elif "list" in cmd:
            # NOT DONE YET
            path = pathlib.Path()
            verb = 0
            if '-l' in cmd:
                verb = 1
                if len(cmd) > 2:
                    path = pathlib.Path(cmd[2])
            elif len(cmd) > 1:
                path = pathlib.Path(cmd[1])

            s3_client.list_all(path, verb)
        elif "s3copy" in cmd:
            if len(cmd) < 3:
                print("invalid argument length")
                continue
            # path, new_path

            s3_client.s3copy(pathlib.Path(cmd[1]), pathlib.Path(cmd[2]))
        elif "s3delete" in cmd:
            if len(cmd) < 2:
                print("invalid argument length")
                continue
            # path
            s3_client.s3delete(pathlib.Path(cmd[1]))
        elif "delete_bucket" in cmd:
            # bucket_name
            if len(cmd) < 2:
                print("invalid argument length")
                continue
            s3_client.delete_bucket(pathlib.Path(cmd[1]))
        elif ":h" in cmd or ":help" in cmd:
            print_help()
        else:
            aws_helper.exec_sys_cmd(cmd_og)


if __name__ == "__main__":
    main()
