# Churn Prediction System

A deep learning-based system for predicting customer churn in subscription-based businesses. This project uses a neural network model to analyze customer data and predict the likelihood of customer churn.

## Features

- Deep learning model using TensorFlow/Keras
- Interactive web dashboard using Flask and Dash
- Real-time predictions
- Feature importance visualization
- Data preprocessing pipeline
- Responsive and modern UI

## Project Structure

```
churn-prediction/
├── app.py                 # Main Flask application
├── requirements.txt       # Project dependencies
├── models/
│   └── neural_network.py # Neural network model implementation
├── data/
│   └── preprocessing.py  # Data preprocessing utilities
└── utils/
    └── visualization.py  # Visualization utilities
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd churn-prediction
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## Model Architecture

The neural network model consists of:
- Input layer with 10 features
- Three hidden layers (64, 32, and 16 neurons)
- Dropout layers (0.3) for regularization
- Output layer with sigmoid activation

## Features Used for Prediction

- Tenure (months)
- Monthly charges
- Contract type
- Payment method

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 