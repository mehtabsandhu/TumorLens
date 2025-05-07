import os
import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import shutil
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class KaggleDataManager:
    def __init__(self, cache_dir: str = "data/cache"):
        """
        Initialize the Kaggle data manager.
        
        Args:
            cache_dir (str): Directory to cache downloaded data
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.api = self._setup_kaggle_api()
        
    def _setup_kaggle_api(self) -> KaggleApi:
        """
        Set up the Kaggle API client.
        
        Returns:
            KaggleApi: Configured Kaggle API client
        """
        try:
            api = KaggleApi()
            api.authenticate()
            logger.info("Successfully authenticated with Kaggle API")
            return api
        except Exception as e:
            logger.error(f"Failed to authenticate with Kaggle API: {str(e)}")
            raise
    
    def download_dataset(self, dataset_name: str, chunk_size: Optional[int] = None) -> Path:
        """
        Download the specified dataset.
        
        Args:
            dataset_name (str): Name of the Kaggle dataset (format: username/dataset-name)
            chunk_size (Optional[int]): Number of files to download at once
            
        Returns:
            Path: Path to the downloaded dataset
        """
        try:
            # Create dataset directory
            dataset_dir = self.cache_dir / dataset_name.split('/')[-1]
            dataset_dir.mkdir(parents=True, exist_ok=True)
            
            # Check if dataset is already downloaded
            if dataset_dir.exists() and any(dataset_dir.iterdir()):
                logger.info(f"Dataset directory {dataset_dir} already exists and is not empty.")
                response = input("Do you want to download again? (y/n): ").lower()
                if response != 'y':
                    logger.info("Using existing dataset files.")
                    return dataset_dir
                else:
                    logger.info("Clearing existing dataset directory...")
                    shutil.rmtree(dataset_dir)
                    dataset_dir.mkdir(parents=True)
            
            # Download dataset
            logger.info(f"Starting download of dataset: {dataset_name}")
            logger.info("This might take a while. The dataset is approximately 4GB.")
            logger.info("You can safely interrupt the download with Ctrl+C and resume later.")
            
            start_time = time.time()
            logger.info("Starting download...")
            
            try:
                # First try to get dataset status
                logger.info("Checking dataset status...")
                self.api.dataset_status(dataset_name)
                logger.info("Dataset is accessible, proceeding with download...")
                
                # Start the download
                logger.info("Initiating download process...")
                self.api.dataset_download_files(
                    dataset_name,
                    path=str(dataset_dir),
                    unzip=True,
                    quiet=False  # Show progress
                )
                logger.info("Download command completed")
                
            except Exception as e:
                logger.error(f"Error during download process: {str(e)}")
                raise
            
            end_time = time.time()
            duration = end_time - start_time
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            logger.info(f"Dataset downloaded successfully to {dataset_dir}")
            logger.info(f"Download completed in {int(hours)}h {int(minutes)}m {int(seconds)}s")
            
            # Verify download and list files
            if not any(dataset_dir.iterdir()):
                raise Exception("Download completed but no files were found in the target directory")
            
            # List downloaded files
            logger.info("\nDownloaded files:")
            total_size = 0
            for file in dataset_dir.rglob("*"):
                if file.is_file():
                    size_mb = file.stat().st_size / (1024 * 1024)
                    total_size += size_mb
                    logger.info(f"- {file.relative_to(dataset_dir)} ({size_mb:.2f} MB)")
            logger.info(f"Total size: {total_size:.2f} MB")
                
            return dataset_dir
            
        except KeyboardInterrupt:
            logger.info("\nDownload interrupted by user. You can resume later.")
            raise
        except Exception as e:
            logger.error(f"Failed to download dataset: {str(e)}")
            raise
    
    def get_dataset_info(self, dataset_name: str) -> Dict[str, Any]:
        """
        Get information about the dataset.
        
        Args:
            dataset_name (str): Name of the Kaggle dataset
            
        Returns:
            Dict[str, Any]: Dataset information
        """
        try:
            # Get dataset metadata file path
            metadata_path = self.api.dataset_metadata(dataset_name, path=str(self.cache_dir))
            logger.info(f"Reading metadata from: {metadata_path}")
            
            # Read and parse the metadata file
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.loads(json.load(f))
                
                logger.info("Successfully parsed dataset metadata")
                
                # Extract information from the metadata dictionary
                info = {
                    'title': metadata.get('title', dataset_name),
                    'size': f"{metadata.get('totalDownloads', 0)} downloads",
                    'last_updated': 'N/A',  # Not available in the metadata
                    'download_count': metadata.get('totalDownloads', 'Unknown'),
                    'views': metadata.get('totalViews', 'Unknown'),
                    'votes': metadata.get('totalVotes', 'Unknown')
                }
                
                logger.info(f"Dataset title: {info['title']}")
                logger.info(f"Total downloads: {info['download_count']}")
                logger.info(f"Total views: {info['views']}")
                
                return info
                
            except (json.JSONDecodeError, FileNotFoundError) as e:
                logger.error(f"Failed to read metadata file: {str(e)}")
                # If parsing fails, return basic info
                return {
                    'title': dataset_name,
                    'size': 'Unknown',
                    'last_updated': 'Unknown',
                    'download_count': 'Unknown'
                }
        except Exception as e:
            logger.error(f"Failed to get dataset info: {str(e)}")
            raise
    
    def clear_cache(self) -> None:
        """
        Clear the cache directory.
        """
        try:
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(parents=True)
                logger.info("Cache cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear cache: {str(e)}")
            raise

def main():
    """
    Example usage of the KaggleDataManager.
    """
    # Initialize data manager
    data_manager = KaggleDataManager()
    
    # Get dataset info
    dataset_name = "awsaf49/brats2020-training-data"  # BraTS 2020 dataset
    try:
        # First try to get dataset info
        try:
            info = data_manager.get_dataset_info(dataset_name)
            logger.info(f"Dataset info: {info}")
        except Exception as e:
            logger.warning(f"Could not get dataset info: {str(e)}")
            logger.info("Proceeding with download...")
        
        # Download dataset
        logger.info("Starting download process...")
        dataset_path = data_manager.download_dataset(dataset_name)
        logger.info(f"Dataset downloaded to: {dataset_path}")
        
    except KeyboardInterrupt:
        logger.info("\nProcess interrupted by user. Exiting gracefully...")
    except Exception as e:
        logger.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 