# TumorLens - Brain Tumor Detection System

A web application for detecting brain tumors in MRI scans using deep learning. The system uses the BraTS 2020 dataset for training and provides a user-friendly interface for medical professionals to upload and analyze MRI scans.

## Features

- MRI scan upload and preprocessing
- Deep learning-based tumor detection
- Interactive visualization of results
- Support for multiple MRI modalities (T1, T1c, T2, FLAIR)
- Detailed analysis reports

## Project Structure

```
TumorLens/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
├── ml_model/          # Model training and inference
├── data/             # Data processing utilities
└── docs/             # Documentation
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- CUDA-compatible GPU (recommended for training)

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## Dataset

This project uses the BraTS 2020 dataset. To use the dataset:

1. Register at the [BraTS 2020 challenge website](https://www.med.upenn.edu/cbica/brats2020/registration.html)
2. Download the dataset
3. Place the dataset in the `data/raw` directory

## License

MIT License

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests. 