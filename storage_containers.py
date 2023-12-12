import os
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
from get_secret_from_kv import get_access_key_from_kv
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions


def get_storage_account_url(storage_account: str):
    """
    returns the URL of storage account
    Args:
        storage_account:

    Returns:
    """
    storage_account_url = f"https://{storage_account}.blob.core.windows.net"
    print(f"Storage account URL is : {storage_account_url}")
    return storage_account_url


def create_container_on_storage_account(storage_account: str, container_name: str):
    """
    creates a container on metioned storage account with mentioned container name
    Args:
        storage_account:
        container_name:

    Returns:
    """
    container_name = container_name
    blob_service_client = create_blob_service_client(storage_account=storage_account)
    container_client = blob_service_client.create_container(container_name)
    print(f"Container {container_name} created on {storage_account}")


def delete_container_on_storage_account(storage_account:str, container_name: str):
    """
    delete a container
    Args:
        storage_account:
        container_name:
    Returns:
    """
    container_client = BlobServiceClient.undelete_container()
    blob_service_client = create_blob_service_client(storage_account=storage_account)
    blob_service_client.delete_container(container=container_name)
    print(f"Container {container_name} deleted from {storage_account}")


# def delete_multiple_contaners_on_storage_aaccount(storage_account: str, *container_name: str):
#     """
#     deletes multiple containers in a single run
#     Args:
#         storage_account:
#         *container_name:

#     Returns:

#     """

## stack overflow link: https://stackoverflow.com/questions/77643982/i-am-getting-an-error-while-using-azure-stprage-blob-sdk-while-undeleting-a-cont
def recover_soft_deleted_containers_on_storage_account(storage_account: str, container_name: str):
    """
    recover soft deleted containers.
    Operation will only be successful if used within the specified number of days set in the delete retention policy.

    Args:
        storage_account:
        container_name:

    Returns:

    """
    blob_service_client = create_blob_service_client(storage_account=storage_account)
    container_list = list(blob_service_client.list_containers(include_deleted=True))
    assert len(container_list) >= 1
    for container in container_list:
        # Find the deleted container and restore it
        if container.deleted and container.name == container_name:
            restored_container_client = blob_service_client.undelete_container(
                deleted_container_name=container.name, deleted_container_version=container.version)
    print(f"Container {container_name} recovered from {storage_account}")


def recover_all_deleted_containers_from_storage_account(storage_account: str):
    """
    recover_all_deleted_containers
    Args:
        storage_account:

    Returns:
        recovers all deleted containers
    """
    blob_service_client = create_blob_service_client(storage_account=storage_account)
    container_list = list(blob_service_client.list_containers(include_deleted=True))
    assert len(container_list) >= 1
    for container in container_list:
        # Find the deleted container and restore it
        if container.deleted :
            restored_container_client = blob_service_client.undelete_container(
                deleted_container_name=container.name, deleted_container_version=container.version)
            print(f"Container {container.name} recovered from {storage_account}")


def list_containers_on_storage_account(storage_account: str):
    """
    function to return name of containers in mentioned storage account
    Includes deleted containers with in soft delete period
    Args:
        storage_account:

    Returns:
    list of containers
    """
    blob_service_client = create_blob_service_client(storage_account=storage_account)
    list_of_containers = blob_service_client.list_containers(include_deleted=True)
    for container in list_of_containers:

        containername = container.name
        container_lastmodifiedd = container.last_modified
        print(f"Container name is : {containername}")
        print(f"Container last modified on : {container_lastmodifiedd}")
    print(f"Containers listed on {storage_account}")


def create_blob_service_client(storage_account: str):
    """
    Create a blob service client for blob operations
    Args:
        storage_account:

    Returns:
    """
    storage_account_url = get_storage_account_url(storage_account)
    default_credential = DefaultAzureCredential()
    # Create the BlobServiceClient object
    blob_service_client = BlobServiceClient(storage_account_url, credential=default_credential)
    return blob_service_client


def azure_storage_blob(storage_account: str, time_limit_of_sas_token: int, keyvault_name: str, secret_name: str, container_name: str, action: str):
    """
    works with azure storage account - especially blobs
    Pre requisites: this function expects the storage account access key to be configured as a secret in kv

    This function will fetch the secret value of storage account acccess key from keyvault and
    use it to generate the SAS token for working with blobs for a specific periods

    : params storage_account --> storage account
    : params time_limit_of_sas_token --> validity of sas token in hoours
    : params keyvault_name --> key vault name
    : params secret_name --> secret name
    : params container_name --> container name 
    : params action --> create_container / delete_container
    """
    # Get storage account access key from Key vault
    account_key = get_access_key_from_kv(keyvault_name, secret_name)
    
    # Generate SAS token for the storage account for an hour by default or specified value
    sas_token = generate_account_sas(
    account_name=storage_account,
    account_key=account_key,
    resource_types=ResourceTypes(service=True),
    permission=AccountSasPermissions(read=True),
    expiry=datetime.utcnow() + timedelta(hours=time_limit_of_sas_token)
    )

    print(f"SAS Token for {storage_account} for {time_limit_of_sas_token} hour is: {sas_token}")
    # storage_account_url = get_storage_account_url(storage_account=storage_account)
    
    if action == "create_container":
        create_container_on_storage_account(storage_account=storage_account, container_name=container_name)
        print(f"Action {action} created {container_name} on {storage_account}")
    elif action == "delete_container":
        delete_container_on_storage_account(storage_account=storage_account,container_name=container_name)
        print(f"Action {action} {container_name} on {storage_account}")
    elif action == "list_containers":
        list_containers_on_storage_account(storage_account=storage_account)
        print(f"Action {action} on storage account {storage_account}")
    elif action == "recover_container":
        recover_soft_deleted_containers_on_storage_account(storage_account=storage_account,container_name=container_name)
        print(f"Action {action} on storage account {storage_account}")
    elif action == "recover_all_deleted_containers":
        recover_all_deleted_containers_from_storage_account(storage_account=storage_account)
        print(f"Recovered all deleted containers from {storage_account}")
    else:
        print(f"provided invalid action. please provide one among the available choices")


def main():
    """
    for testing
    """
    parser = argparse.ArgumentParser (description='argumets for the function')
    parser.add_argument('--storage_account', help= 'storage account name', type= str, nargs='?', required=True)
    parser.add_argument('--time_limit_of_sas_token', help='time limit of SAS token', type=float, default= 1, required=True)
    parser.add_argument('--keyvault_name', help='keyvault name in which storage account key secret set', type=str)
    parser.add_argument('--secret_name', help='storage account access key secret name', type=str)
    parser.add_argument('--action', required=True, help= 'create container / delete container/ list containers/ recover container or containers', type= str, choices=[  ])
    parser.add_argument('--container_name', type=str, help='container name')
    args = parser.parse_args()
    storage_account = args.storage_account
    time_limit_of_sas_token = args.time_limit_of_sas_token
    keyvault_name = args.keyvault_name
    secret_name = args.secret_name
    container_name = args.container_name
    action = args.action
    load_dotenv()
    azure_storage_blob(storage_account=storage_account, time_limit_of_sas_token=time_limit_of_sas_token, keyvault_name=keyvault_name, secret_name=secret_name, container_name=container_name, action=action)
    
    
if __name__ == '__main__':
    main()