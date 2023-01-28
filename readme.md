# CIS\*4010 AWS S3 Shell

David Pearson

1050197

### Requirements

**Must have Python3**

This is because of f strings used in outputs which are not available until python 3.6 I believe. 

See Requirments.txt for dependencies! This file was generated automatically using pipreqs. 

`pip install boto3`

Developed on WSL Debian & OSX

Not sure about Windows support

Must have a file `S5-S3.conf` with the same stucture as defined in the spec.
It will look for a `[default]` profile.  

## How to Run

`python3 S5.py` --> Must be python3 to handle f strings

use `:h` or `:help` for command options

## Behaviour
Upon startup you will encounter the S5 shell prompt as follows: 

`/ % S5> `

As personal preference and how I have my actual terminal setup, the cwd is included in the prompt. When navigating, the cwd will always be refelected on the left side of the prompt:

`/dpears04b01/images % S5> `

I have implemented a help command to improve user experience. This is a very basic command but will list available S3 commands and arguments they expect. 

Most commands will expect the user to chlocn into a bucket before execution, inline with the spec. I considered just allowing the user to do as they wish and not validate this, but in the end decided its best to include it. 

Upon command success nothing is returned, on failure the error message from Boto3 will be returned. All commands will also return a 0 or 1 value depending on success, although these are not used by the shell currently. 

Use `exit` to exit the shell

Any commands not recognized by S5 shell is passed off to the OS shell, typically Bash

Relative paths can be used as `./path/to/object` or simply `path/to/object`

`chlocn ../../images` is a viable command 

## Limitations 
- `chlocn` validates if the new path exists before alowing the user to navigate there. Initially, inorder to be efficient with requests the head_bucket() function was used as this only makes a single request and would scale efficiently. However, this meant that nested subdirectories would not be visible as they are not 'head objects'. As such, the validation now checks the new directory against all keys in the S3 bucket. This will not scale well as bucket objects increases beyond the scope of this project.
- If ObjectACL data is not available, nothing will be output for the -l flag for the list command except for the folder name
  - This is a result of how subfolders are treated in S3
  - Only 'head objects' will have a return value from ObjectAcl() 
- In a similar fashion to how Bash handles errors, when something goes wrong, error messages are the output of the expection thrown by Boto3. Usually these messages are very clear. 
- Very basic input validation. Bash will let you try to execute anything and isn't responsible for ensuring the proper inputs. Despite this to improve usability there is input validation that ensures that the correct number of arguments are passed in at the very least. 
- For `list -l` the data Boto3 offers on details is fairly limited, for buckets, this will only output the permission level. Similarly for folders.
- Sometimes s3delete will not return an error if it was unable to delete an object. This is a result that Boto3 doesnt offer any return value that indicates failure. The simple fix for this would be checking if the object exists after a delete attempt, but with a limited number of requests with AWS this wouldnt work for the sake of this project. 
