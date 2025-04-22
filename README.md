# Gesture-glove

**Gesture-glove** is a machine learning-powered system designed to recognize hand gestures using sensor data from a wearable glove. It processes data from multiple sensors to classify gestures like "clap," "pinch," and "snap." This project aims to facilitate intuitive human-computer interaction, with potential applications in assistive technology, gaming, and virtual reality.

## Features

- Synthetic data generation for training purposes
- Custom PyTorch `Dataset` class for efficient data loading
- Neural network model with adaptive pooling to handle variable-length sequences
- Support for GPU acceleration using CUDA or MPS
- Visualization tools for data inspection

## Project Structure

```
gesture-glove/
├── Runs/                   # Contains synthetic sensor data and gesture labels
├── dataset.py              # Custom PyTorch Dataset class
├── model.py                # Neural network model definition
├── train.py                # Training script
├── tests/
│   └── test_dataset.py     # Test script for the dataset
├── generate_fake_runs.py   # Script to generate synthetic data
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PyTorch 1.10+
- Matplotlib

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your_username/gesture-glove.git
cd gesture-glove
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Data Generation

To generate synthetic sensor data:

```bash
python generate_fake_runs.py
```

This will create 50 runs in the `Runs/` directory, each containing sensor logs and a corresponding `gesture.txt` file.

## Training the Model

To train the gesture recognition model:

```bash
python train.py
```

The script will automatically detect and utilize available hardware (CUDA, MPS, or CPU).

## Testing the Dataset

To test the dataset loading and visualize a sample:

```bash
python tests/test_dataset.py
```

This script will display a plot of sensor readings for a randomly selected sample.

## Model Architecture

The model is a 1D Convolutional Neural Network with adaptive pooling to handle variable-length input sequences. It consists of:

- Conv1D layers with ReLU activation
- Adaptive average pooling to compress sequence length
- Fully connected layer + dropout
- Output layer for classification (3 gestures)

## Hardware Acceleration

The training script automatically selects the best available hardware:

- CUDA (NVIDIA GPUs)
- MPS (Apple Silicon)
- CPU (fallback)

Ensure that the appropriate drivers and libraries are installed for GPU acceleration.

## License

This project is licensed under the MIT License.

## Acknowledgments

This project was inspired by various gesture recognition systems and aims to contribute to the field of human-computer interaction.
