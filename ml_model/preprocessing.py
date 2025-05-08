import os
import json
import shutil
from pathlib import Path
import nibabel as nib
import numpy as np
from typing import List, Dict, Any
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BraTS2nnUNetConverter:
    def __init__(self, 
                 input_dir: str = "data/cache/BraTS2024_small_dataset",
                 output_dir: str = "data/nnunet",
                 task_name: str = "Task001_BrainTumor"):
        """
        Initialize the BraTS to nnU-Net converter.
        
        Args:
            input_dir (str): Directory containing the BraTS dataset
            output_dir (str): Directory where nnU-Net formatted data will be saved
            task_name (str): Name of the nnU-Net task
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.task_name = task_name
        self.task_dir = self.output_dir / task_name
        
        # Create necessary directories
        self.images_dir = self.task_dir / "imagesTr"
        self.labels_dir = self.task_dir / "labelsTr"
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.labels_dir.mkdir(parents=True, exist_ok=True)
        
    def convert_dataset(self):
        """
        Convert the BraTS dataset to nnU-Net format.
        """
        logger.info("Starting conversion of BraTS dataset to nnU-Net format...")
        
        # Get all patient directories
        patient_dirs = [d for d in self.input_dir.iterdir() if d.is_dir()]
        logger.info(f"Found {len(patient_dirs)} patients")
        
        # Process each patient
        for patient_dir in tqdm(patient_dirs, desc="Processing patients"):
            self._process_patient(patient_dir)
        
        # Create dataset.json
        self._create_dataset_json()
        
        logger.info("Conversion completed successfully!")
        
    def _process_patient(self, patient_dir: Path):
        """
        Process a single patient's data.
        
        Args:
            patient_dir (Path): Path to the patient's directory
        """
        patient_id = patient_dir.name
        logger.info(f"Processing patient {patient_id}")
        
        # Get the four MRI modalities (2024 format)
        modalities = {
            't1n': patient_dir / f"{patient_id}-t1n.nii",
            't1c': patient_dir / f"{patient_id}-t1c.nii",
            't2w': patient_dir / f"{patient_id}-t2w.nii",
            't2f': patient_dir / f"{patient_id}-t2f.nii"
        }
        
        # Get the segmentation mask
        seg_path = patient_dir / f"{patient_id}-seg.nii"
        
        # Verify all files exist
        if not all(path.exists() for path in modalities.values()):
            logger.warning(f"Missing files for patient {patient_id}, skipping...")
            return
        if not seg_path.exists():
            logger.warning(f"Missing segmentation for patient {patient_id}, skipping...")
            return
        
        # Create the 4D image by stacking modalities
        try:
            # Load and stack modalities
            image_data = []
            for modality in ['t1n', 't1c', 't2w', 't2f']:
                img = nib.load(modalities[modality])
                image_data.append(img.get_fdata())
            
            # Stack along the channel dimension
            image_data = np.stack(image_data, axis=-1)
            
            # Create the output image
            output_img = nib.Nifti1Image(image_data, img.affine)
            output_path = self.images_dir / f"{patient_id}_0000.nii.gz"
            nib.save(output_img, output_path)
            
            # Copy the segmentation
            shutil.copy2(seg_path, self.labels_dir / f"{patient_id}.nii.gz")
            
            logger.info(f"Successfully processed patient {patient_id}")
            
        except Exception as e:
            logger.error(f"Error processing patient {patient_id}: {str(e)}")
    
    def _create_dataset_json(self):
        """
        Create the dataset.json file required by nnU-Net.
        """
        dataset_json = {
            "name": self.task_name,
            "description": "BraTS 2024 Brain Tumor Segmentation Dataset",
            "reference": "BraTS 2024 Challenge",
            "licence": "CC0-1.0",
            "release": "1.0",
            "tensorImageSize": "4D",
            "modality": {
                "0": "T1n",
                "1": "T1c",
                "2": "T2w",
                "3": "T2f"
            },
            "labels": {
                "0": "background",
                "1": "NCR/NET",
                "2": "ED",
                "3": "ET"
            },
            "numTraining": len(list(self.images_dir.glob("*.nii.gz"))),
            "numTest": 0,
            "training": [
                {
                    "image": f"./imagesTr/{img.name}",
                    "label": f"./labelsTr/{img.stem.split('_')[0]}.nii.gz"
                }
                for img in self.images_dir.glob("*.nii.gz")
            ],
            "test": []
        }
        
        # Save the dataset.json file
        with open(self.task_dir / "dataset.json", "w") as f:
            json.dump(dataset_json, f, indent=4)
        
        logger.info("Created dataset.json file")

def main():
    """
    Example usage of the BraTS to nnU-Net converter.
    """
    converter = BraTS2nnUNetConverter()
    converter.convert_dataset()

if __name__ == "__main__":
    main() 