"""
Specialized synthetic data generator for SmartAlloc housing allocation.

This generates realistic university housing data with proper distributions,
correlations, and realistic allocation outcomes based on university policies.
"""

import os
import sys
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))

try:
    import django
    django.setup()
except ImportError:
    pass

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import joblib
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class HousingDataGenerator:
    """
    Generates realistic synthetic data for university housing allocation.
    
    Models real-world scenarios:
    - GPA distribution (skewed towards higher GPAs)
    - Level distribution (more lower-level students)
    - Distance from campus (urban vs rural students)
    - Disability accommodations (rare but prioritized)
    - Financial need (correlated with distance and GPA)
    - Gender distribution
    - Academic performance trends
    """
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.rng = np.random.RandomState(random_state)
        
    def generate_student_features(self, n_samples: int) -> pd.DataFrame:
        """
        Generate realistic student feature distributions.
        """
        logger.info(f"Generating {n_samples} student profiles...")
        
        data = {}
        
        # 1. ACADEMIC LEVEL (100-500)
        # More lower-level students (freshmen/sophomores need housing more)
        level_probs = [0.35, 0.30, 0.20, 0.12, 0.03]  # 100, 200, 300, 400, 500
        data['level'] = self.rng.choice([100, 200, 300, 400, 500], 
                                        size=n_samples, p=level_probs)
        
        # 2. GPA (0.0 - 5.0)
        # Skewed normal distribution (most students 2.5-4.5)
        # Lower levels tend to have more variable GPAs
        gpa_base = self.rng.beta(5, 2, n_samples) * 4.0 + 0.5  # Beta distribution
        # Add noise based on level
        level_noise = (500 - data['level']) / 500 * 0.3  # Lower levels more variance
        data['gpa'] = np.clip(gpa_base + self.rng.normal(0, level_noise), 0.5, 5.0)
        
        # 3. DISTANCE FROM CAMPUS (km)
        # Bimodal distribution: local students (nearby) + distant students
        # 40% local (< 20km), 60% from various distances
        is_local = self.rng.random(n_samples) < 0.40
        distance = np.zeros(n_samples)
        distance[is_local] = self.rng.exponential(10, is_local.sum())  # Local
        distance[~is_local] = self.rng.gamma(2, 40, (~is_local).sum()) + 20  # Distant
        data['distance_km'] = np.clip(distance, 1, 500)
        
        # 4. DISABILITY/ACCOMMODATION NEEDS
        # ~5% of students need disability accommodations
        # Higher correlation with medical conditions
        data['disability'] = self.rng.choice([0, 1], n_samples, p=[0.95, 0.05])
        
        # 5. CHRONIC MEDICAL CONDITIONS
        # ~3% have serious medical conditions requiring housing priority
        data['medical_condition'] = self.rng.choice([0, 1], n_samples, p=[0.97, 0.03])
        
        # 6. FINANCIAL NEED
        # Correlated with: distance (farther = need housing more), GPA (aid eligibility)
        # Base probability
        financial_prob = 0.25  # 25% base need
        # Adjust based on distance (farther = more need)
        distance_factor = np.clip(data['distance_km'] / 200, 0, 0.20)
        # Adjust based on disability (higher need)
        disability_factor = data['disability'] * 0.15
        # Combine probabilities
        financial_probs = np.clip(financial_prob + distance_factor + disability_factor, 0, 0.8)
        data['financial_need'] = (self.rng.random(n_samples) < financial_probs).astype(int)
        
        # 7. FIRST GENERATION STUDENT
        # ~20% are first-gen (often need more support)
        data['first_generation'] = self.rng.choice([0, 1], n_samples, p=[0.80, 0.20])
        
        # 8. INTERNATIONAL STUDENT
        # ~10% international (often need guaranteed housing)
        data['international'] = self.rng.choice([0, 1], n_samples, p=[0.90, 0.10])
        # International students are typically farther
        data['distance_km'] = np.where(data['international'] == 1, 
                                       self.rng.uniform(1000, 15000, n_samples),
                                       data['distance_km'])
        
        # 9. GENDER
        data['gender'] = self.rng.choice(['M', 'F', 'Other'], n_samples, p=[0.48, 0.48, 0.04])
        
        # 10. PREVIOUS HOUSING STATUS
        # Some students lived on campus before
        data['previous_housing'] = self.rng.choice([0, 1], n_samples, p=[0.70, 0.30])
        
        # 11. SEMESTERS COMPLETED
        data['semesters_completed'] = ((data['level'] - 100) / 100 * 2 + 
                                       self.rng.randint(0, 2, n_samples))
        
        # 12. ACADEMIC PROBATION
        # ~5% on probation (lower priority)
        data['academic_probation'] = (data['gpa'] < 2.0).astype(int)
        # But not too many
        probation_mask = data['academic_probation'] == 1
        data['academic_probation'][probation_mask] = self.rng.choice(
            [0, 1], probation_mask.sum(), p=[0.3, 0.7]
        )
        
        # 13. FAMILY SIZE (for dependency calculation)
        data['family_size'] = self.rng.choice([1, 2, 3, 4, 5, 6], n_samples, 
                                               p=[0.05, 0.15, 0.30, 0.30, 0.15, 0.05])
        
        # 14. FAMILY INCOME BRACKET (1-10, 10 = highest income)
        # Correlated with financial need (inverse)
        income_base = self.rng.normal(5.5, 2, n_samples)
        income_adjustment = data['financial_need'] * (-2)  # Lower income if financial need
        data['family_income_bracket'] = np.clip(
            (income_base + income_adjustment).astype(int), 1, 10
        )
        
        # 15. EMPLOYMENT STATUS (hours per week)
        # Higher for financial need students
        employment_base = self.rng.exponential(10, n_samples)
        employment_boost = data['financial_need'] * self.rng.uniform(5, 20, n_samples)
        data['employment_hours'] = np.clip(employment_base + employment_boost, 0, 40)
        
        df = pd.DataFrame(data)
        logger.info(f"Generated {len(df)} student profiles")
        return df
    
    def calculate_priority_score(self, row: pd.Series) -> float:
        """
        Calculate realistic priority score based on university housing policy.
        
        Priority factors (realistic weights):
        - Distance from campus (30%): Farther = higher priority
        - Academic level (20%): Higher levels = slight priority
        - GPA (15%): Higher GPA = slight priority (merit)
        - Financial need (15%): Higher need = priority
        - Disability/Medical (10%): Automatic high priority
        - International status (5%): Guaranteed housing
        - First generation (5%): Support priority
        """
        score = 50.0  # Base score
        
        # Distance component (0-30 points)
        # Exponential scale: closer gets less, farther gets more
        distance_score = min(30, (row['distance_km'] ** 0.7) * 1.5)
        score += distance_score
        
        # Academic level component (0-20 points)
        level_score = (row['level'] / 500) * 20
        score += level_score
        
        # GPA component (0-15 points)
        gpa_score = (row['gpa'] / 5.0) * 15
        score += gpa_score
        
        # Financial need (0-15 points)
        if row['financial_need']:
            score += 15
        
        # Disability/Medical (0-10 points) - HIGH PRIORITY
        if row['disability']:
            score += 10
        if row['medical_condition']:
            score += 8
        
        # International students (0-5 points)
        if row['international']:
            score += 5
        
        # First generation (0-5 points)
        if row['first_generation']:
            score += 5
        
        # Academic probation penalty (-10 points)
        if row['academic_probation']:
            score -= 10
        
        # Employment hours bonus (working students need housing more)
        if row['employment_hours'] > 20:
            score += 3
        
        # Clip to valid range
        return np.clip(score, 0, 100)
    
    def generate_training_data(self, n_samples: int = 10000, 
                               add_noise: bool = True) -> pd.DataFrame:
        """
        Generate complete training dataset with priority scores.
        """
        logger.info("=" * 60)
        logger.info("GENERATING SPECIALIZED SYNTHETIC DATA")
        logger.info("=" * 60)
        
        # Generate features
        df = self.generate_student_features(n_samples)
        
        # Calculate priority scores
        logger.info("Calculating priority scores...")
        df['priority_score'] = df.apply(self.calculate_priority_score, axis=1)
        
        # Add realistic noise
        if add_noise:
            noise = self.rng.normal(0, 2, n_samples)  # Small noise
            df['priority_score'] = np.clip(df['priority_score'] + noise, 0, 100)
        
        # Round scores
        df['priority_score'] = df['priority_score'].round(2)
        
        # Add allocation outcome (simulated historical data)
        # Assume threshold for allocation varies by availability
        # Higher scores more likely to be allocated
        allocation_threshold = self.rng.uniform(40, 60)  # Variable threshold
        allocation_prob = 1 / (1 + np.exp(-(df['priority_score'] - allocation_threshold) / 10))
        df['was_allocated'] = (self.rng.random(n_samples) < allocation_prob).astype(int)
        
        # Generate timestamps for historical data
        base_date = datetime(2023, 1, 1)
        df['application_date'] = [
            base_date + timedelta(days=int(self.rng.randint(0, 365)))
            for _ in range(n_samples)
        ]
        
        logger.info(f"\nDataset Summary:")
        logger.info(f"  Total samples: {len(df)}")
        logger.info(f"  Allocated: {df['was_allocated'].sum()} ({df['was_allocated'].mean()*100:.1f}%)")
        logger.info(f"  Avg priority score: {df['priority_score'].mean():.2f}")
        logger.info(f"  Score std: {df['priority_score'].std():.2f}")
        
        return df
    
    def save_dataset(self, df: pd.DataFrame, output_dir: str = None):
        """Save the generated dataset."""
        if output_dir is None:
            output_dir = Path(__file__).parent / 'artifacts'
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save as CSV
        csv_path = output_dir / 'training_data.csv'
        df.to_csv(csv_path, index=False)
        logger.info(f"\nDataset saved to: {csv_path}")
        
        # Save statistics
        stats = {
            'n_samples': len(df),
            'allocated_count': int(df['was_allocated'].sum()),
            'allocation_rate': float(df['was_allocated'].mean()),
            'priority_score_mean': float(df['priority_score'].mean()),
            'priority_score_std': float(df['priority_score'].std()),
            'feature_columns': [c for c in df.columns if c not in ['priority_score', 'was_allocated', 'application_date']],
            'generated_at': datetime.now().isoformat()
        }
        
        stats_path = output_dir / 'dataset_stats.json'
        with open(stats_path, 'w') as f:
            json.dump(stats, f, indent=2)
        logger.info(f"Statistics saved to: {stats_path}")
        
        return csv_path, stats_path


