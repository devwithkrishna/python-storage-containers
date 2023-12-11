# python-storage-blob

azure storage blob modifications using python sdk and create workflow

## Pre requesites

 * this program expects the storage account access key to be configured as a secret in kv
    - This is a best practice to not hardcode any sensitive values into public repositories and
      leverage key vault.

## What does the code do?

* It can create container in storage account
* it can delete a container from storage account
* It can create a SAS token for an expiry time using SP credentials

## What is the new features to be added?

* Uploading a blobs / directory
* deleting blobs / directory inside container
* Listing blobs / directory inside container 
* Downloading blobs / directory
* Copying blobs / directory

## Parameters

| parameter name| positional params| optional params | description |
|---------------|------------------|-----------------|-------------|
|storage_account| yes              | no              |storage account we are dealing with|
|time_limit_of_sas_token| yes      | no              | time limit for SAS token to be alive in hours|
|keyvault_name |       yes         | no              | keyvault in which storage account key is stored as a secret|
|secret_name   | yes               | no              | secret name of storage account access key in key vault|
|container_name| no                | yes             | used for creating / deleting a container|

## How to run the code

    - Program is still in development, will add later


### Jira ticket associated

[jira story - DEVOPS-16](https://devwithkrishna.atlassian.net/jira/software/projects/DEVOPS/boards/1?selectedIssue=DEVOPS-16)
