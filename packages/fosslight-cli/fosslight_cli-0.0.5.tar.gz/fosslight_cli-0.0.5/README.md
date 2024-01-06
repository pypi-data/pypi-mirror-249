# FOSSLIGHT CLI

This tool allows easy communication with the FOSSLIGHT Hub server. <br>
It can be utilized for various purposes such as project creation, modification, export Bill of Materials (bom), scanning and upload scan result files.


# 📋 Prerequisite
Python 3.8+

# 🎉 How to install
```
$ pip3 install fosslight_cli
```

# How to Run

To execute the fosslight-cli command in the terminal, use the following syntax:

```
$ fosslight-cli [command] [resource name] ([sub-resource name]) [parameters ...]
```

- **command**: Specifies the action to be performed.
    - create
    - update
    - get
    - export
    - apply
    - compare
- **resource name**: Specifies the resource name.
    - project
    - selfCheck
    - config
    - code
    - partner
    - oss
    - license
    - vulnerability
    - maxVulnerability
    - yaml
- **sub-resource name**: Some commands require specifying a sub-resource name.
    - ex.
        
        ```
        $ fosslight-cli get project list
        $ fosslight-cli update project bin
        $ fosslight-cli get project models
        ```
- **parameters**: List of input parameters. Mandatory and optional parameters can be provided.


# Commands
| Command | Syntax                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Description                                                                     |
| --- |--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| create |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Create a resource                                                               |
|  | fosslight-cli create project <br>&nbsp; --prjName TEXT            Name of the Project  [required] <br>&nbsp; --osType TEXT             OS type of the Project  [required] <br>&nbsp; --distributionType TEXT   [required] <br>&nbsp; --networkServerType TEXT  [required] <br>&nbsp; --priority TEXT           [required] <br>&nbsp; --osTypeEtc TEXT <br>&nbsp; --prjVersion TEXT <br>&nbsp; --publicYn TEXT <br>&nbsp; --comment TEXT <br>&nbsp; --userComment TEXT <br>&nbsp; --watcherEmailList TEXT <br>&nbsp; --modelListToUpdate TEXT <br>&nbsp; --modelReportFile TEXT | Create a project                                                                |
|  | fosslight-cli create selfCheck <br>&nbsp; --prjName TEXT     Name of the Project  [required] <br>&nbsp; --prjVersion TEXT  Version of the Project                                                                                                                                                                                                                                                                                                                                                                  | Create a self-check                                                             |
| update |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Modify a resource                                                               |
|  | fosslight-cli update project watchers <br>&nbsp; --prjId TEXT      project id  [required] <br>&nbsp; --emailList TEXT  watcher emailList  [required]                                                                                                                                                                                                                                                                                                                                                               | Update project watchers                                                         |
|  | fosslight-cli update project models <br>&nbsp; --prjId TEXT              project id  [required] <br>&nbsp; --modelListToUpdate TEXT  [required]                                                                                                                                                                                                                                                                                                                                                                    | Update project model list                                                       |
|  | fosslight-cli update project modelFile <br>&nbsp; --prjId TEXT        project id  [required] <br>&nbsp; --modelReport TEXT  [required]                                                                                                                                                                                                                                                                                                                                                                             | Update project model list using a model file                                    |
|  | fosslight-cli update project scan <br>&nbsp; --prjId TEXT  project id  [required] <br>&nbsp; --dir TEXT    project directory path  [required]                                                                                                                                                                                                                                                                                                                                                                      | Analyze the project directory using FOSSLIGHT scanner and upload bin, src files |
|  | fosslight-cli update project bin <br>&nbsp; --prjId TEXT      project id  [required] <br>&nbsp; --ossReport TEXT <br>&nbsp; --binaryTxt TEXT <br>&nbsp; --comment TEXT <br>&nbsp; --resetFlag TEXT                                                                                                                                                                                                                                                                                                                                   | Upload bin files for the project                                                |
|  | fosslight-cli update project src <br>&nbsp; --prjId TEXT      project id  [required] <br>&nbsp; --ossReport TEXT <br>&nbsp; --comment TEXT <br>&nbsp; --resetFlag TEXT                                                                                                                                                                                                                                                                                                                                                         | Upload src files for the project                                                |
|  | fosslight-cli update project package <br>&nbsp; --prjId TEXT        project id  [required] <br>&nbsp; --packageFile TEXT  [required] <br>&nbsp; --verifyFlag TEXT                                                                                                                                                                                                                                                                                                                                                        | Upload package files for the project                                            |
|  | fosslight-cli update selfCheck report <br>&nbsp; --selfCheckId TEXT  selfCheck id  [required] <br>&nbsp; --ossReport TEXT <br>&nbsp; --resetFlag TEXT                                                                                                                                                                                                                                                                                                                                                                    | Upload self-check report files                                                  |
|  | fosslight-cli update selfCheck watchers <br>&nbsp; --selfCheckId TEXT  selfCheck id  [required] <br>&nbsp; --emailList TEXT    [required]                                                                                                                                                                                                                                                                                                                                                                          | Update self-check watchers                                                      |
|  | fosslight-cli update partner watchers <br>&nbsp; --partnerId TEXT  partner id  [required] <br>&nbsp; --emailList TEXT  [required]                                                                                                                                                                                                                                                                                                                                                                                  | Update partner watchers                                                         |
|  | fosslight-cli update config <br>&nbsp; -s, --server TEXT  Server url <br>&nbsp; -t, --token TEXT   Account token                                                                                                                                                                                                                                                                                                                                                                                                   | Update server and authentication token settings                                 |
| get |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Retrieve a resource                                                             |
|  | fosslight-cli get project list <br>&nbsp; --createDate TEXT <br>&nbsp; --creator TEXT <br>&nbsp; --division TEXT <br>&nbsp; --modelName TEXT <br>&nbsp; --prjIdList TEXT <br>&nbsp; --status TEXT <br>&nbsp; --updateDate TEXT                                                                                                                                                                                                                                                                                                                   | Get project list                                                                |
|  | fosslight-cli get project models <br>&nbsp; --prjIdList TEXT                                                                                                                                                                                                                                                                                                                                                                                                                 | Get license list                                                                |
|  | fosslight-cli get license list <br>&nbsp; --licenseName TEXT  license name  [required]                                                                                                                                                                                                                                                                                                                                                                                                                       | Get license list                                                                |
|  | fosslight-cli get oss list <br>&nbsp; --ossName TEXT           oss name  [required] <br>&nbsp; --ossVersion TEXT        oss version <br>&nbsp; --downloadLocation TEXT  download location                                                                                                                                                                                                                                                                                                                                | Get oss list                                                                    |
|  | fosslight-cli get partner list <br>&nbsp; --createDate TEXT <br>&nbsp; --creator TEXT <br>&nbsp; --division TEXT <br>&nbsp; --partnerIdList TEXT <br>&nbsp; --status TEXT <br>&nbsp; --updateDate TEXT                                                                                                                                                                                                                                                                                                                                     | Get 3rd party list                                                              |
|  | fosslight-cli get config                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Get configured server and authentication token                                  |
|  | fosslight-cli get code <br>&nbsp; --codeType TEXT     code type  [required] <br>&nbsp; --detailValue TEXT  detail value                                                                                                                                                                                                                                                                                                                                                                                            | Get code information                                                            |
|  | fosslight-cli get maxVulnerability <br>&nbsp; --ossName TEXT     oss name  [required] <br>&nbsp; --ossVersion TEXT  oss version                                                                                                                                                                                                                                                                                                                                                                                    | Get max vulnerability                                                           |
|  | fosslight-cli get vulnerability <br>&nbsp; --cveId TEXT       cve id <br>&nbsp; --ossName TEXT     oss name <br>&nbsp; --ossVersion TEXT  oss version                                                                                                                                                                                                                                                                                                                                                                    | Get vulnerability info                                                          |
| export |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Export resources (usually a file)                                               |
|  | fosslight-cli export project bom <br>&nbsp; --prjId TEXT          project id  [required] <br>&nbsp; --mergeSaveFlag TEXT  mergeSaveFlag <br>&nbsp; -o, --output TEXT     output file path                                                                                                                                                                                                                                                                                                                                | Download project bom file                                                       |
|  | fosslight-cli export project bomJson <br>&nbsp; --prjId TEXT  project id  [required]                                                                                                                                                                                                                                                                                                                                                                                                                         | Download project bom information as JSON                                        |
|  | fosslight-cli export project notice <br>&nbsp; --prjId TEXT       project id  [required] <br>&nbsp; -o, --output TEXT  output file path                                                                                                                                                                                                                                                                                                                                                                            | Download project notice file                                                                           |
|  | fosslight-cli export selfCheck <br>&nbsp; --selfCheckId TEXT  selfCheck id  [required]                                                                                                                                                                                                                                                                                                                                                                                                                       | self-check export                                                               |
| compare |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Compare resources                                                                          |
|  | fosslight-cli compare project bom <br>&nbsp; --prjId TEXT      [required] <br>&nbsp; --compareId TEXT  [required]                                                                                                                                                                                                                                                                                                                                                                                                  | Compare the boms of two projects                                                               |
| apply |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Execute actions defined in a file                                                                  |
|  | fosslight-cli apply yaml <br>&nbsp; -f, --file TEXT  yaml file path  [required]                                                                                                                                                                                                                                                                                                                                                                                                                              | Perform actions defined in a YAML file                                                   |