def train_priority_model(df: pd.DataFrame, output_dir: str = None, 
                         model_version: str = 'v2.0.0') -> Dict:
    """
    Train a priority prediction model on the synthetic data.
    """
    logger.info("\n" + "=" * 60)
    logger.info("TRAINING PRIORITY PREDICTION MODEL")
    logger.info("=" * 60)
    
    if output_dir is None:
        output_dir = Path(__file__).parent / 'artifacts'
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Feature engineering
    feature_cols = [
        'level', 'gpa', 'distance_km', 'disability', 'medical_condition',
        'financial_need', 'first_generation', 'international', 'previous_housing',
        'semesters_completed', 'academic_probation', 'family_size',
        'family_income_bracket', 'employment_hours'
    ]
    
    # Encode gender
    df_encoded = df.copy()
    df_encoded['gender_M'] = (df_encoded['gender'] == 'M').astype(int)
    df_encoded['gender_F'] = (df_encoded['gender'] == 'F').astype(int)
    df_encoded['gender_Other'] = (df_encoded['gender'] == 'Other').astype(int)
    feature_cols.extend(['gender_M', 'gender_F', 'gender_Other'])
    
    X = df_encoded[feature_cols].values
    y = df_encoded['priority_score'].values
    
    logger.info(f"Feature matrix shape: {X.shape}")
    logger.info(f"Features: {feature_cols}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = RobustScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model with hyperparameter tuning
    logger.info("\nTraining Gradient Boosting Regressor...")
    
    model = GradientBoostingRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.1,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    
    metrics = {
        'mse': float(mean_squared_error(y_test, y_pred)),
        'rmse': float(np.sqrt(mean_squared_error(y_test, y_pred))),
        'mae': float(mean_absolute_error(y_test, y_pred)),
        'r2': float(r2_score(y_test, y_pred)),
        'mape': float(np.mean(np.abs((y_test - y_pred) / (y_test + 1e-8))) * 100)
    }
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
    metrics['cv_r2_mean'] = float(cv_scores.mean())
    metrics['cv_r2_std'] = float(cv_scores.std())
    
    logger.info("\nModel Performance:")
    logger.info(f"  R² Score: {metrics['r2']:.4f}")
    logger.info(f"  RMSE: {metrics['rmse']:.4f}")
    logger.info(f"  MAE: {metrics['mae']:.4f}")
    logger.info(f"  CV R²: {metrics['cv_r2_mean']:.4f} (+/- {metrics['cv_r2_std']:.4f})")
    
    # Feature importance
    feature_importance = dict(zip(feature_cols, model.feature_importances_))
    sorted_importance = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    
    logger.info("\nTop 10 Feature Importances:")
    for feat, imp in sorted_importance[:10]:
        logger.info(f"  {feat}: {imp:.4f}")
    
    # Save model
    model_path = output_dir / 'priority_model_v2.pkl'
    joblib.dump(model, model_path)
    logger.info(f"\nModel saved to: {model_path}")
    
    scaler_path = output_dir / 'scaler_v2.pkl'
    joblib.dump(scaler, scaler_path)
    logger.info(f"Scaler saved to: {scaler_path}")
    
    # Save feature names
    feature_path = output_dir / 'feature_names_v2.pkl'
    joblib.dump(feature_cols, feature_path)
    logger.info(f"Feature names saved to: {feature_path}")
    
    # Save metadata
    metadata = {
        'version': model_version,
        'created_at': datetime.now().isoformat(),
        'model_type': 'GradientBoostingRegressor',
        'n_estimators': model.n_estimators,
        'max_depth': model.max_depth,
        'learning_rate': model.learning_rate,
        'feature_names': feature_cols,
        'metrics': metrics,
        'feature_importance': {k: float(v) for k, v in feature_importance.items()},
        'n_training_samples': len(X_train),
        'n_test_samples': len(X_test)
    }
    
    metadata_path = output_dir / 'model_metadata_v2.json'
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    logger.info(f"Metadata saved to: {metadata_path}")
    
    results = {
        'model': model,
        'scaler': scaler,
        'metrics': metrics,
        'feature_importance': feature_importance,
        'paths': {
            'model': str(model_path),
            'scaler': str(scaler_path),
            'features': str(feature_path),
            'metadata': str(metadata_path)
        }
    }
    
    return results


def main():
    """Main function to generate data and train model."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate synthetic housing data and train model')
    parser.add_argument('--samples', type=int, default=10000, help='Number of samples')
    parser.add_argument('--output', type=str, default=None, help='Output directory')
    parser.add_argument('--version', type=str, default='v2.0.0', help='Model version')
    parser.add_argument('--skip-training', action='store_true', help='Only generate data')
    
    args = parser.parse_args()
    
    # Generate data
    generator = HousingDataGenerator(random_state=42)
    df = generator.generate_training_data(n_samples=args.samples)
    
    # Save dataset
    csv_path, stats_path = generator.save_dataset(df, args.output)
    
    # Train model
    if not args.skip_training:
        results = train_priority_model(df, args.output, args.version)
        
        print("\n" + "=" * 60)
        print("TRAINING COMPLETE!")
        print("=" * 60)
        print(f"Model Version: {args.version}")
        print(f"R² Score: {results['metrics']['r2']:.4f}")
        print(f"RMSE: {results['metrics']['rmse']:.4f}")
        print(f"Files saved to: {results['paths']['model']}")
    
    print(f"\nDataset saved to: {csv_path}")
    print(f"View it with: head {csv_path}")


if __name__ == '__main__':
    main()
