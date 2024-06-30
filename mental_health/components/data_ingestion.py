import os
import sys
from zipfile import ZipFile
from mental_health.logger import logging
from mental_health.exception import CustomException
from mental_health.configuration.aws_syncer import AWSS3Sync
from mental_health.entity.config_entity import DataIngestionConfig
from mental_health.entity.artifact_entity import DataIngestionArtifacts


class DataIngestion:
    def __init__(self, data_ingestion_config : DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        self.gcloud = AWSS3Sync()


    def sync_folder_from_s3(self) -> None:
        try:
            logging.info("Entered the get_data_from_awscloud method of Data ingestion class")
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)

            self.AWSS3Sync.sync_folder_from_gcloud(self.data_ingestion_config.BUCKET_NAME,
                                                self.data_ingestion_config.ZIP_FILE_NAME,
                                                self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR,
                                                )
            
            logging.info("Exited the get_data_from_awscloud method of Data ingestion class")

        
        except Exception as e:
            raise CustomException(e, sys) from e
        
    
    def unzip_and_clean(self):
        logging.info("Entered the unzip_and_clean method of Data ingestion class")
        try: 
            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)

            logging.info("Exited the unzip_and_clean method of Data ingestion class")

            return self.data_ingestion_config.DATA_ARTIFACTS_DIR, self.data_ingestion_config.DATA_ARTIFACTS_DIR

        except Exception as e:
            raise CustomException(e, sys) from e
        
    

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the initiate_data_ingestion method of Data ingestion class")

        try:
            self.sync_folder_from_s3()
            logging.info("Fetched the data from gcloud bucket")
            mental_health_data_file_path = self.unzip_and_clean()
            logging.info("Unzipped file and split into train and valid")

            data_ingestion_artifacts = DataIngestionArtifacts(
                mental_health_data_file_path= mental_health_data_file_path,
               
            )

            logging.info("Exited the initiate_data_ingestion method of Data ingestion class")

            logging.info(f"Data ingestion artifact: {data_ingestion_artifacts}")

            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e