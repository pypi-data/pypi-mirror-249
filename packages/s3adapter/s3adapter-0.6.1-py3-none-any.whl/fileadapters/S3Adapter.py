import boto3
import os
from io import StringIO
import pandas as pd
from dotenv import load_dotenv
from fileadapters.basefileadapter import BaseFileAdapter
from log import get_logger

class S3Adapter:
    #TODO: Implement Base Init
    #def __init__(self, file_path, file_name, formater:BaseFileFormater, validade_aws=True):  
    def __init__(self, bucket_name, validade_aws=False):
        self.log=get_logger('S3Adapter')

        self.log.debug('Initializing S3Adapter')
        
        # Load environment variables from .env file
        load_dotenv()


        if validade_aws:          
          if not self.__validate_cloud_credentials__():
              self.log.error('Cloud Credentials not valid or not informed in env')
              raise Exception('Enviroments for init AWS Client not informed. Please provide default AWS enviroment vars AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY and AWS_DEFAULT_REGION or init class with validate_aws=False and init AWS account infos call method init_cloud.')  
                      
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')

        self.log.debug('S3Adapter Initialized')


    def __validate_cloud_credentials__(self):
        self.log.debug('Validanting Cloud Credentials')
        #False or True or True = True -> not = False
        #False or False or False = False -> not = True

        is_valid = not (os.getenv('AWS_ACCESS_KEY_ID')==None or
                        os.getenv('AWS_SECRET_ACCESS_KEY')==None or
                        os.getenv('AWS_DEFAULT_REGION')==None)

        self.log.debug(f'Cloud Credentials is valid:{is_valid}')
        
        return is_valid
                      
            
        
    def init_cloud(self, aws_access_key_id, aws_secret_access_key, region_name):
        self.log.debug(f'Initializing Cloud Credentials for access_key [{aws_access_key_id}] and region [{region_name}]')
        
        #set default aws env vars
        os.environ['AWS_ACCESS_KEY_ID']=aws_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY']=aws_secret_access_key
        os.environ['AWS_DEFAULT_REGION']=region_name

        #init s3 client
        self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id,
                                      aws_secret_access_key=aws_secret_access_key,
                                      region_name=region_name)
        
        self.log.debug('Cloud Credentials Initialized')
            

    #TODO: [SCRUM-2] Refactor it to Generic Write, including File Formater to deal with parquet, csv and other formats
    def read_csv_as_dataframe(self, file_key, sep=','):
        try:
            self.log.debug(f'Reading CSV as Dataframe from S3Bucket, object [{file_key}], bucket [{self.bucket_name}]')
            
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=file_key)
            content = response['Body'].read().decode('utf-8')
            df = pd.read_csv(StringIO(content), sep=sep)

            self.log.debug(f'Sucess Read CSV as Dataframe from S3Bucket, object [{file_key}], bucket [{self.bucket_name}]')

            return df
        except Exception as e:
            print(f"Error reading CSV from S3: {e}")
            self.log.exception(e)
            self.log.debug(f'Error in Reading CSV as Dataframe from S3Bucket, object [{file_key}], bucket [{self.bucket_name}]')
            return None
       
    
    def write_dataframe_as_csv(self, df, file_key, sep=','):
        try:
            self.log.debug(f'Writing Dataframe as CSV to S3Bucket, object [{file_key}], bucket [{self.bucket_name}]')

            csv_content = df.to_csv(index=False, sep=sep)
            self.s3_client.put_object(Body=csv_content, Bucket=self.bucket_name, Key=file_key)
            
            print(f"CSV written to S3: {file_key}")            
            self.log.debug(f'Sucess in Writing Dataframe as CSV to S3Bucket, object [{file_key}], bucket [{self.bucket_name}]')
        except Exception as e:
            print(f"Error writing CSV to S3: {e}")
            self.log.exception(e)
            self.log.debug(f'Error in Writing Dataframe as CSV to S3Bucket, object [{file_key}], bucket [{self.bucket_name}]')

    def exists(self, file_key):
        try:
            self.log.debug(f'Trying to get S3Bucket, object [{file_key}], bucket [{self.bucket_name}]')
            self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
            self.log.debug(f'Sucess to get S3Bucket, object [{file_key}], bucket [{self.bucket_name}]')
            return True
        except Exception as e:
            self.log.exception(e)
            self.log.debug(f'Error to get S3Bucket, object [{file_key}], bucket [{self.bucket_name}]')
            return False