# Apply

Functionality to perform actions defined in a file all at once.

Actions are distinguished based on the kind value.


### createProject

Example:

- fosslight-cli apply yaml -f create_project.yaml
    
    ```yaml
    # create_project.yaml
    kind: createProject
    parameters:
      prjName: test-project
      prjVersion: 1
      osType: Linux
      distributionType: "General Model"
      networkServerType: N
      priority: P1
    update:
      models:
        modelListToUpdate: "ASDF|AV/Car/Security > AV|20201010"
    scan:
      dir: "~/data/simpleProject"
    ```
    
    - Create a project, update model information, and upload the results of scanning the project directory.




# Examples

## Config

- Update server url and token settings
    
    ```
    $ fosslight-cli update config --server http://127.0.0.1:8180 --token xxxx
    ```
    

- Get configured server and token
    
    ```
    $ fosslight-cli get config
    ```
    

## Project

- Create a project
    
    ```
    $fosslight-cli create project \
    	--prjName test_project \
    	--osType Linux \
    	--distributionType 'General Model' \
    	--networkServerType N \
    	--priority P1
    ```
    
    *For code values like osType, you can input numeric codes such as 100, or display values like Linux (case insensitive).
    

- Input models
    
    ```
    $fosslight-cli update project models \
    	--prjId 1 \
    	--modelListToUpdate "ASDF|AV/Car/Security > AV|20201010"
    ```
    

- Upload bin files
    
    ```
    $fosslight-cli update project bin \
    	--prjId 1 \
    	--binaryTxt /path/to/file/fosslight_binary_bin_231214_1020.txt \
    	--ossReport /path/to/file/fosslight_report_231219_prj-10.xlsx
    ```
    

- Run Scanner & Upload results
    
    ```
    $fosslight-cli update project scan --prjId 1 --dir /path/to/project/
    ```
    

- Retrieve project list
    
    ```
    $fosslight-cli get project list
    ```
