import logging
from pathlib import Path
from decouple import config
from typing import Any, Text

try:
    from azure.identity import DefaultAzureCredential, AzureCliCredential, ChainedTokenCredential, ManagedIdentityCredential
except:
    logging.warning("missing azure.identity")

try:
    from azure.keyvault.secrets import SecretClient
except:
    logging.warning("missing azure-keyvault-secrets")

class SecretUtils(object):
    def __init__(self, dbutils = None, env_name: Text = None, keyvault_name: Text = ""):
        self.keyvault_name = keyvault_name
        self.dbutils = dbutils
        self.az_keyvault_utils = AzKeyVaultUtils(env_name=env_name, keyvault_name=keyvault_name)

    def get_secret(self, key_name: Text):
        try:
            if self.dbutils:
                logging.info(f"SecretUtils::get_secret - dbutils.secrets - scope:{self.keyvault_name} - key: {key_name}")
                return self.dbutils.secrets.get(scope=self.keyvault_name, key=key_name)
            else:
                secret_value = LocalSecretUtils.get_secret(key_name=key_name)
                
                if secret_value is None or len(secret_value) == 0: # checking if secret_value is empty
                    secret_value = self.az_keyvault_utils.get_secret(key_name=key_name)
                    #print(f"AzKeyVaultUtils-{key_name} - {secret_value}")
                    return secret_value
                else:
                    #print(f"LocalSecretUtils-{key_name} - {secret_value}")
                    return secret_value
        except Exception as error:
            #print(error)
            logging.warning('SecretUtils - get_secret() Execution error: %s', error)
        
        return ""
    def get_managed_identity_client_id() -> str:
        """
        return User-assigned Managed Identity from environement variable - XOM-APP-MANAGED-IDENTITY-ID
        """
        return LocalSecretUtils.get_managed_identity_client_id()
    
class LocalSecretUtils(object):
    @staticmethod
    def get_secret(key_name: Text):
        contents = ""

        # If there is no key_value in .keyvaults folder, Try to load key_value from system environment
        try:
            # How does it work? - https://pypi.org/project/python-decouple/#toc-entry-12
            contents = config(key_name, default='')
        except Exception as error:
            logging.warning('LocalSecretUtils - get_secret() Execution error: %s', error)
            contents = ""
                
        return contents

    @staticmethod
    def is_env_dev(env_name:str) -> bool:
        if env_name is not None:
            return env_name in ["dev", "develop", "development"]
        return False

    @staticmethod
    def is_env_staging(env_name:str) -> bool:
        if env_name is not None:
            return env_name in ["tst", "stg", "staging"]
        return False

    @staticmethod
    def is_env_prod(env_name:str) -> bool:
        if env_name is not None:
            return env_name in ["prd", "prod", "production"]
        return False

    @staticmethod
    def get_keyvault_name() -> str:
        """
        return WellRt KeyVault from environement variable - XOM-APP-KEYVAULT-NAME
        """
        return LocalSecretUtils.get_secret(key_name="XOM-APP-KEYVAULT-NAME")

    @staticmethod
    def get_environment() -> str:
        """
        return WellRt KeyVault from environement variable - XOM-APP-DEPLOYMENT
        """
        return LocalSecretUtils.get_secret(key_name="XOM-APP-DEPLOYMENT")

    @staticmethod
    def is_managed_identity_enabled() -> bool:
        """
        check User-assigned Managed Identity from environement variable - XOM-APP-MANAGED-IDENTITY-ENABLED
        """
        managed_identity_enabled =  LocalSecretUtils.get_secret(key_name="XOM-APP-MANAGED-IDENTITY-ENABLED")
        return managed_identity_enabled is not None and "true" == managed_identity_enabled.lower()

    @staticmethod
    def get_managed_identity_client_id() -> str:
        """
        return User-assigned Managed Identity from environement variable - XOM-APP-MANAGED-IDENTITY-ID
        """
        return LocalSecretUtils.get_secret(key_name="XOM-APP-MANAGED-IDENTITY-ID")


class AzKeyVaultUtils(object):
    def __init__(self, env_name: Text = None, keyvault_name: Text = ""):
        self.keyvault_name = keyvault_name
        self.secret_client  = None
        if env_name is not None or len(env_name) == 0:
            self.env_name = env_name
        else:
            self.env_name = LocalSecretUtils.get_environment()

        self._init_secret_client()
    
    def _init_secret_client(self):
        try:  
            # Service principal with secret:
            # - **AZURE_TENANT_ID**: ID of the service principal's tenant. Also called its 'directory' ID.
            # - **AZURE_CLIENT_ID**: the service principal's client ID
            # - **AZURE_CLIENT_SECRET**: one of the service principal's client secrets
            default_credential = DefaultAzureCredential()          
            # 

            check_default_env_name = self.env_name
            if self.env_name is None or len(self.env_name) == 0:
                check_default_env_name = "dev"

            if LocalSecretUtils.is_env_dev(env_name=check_default_env_name):
                # local development
                azure_cli = AzureCliCredential()
                credential_chain = ChainedTokenCredential(azure_cli, default_credential)
            else:
                # setup managed-identity
                if LocalSecretUtils.is_managed_identity_enabled():
                    managed_identity_client_id = LocalSecretUtils.get_managed_identity_client_id()
                    if len(managed_identity_client_id) > 0:
                        # user-managed identity
                        managed_identity = ManagedIdentityCredential(client_id=managed_identity_client_id)
                    else:
                        # system managed_identity
                        managed_identity = ManagedIdentityCredential()
            
                    # production (azure) deployment
                    credential_chain = ChainedTokenCredential(managed_identity, default_credential)
                else:
                    # production (azure) deployment
                    credential_chain = ChainedTokenCredential(default_credential)

            self.secret_client = SecretClient(vault_url=f"https://{self.keyvault_name}.vault.azure.net", credential=credential_chain)
            
        except Exception as ex:
            #print(ex)
            logging.warning('AzKeyVaultUtils - _init_secret_client() Execution error: %s', ex)

    def get_secret(self, key_name: Text):
        contents = ""
        try:
            if self.secret_client is not None:
                _secret = self.secret_client.get_secret(key_name)
                contents = _secret.value
        except Exception as ex:
            #print(ex)
            logging.warning('AzKeyVaultUtils - get_secret() Execution error: %s', ex)

        return contents