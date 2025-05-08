from nnunetv2.dataset_conversion.generate_dataset_json import generate_dataset_json
from batchgenerators.utilities.file_and_folder_operations import join, subdirs, subfiles, maybe_mkdir_p
from nnunetv2.paths import nnUNet_raw
import os
import shutil

if __name__ == '__main__':
    """
    Convert BraTS 2024 dataset to nnU-Net format
    """
    # Update path to our local dataset
    extracted_BraTS2024_GLI_dir = os.path.join('data', 'cache', 'BraTS2024_small_dataset')
    nnunet_dataset_name = 'BraTS2024-BraTS-GLI'
    nnunet_dataset_id = 226
    dataset_name = f'Dataset{nnunet_dataset_id:03d}_{nnunet_dataset_name}'
    dataset_dir = join(nnUNet_raw, dataset_name)
    
    # Create required directories
    imagesTr_dir = join(dataset_dir, 'imagesTr')
    labelsTr_dir = join(dataset_dir, 'labelsTr')
    maybe_mkdir_p(imagesTr_dir)
    maybe_mkdir_p(labelsTr_dir)

    # Process each case
    dataset = {}
    casenames = subdirs(extracted_BraTS2024_GLI_dir, join=False)
    for c in casenames:
        # Copy and rename images with correct modality identifiers
        modalities = {
            't1n': '0000',
            't1c': '0001',
            't2w': '0002',
            't2f': '0003'
        }
        
        # Copy and rename each modality
        for modality, identifier in modalities.items():
            src = join(extracted_BraTS2024_GLI_dir, c, f"{c}-{modality}.nii")
            dst = join(imagesTr_dir, f"{c}_{identifier}.nii")
            shutil.copy2(src, dst)
        
        # Copy segmentation
        src_seg = join(extracted_BraTS2024_GLI_dir, c, f"{c}-seg.nii")
        dst_seg = join(labelsTr_dir, f"{c}.nii")
        shutil.copy2(src_seg, dst_seg)
        
        # Add to dataset dictionary
        dataset[c] = {
            'label': dst_seg,
            'images': [
                join(imagesTr_dir, f"{c}_0000.nii"),
                join(imagesTr_dir, f"{c}_0001.nii"),
                join(imagesTr_dir, f"{c}_0002.nii"),
                join(imagesTr_dir, f"{c}_0003.nii")
            ]
        }

    # Define labels
    labels = {
        'background': 0,
        'NETC': 1,
        'SNFH': 2,
        'ET': 3,
        'RC': 4,
    }

    # Generate dataset.json
    generate_dataset_json(
        dataset_dir,
        {
            0: 'T1n',
            1: "T1c",
            2: "T2w",
            3: "T2f"
        },
        labels,
        num_training_cases=len(dataset),
        file_ending='.nii',
        regions_class_order=None,
        dataset_name=dataset_name,
        reference='https://www.synapse.org/Synapse:syn53708249/wiki/627500',
        license='see https://www.synapse.org/Synapse:syn53708249/wiki/627508',
        dataset=dataset,
        description='BraTS 2024 dataset converted to nnU-Net format'
    )
