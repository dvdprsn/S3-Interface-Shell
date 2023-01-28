# CIS\*4010 AWS S3 Shell

### Requirements

`pip install boto3`

## How to Run

`python3 S5.py`

use `:h` or `:help` for commands

## Behaviour

## Limitations

- If ObjectACL data is not available, nothing will be output for the -l flag for the list command except for the folder name
  - This is a result of how subfolders are treated in S3
