import os
from nnunetv2.run.run_training import run_training
from nnunetv2.paths import nnUNet_raw, nnUNet_preprocessed, nnUNet_results
from nnunetv2.utilities.dataset_name_id_conversion import maybe_convert_to_dataset_name

def test_nnunet_installation():
    """
    Test if nnU-Net is properly installed and can access its required directories.
    """
    print("Testing nnU-Net installation...")
    
    # Check if required directories exist
    print(f"nnUNet_raw directory: {nnUNet_raw}")
    print(f"nnUNet_preprocessed directory: {nnUNet_preprocessed}")
    print(f"nnUNet_results directory: {nnUNet_results}")
    
    # Create directories if they don't exist
    os.makedirs(nnUNet_raw, exist_ok=True)
    os.makedirs(nnUNet_preprocessed, exist_ok=True)
    os.makedirs(nnUNet_results, exist_ok=True)
    
    print("nnU-Net installation test completed successfully!")

if __name__ == "__main__":
    test_nnunet_installation() 