import os
import argparse
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv

def get_access_key_from_kv(keyvault_name: str, secret_name: str):
    """
    Get the account access key for storage account stored in the key vault
    Args:
        keyvault_name (str): _description_
        secret_name (str): _description_
    """
    credential = DefaultAzureCredential ()
    keyvault_url = f"https://{keyvault_name.lower ()}.vault.azure.net"
    print(f"Keyvault Url is : {keyvault_url}")
    client = SecretClient (vault_url= keyvault_url, credential=credential)
    get_access_key = client.get_secret(secret_name).value
    return get_access_key


def main():
    """
    For testing the function
    """
    load_dotenv()
    parser = argparse.ArgumentParser (description='argumets for the function')
    parser.add_argument('keyvault_name', description= 'keyvault from which secret need to be fetched', type=str)
    parser.add_argument('secret_name', description='secret to be fetched from key vault', type=str)
    args = parser.parse_args()
    keyvault_name = args.keyvault_name
    secret_name = args.secret_name
    get_access_key_from_kv(keyvault_name=keyvault_name, secret_name=secret_name)
    
if __name__ == '__main__':
    main()

