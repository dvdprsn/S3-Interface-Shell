# CIS\*4010 AWS S3 Shell

David Pearson

1050197

### Requirements

**Must have Python3 **

This is because of f strings used in outputs which are not available until python 3.6 I believe. 

`pip install boto3`

## How to Run

`python3 S5.py`

use `:h` or `:help` for command options

## Behaviour
Upon startup you will encounter the S5 shell prompt as follows: 

`/ % S5> `

As personal preference and how I have my actual terminal setup, the cwd is included in the prompt. 
## Limitations

- If ObjectACL data is not available, nothing will be output for the -l flag for the list command except for the folder name
  - This is a result of how subfolders are treated in S3
  - Only 'head objects' will have a return value from ObjectAcl() 
- In a similar fashion to how Bash handles errors, when something goes wrong, error messages are the output of the expection thrown by Boto3. Usually these messages are very clear. 
- Very basic input validation. Bash will let you try to execute anything and isn't responsible for ensuring the proper inputs. Despite this to improve usability there is input validation that ensures that the correct number of arguments are passed in at the very least. 
