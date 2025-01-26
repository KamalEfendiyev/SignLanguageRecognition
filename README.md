# Gesture Image Classification using VGG19

This project implements a gesture image classification model using transfer learning with the VGG19 architecture. The model is trained to classify gesture images into one of 37 categories.

## Features

- Utilizes VGG19 pretrained on ImageNet for transfer learning.
- Preprocessing of gesture image data, including resizing and normalization.
- Splits dataset into training, testing, and evaluation subsets.
- Implements dropout and batch normalization to reduce overfitting.
- Evaluates model performance using metrics such as accuracy and classification reports.

## Dataset

The dataset directory structure should be as follows:
/Gesture Image Data/ ├── val/ ├── class1/ ├── class2/ ├── ...


## Prerequisites

- Python 3.x
- Libraries:
  - numpy
  - tensorflow
  - keras
  - sklearn
  - matplotlib
  - OpenCV (cv2)

Install dependencies using:
```bash
pip install numpy tensorflow keras scikit-learn matplotlib opencv-python
File Description
The script performs the following tasks:

Loads and preprocesses gesture image data.
Splits the data into training, testing, and evaluation sets.
Builds and trains a gesture classification model based on VGG19.
Outputs evaluation metrics, including accuracy and a classification report.
How to Run
Dataset Preparation:
Ensure the gesture image dataset is available and follows the specified directory structure. Update the data_dir variable in the script to point to the dataset location.

Run the Script:
Execute the script using:

python gesture_classification.py
Model Training:
The model will train for 25 epochs by default. You can adjust the number of epochs and batch size in the model.fit section.

Model Evaluation:
After training, the script evaluates the model on the test set and prints metrics such as accuracy, loss, and a classification report.

Model Architecture
The model architecture is based on VGG19 and includes:

Base: VGG19 (excluding the top layers).
Fully connected layers:
512 neurons, ReLU activation, dropout (40%), batch normalization.
512 neurons, ReLU activation, dropout (30%), batch normalization.
Output Layer: 37 neurons, softmax activation.
Outputs
Model Performance Metrics:
Loss
Accuracy
Classification Report
Confusion Matrix: Detailed metrics such as precision, recall, and F1-score for each class.
Example Training Output
yaml
Копировать
Редактировать
Train images shape: (11800, 50, 50, 3)
Test images shape: (1400, 50, 50, 3)
Evaluate image shape: (156, 50, 50, 3)
Printing the labels: ['class1', 'class2', ..., 'class37']

Epoch 1/25
...
Epoch 25/25

Evaluation Loss: 0.2345, Evaluation Accuracy: 95.67%
Example Classification Report
markdown
Копировать
Редактировать
              precision    recall  f1-score   support
      class1       0.93      0.92      0.93        50
      ...
   class37       0.95      0.96      0.96        40
Notes
Ensure the dataset directory structure and file paths are correct.
Adjust training parameters (epochs, batch size) as needed for your hardware and dataset size.
Experiment with different architectures or hyperparameters to improve performance.
