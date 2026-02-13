"""
Training pipeline for the priority scoring model.
"""

import os
import sys
import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

try:
    import django
    django.setup()
except ImportError:
    pass

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from .features import FeatureEngineer, generate_synthetic_priority_score
from utils.constants import MIN_PRIORITY_SCORE, MAX_PRIORITY_SCORE
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_synthetic_data(n_samples: int = 5000, random_state: int = 42) -> pd.DataFrame:
    """
    Generate synthetic training data.
    
    Args:
        n_samples: Number of samples to generate
        random_state: Random seed for reproducibility
    
    Returns:
        DataFrame with synthetic student data
    """
    np.random.seed(random_state)
    
    # Generate random features
    data = {
        'gpa': np.random.uniform(0.0, 5.0, n_samples),
        'level': np.random.choice([100, 200, 300, 400, 500], n_samples),
        'distance': np.random.exponential(50, n_samples),  # Exponential distribution for distance
        'disability': np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),
        'financial_aid': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
    }
    
    df = pd.DataFrame(data)
    
    # Generate priority scores using domain knowledge
    feature_engineer = FeatureEngineer()
    
    def calculate_priority(row):
        features = feature_engineer.extract_features_from_dict({
            'gpa': row['gpa'],
            'level': row['level'],
            'distance': row['distance'],
            'disability': bool(row['disability']),
            'financial_aid': bool(row['financial_aid']),
        })
        
        score = generate_synthetic_priority_score(features)
        
        # Add some noise for realism
        noise = np.random.normal(0, 3)
        return max(MIN_PRIORITY_SCORE, min(MAX_PRIORITY_SCORE, score + noise))
    
    df['priority_score'] = df.apply(calculate_priority, axis=1)
    
    return df


def prepare_features(df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """
    Prepare features and target from DataFrame.
    
    Args:
        df: DataFrame with raw data
    
    Returns:
        Tuple of (X, y) arrays
    """
    feature_engineer = FeatureEngineer()
    
    # Extract features for each row
    features_list = []
    for _, row in df.iterrows():
        features = feature_engineer.extract_features_from_dict({
            'gpa': row['gpa'],
            'level': row['level'],
            'distance': row['distance'],
            'disability': bool(row['disability']),
            'financial_aid': bool(row['financial_aid']),
        })
        features_list.append(features)
    
    feature_df = pd.DataFrame(features_list)
    
    # Select features for model
    feature_cols = [
        'gpa_normalized',
        'level_encoded',
        'distance_transformed',
        'disability_flag',
        'financial_aid_flag',
    ]
    
    X = feature_df[feature_cols].values
    y = df['priority_score'].values
    
    return X, y


def train_model(
    X: np.ndarray,
    y: np.ndarray,
    test_size: float = 0.2,
    random_state: int = 42
) -> Tuple[RandomForestRegressor, StandardScaler, dict]:
    """
    Train the Random Forest model.
    
    Args:
        X: Feature matrix
        y: Target vector
        test_size: Fraction of data for testing
        random_state: Random seed
    
    Returns:
        Tuple of (model, scaler, metrics)
    """
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    logger.info("Training Random Forest Regressor...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=random_state,
        n_jobs=-1,
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    
    metrics = {
        'mse': mean_squared_error(y_test, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
        'mae': mean_absolute_error(y_test, y_pred),
        'r2': r2_score(y_test, y_pred),
    }
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
    metrics['cv_r2_mean'] = cv_scores.mean()
    metrics['cv_r2_std'] = cv_scores.std()
    
    logger.info(f"Model metrics: {metrics}")
    
    return model, scaler, metrics


def save_model(
    model: RandomForestRegressor,
    scaler: StandardScaler,
    output_dir: str,
    version: str = 'v1.0.0'
) -> dict:
    """
    Save the trained model and scaler.
    
    Args:
        model: Trained model
        scaler: Fitted scaler
        output_dir: Directory to save files
        version: Model version
    
    Returns:
        Dictionary with saved file paths
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save model
    model_file = output_path / 'priority_model.pkl'
    joblib.dump(model, model_file)
    logger.info(f"Model saved to {model_file}")
    
    # Save scaler
    scaler_file = output_path / 'scaler.pkl'
    joblib.dump(scaler, scaler_file)
    logger.info(f"Scaler saved to {scaler_file}")
    
    # Save metadata
    metadata = {
        'version': version,
        'created_at': datetime.now().isoformat(),
        'model_type': 'RandomForestRegressor',
        'n_estimators': model.n_estimators,
        'max_depth': model.max_depth,
        'feature_names': [
            'gpa_normalized',
            'level_encoded',
            'distance_transformed',
            'disability_flag',
            'financial_aid_flag',
        ],
    }
    
    metadata_file = output_path / 'metadata.json'
    import json
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Metadata saved to {metadata_file}")
    
    return {
        'model': str(model_file),
        'scaler': str(scaler_file),
        'metadata': str(metadata_file),
    }


def run_training_pipeline(
    n_samples: int = 5000,
    output_dir: Optional[str] = None,
    version: str = 'v1.0.0'
) -> dict:
    """
    Run the complete training pipeline.
    
    Args:
        n_samples: Number of synthetic samples to generate
        output_dir: Directory to save model files
        version: Model version
    
    Returns:
        Dictionary with training results
    """
    logger.info("=" * 50)
    logger.info("Starting Training Pipeline")
    logger.info("=" * 50)
    
    # Generate synthetic data
    logger.info(f"Generating {n_samples} synthetic samples...")
    df = generate_synthetic_data(n_samples)
    logger.info(f"Generated {len(df)} samples")
    
    # Prepare features
    logger.info("Preparing features...")
    X, y = prepare_features(df)
    logger.info(f"Feature matrix shape: {X.shape}")
    
    # Train model
    model, scaler, metrics = train_model(X, y)
    
    # Save model
    if output_dir is None:
        output_dir = Path(__file__).parent / 'artifacts'
    
    files = save_model(model, scaler, output_dir, version)
    
    results = {
        'status': 'success',
        'metrics': metrics,
        'files': files,
        'n_samples': n_samples,
        'version': version,
    }
    
    logger.info("=" * 50)
    logger.info("Training Pipeline Complete")
    logger.info(f"R² Score: {metrics['r2']:.4f}")
    logger.info(f"RMSE: {metrics['rmse']:.4f}")
    logger.info("=" * 50)
    
    return results


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Train priority scoring model')
    parser.add_argument(
        '--samples',
        type=int,
        default=5000,
        help='Number of synthetic samples to generate'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Output directory for model files'
    )
    parser.add_argument(
        '--version',
        type=str,
        default='v1.0.0',
        help='Model version'
    )
    
    args = parser.parse_args()
    
    results = run_training_pipeline(
        n_samples=args.samples,
        output_dir=args.output,
        version=args.version
    )
    
    print("\nTraining Results:")
    print(f"Status: {results['status']}")
    print(f"R² Score: {results['metrics']['r2']:.4f}")
    print(f"RMSE: {results['metrics']['rmse']:.4f}")
    print(f"Files saved: {results['files']}")
