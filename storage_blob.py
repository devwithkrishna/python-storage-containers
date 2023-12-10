import os
import argparse
from datetime import datetime, timedelta
from dotenv import load_dotenv
from get_secret_from_kv import get_access_key_from_kv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, generate_account_sas, ResourceTypes, AccountSasPermissions


def azure_storage_blob(storage_account: str, time_limit_of_sas_token: int, keyvault_name: str, secret_name: str):
    """
    works with azure storage account - especially blobs
    Pre requisites: this function expects the storage account access key to be configured as a secret in kv

    This function will fetch the secret value of storage account acccess key from keyvault and
    use it to generate the SAS token for working with blobs for a specific periods

    : params storage_account --> storage account
    : params time_limit_of_sas_token --> validity of sas token in hoours
    : params keyvault_name --> key vault name
    : params secret_name --> secret name
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

    
    
def main():
    """
    for testing
    """
    parser = argparse.ArgumentParser (description='argumets for the function')
    parser.add_argument('--storage_account', help= 'storage account name', type= str, nargs='?', required=True)
    parser.add_argument('--time_limit_of_sas_token', help='time limit of SAS token', type=int, default= 1, required=True)
    parser.add_argument('--keyvault_name', help='keyvault name in which storage account key secret set', type=str)
    parser.add_argument('--secret_name', help='storage account access key secret name', type=str)
    
    args = parser.parse_args()
    storage_account = args.storage_account
    time_limit_of_sas_token = args.time_limit_of_sas_token
    keyvault_name = args.keyvault_name
    secret_name = args.secret_name
    load_dotenv()
    azure_storage_blob(storage_account=storage_account, time_limit_of_sas_token=time_limit_of_sas_token, keyvault_name=keyvault_name, secret_name=secret_name)
    
    
if __name__ == '__main__':
    main()