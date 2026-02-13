"""
Priority prediction model for SmartAlloc.
"""

import os
import joblib
import numpy as np
from typing import Dict, Optional, Tuple
from pathlib import Path

from django.conf import settings

from .features_v2 import FeatureEngineerV2, FeatureEngineer
from .features import generate_synthetic_priority_score
from utils.constants import MIN_PRIORITY_SCORE, MAX_PRIORITY_SCORE
from utils.exceptions import ModelNotTrainedError
import logging

logger = logging.getLogger(__name__)


class PriorityPredictor:
    """
    Priority prediction model wrapper.
    
    Uses Random Forest Regressor to predict priority scores
    based on student features.
    """
    
    MODEL_FILENAME = 'priority_model.pkl'
    SCALER_FILENAME = 'scaler.pkl'
    FEATURES_FILENAME = 'feature_names.pkl'
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the predictor.
        
        Args:
            model_path: Path to model files (default: settings.ML_MODEL_PATH)
        """
        self.model_path = Path(model_path or settings.ML_MODEL_PATH)
        self.model = None
        self.scaler = None
        self.feature_engineer = FeatureEngineerV2()
        self.model_version = getattr(settings, 'ML_MODEL_VERSION', 'v1.0.0')
        
        self._load_model()
    
    def _load_model(self):
        """Load the trained model and scaler."""
        model_file = self.model_path / self.MODEL_FILENAME
        scaler_file = self.model_path / self.SCALER_FILENAME
        
        try:
            if model_file.exists():
                self.model = joblib.load(model_file)
                logger.info(f"Loaded model from {model_file}")
            else:
                logger.warning(f"Model file not found: {model_file}")
            
            if scaler_file.exists():
                self.scaler = joblib.load(scaler_file)
                logger.info(f"Loaded scaler from {scaler_file}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = None
            self.scaler = None
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded and ready."""
        return self.model is not None
    
    def predict(
        self,
        student_features: Dict[str, float],
        use_domain_knowledge: bool = False
    ) -> Dict:
        """
        Predict priority score for a student.
        
        Args:
            student_features: Dictionary of student features
            use_domain_knowledge: If True and model not loaded, use synthetic scoring
        
        Returns:
            Dictionary with prediction results:
            {
                'priority_score': float,
                'confidence': float,
                'feature_importance': Dict[str, float],
                'model_version': str,
                'scoring_method': str
            }
        """
        # Extract features
        if hasattr(student_features, 'get'):
            # It's a student profile object, extract features
            if hasattr(student_features, 'current_gpa'):
                features = self.feature_engineer.extract_features(student_features)
            else:
                features = self.feature_engineer.extract_features_from_dict(student_features)
        else:
            features = student_features
        
        # Try ML model prediction
        if self.is_model_loaded():
            try:
                return self._ml_predict(features)
            except Exception as e:
                logger.error(f"ML prediction failed: {e}")
                if not use_domain_knowledge:
                    raise ModelNotTrainedError("ML model prediction failed and fallback disabled")
        
        # Fallback to domain knowledge scoring
        if use_domain_knowledge:
            return self._domain_knowledge_predict(features)
        
        raise ModelNotTrainedError("No trained model available")
    
    def _ml_predict(self, features: Dict[str, float]) -> Dict:
        """
        Predict using the ML model.
        
        Args:
            features: Extracted features dictionary
        
        Returns:
            Prediction results
        """
        # Prepare input
        X = self.feature_engineer.prepare_model_input(features)
        
        # Scale if scaler available
        if self.scaler:
            X = self.scaler.transform(X)
        
        # Predict
        raw_score = self.model.predict(X)[0]
        
        # Clamp score to valid range
        priority_score = max(MIN_PRIORITY_SCORE, min(MAX_PRIORITY_SCORE, raw_score))
        
        # Calculate confidence using prediction intervals if available
        confidence = self._calculate_confidence(X)
        
        # Get feature importance
        feature_importance = self._get_feature_importance()
        
        return {
            'priority_score': round(priority_score, 2),
            'confidence': round(confidence, 4),
            'feature_importance': feature_importance,
            'model_version': self.model_version,
            'scoring_method': 'ml_model',
            'raw_score': round(raw_score, 2),
        }
    
    def _domain_knowledge_predict(self, features: Dict[str, float]) -> Dict:
        """
        Predict using domain knowledge formula.
        
        Args:
            features: Extracted features dictionary
        
        Returns:
            Prediction results
        """
        score = generate_synthetic_priority_score(features)
        
        # Calculate feature contributions
        feature_importance = {
            'gpa_normalized': 0.40,
            'distance_transformed': 0.30,
            'level_encoded': 0.20,
            'disability_flag': 0.05,
            'financial_aid_flag': 0.05,
        }
        
        return {
            'priority_score': round(score, 2),
            'confidence': 0.85,  # Fixed confidence for domain knowledge
            'feature_importance': feature_importance,
            'model_version': 'domain_knowledge_v1',
            'scoring_method': 'domain_knowledge',
            'raw_score': round(score, 2),
        }
    
    def _calculate_confidence(self, X: np.ndarray) -> float:
        """
        Calculate prediction confidence.
        
        For Random Forest, we can use the variance across trees
        as a measure of uncertainty.
        
        Args:
            X: Input features
        
        Returns:
            Confidence score (0-1)
        """
        try:
            if hasattr(self.model, 'estimators_'):
                # Random Forest - calculate variance across trees
                predictions = [tree.predict(X)[0] for tree in self.model.estimators_]
                variance = np.var(predictions)
                
                # Higher variance = lower confidence
                # Normalize: assume max reasonable variance is 100
                confidence = max(0, 1 - (variance / 100))
                return confidence
            else:
                # For other models, return a default confidence
                return 0.9
        except:
            return 0.8  # Default confidence
    
    def _get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance from the model.
        
        Returns:
            Dictionary mapping feature names to importance scores
        """
        try:
            if hasattr(self.model, 'feature_importances_'):
                importances = self.model.feature_importances_
                feature_names = [
                    'level',
                    'gpa',
                    'distance_km',
                    'disability',
                    'medical_condition',
                    'financial_need',
                    'first_generation',
                    'international',
                    'previous_housing',
                    'semesters_completed',
                    'academic_probation',
                    'family_size',
                    'family_income_bracket',
                    'employment_hours',
                    'gender_M',
                    'gender_F',
                    'gender_Other',
                ]
                
                return {
                    name: round(float(imp), 4)
                    for name, imp in zip(feature_names, importances)
                }
        except Exception as e:
            logger.error(f"Error getting feature importance: {e}")
        
        # Default equal importance
        return {
            'gpa_normalized': 0.20,
            'level_encoded': 0.20,
            'distance_transformed': 0.20,
            'disability_flag': 0.20,
            'financial_aid_flag': 0.20,
        }
    
    def batch_predict(
        self,
        students_data: list,
        use_domain_knowledge: bool = False
    ) -> list:
        """
        Predict priority scores for multiple students.
        
        Args:
            students_data: List of student data dictionaries or profile objects
            use_domain_knowledge: Whether to use domain knowledge fallback
        
        Returns:
            List of prediction result dictionaries
        """
        results = []
        
        for student_data in students_data:
            try:
                prediction = self.predict(student_data, use_domain_knowledge)
                prediction['student_id'] = getattr(student_data, 'id', student_data.get('id'))
                results.append(prediction)
            except Exception as e:
                logger.error(f"Prediction failed for student: {e}")
                results.append({
                    'student_id': getattr(student_data, 'id', student_data.get('id')),
                    'error': str(e),
                    'priority_score': None,
                })
        
        return results
    
    def get_model_info(self) -> Dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        info = {
            'model_version': self.model_version,
            'is_loaded': self.is_model_loaded(),
            'model_path': str(self.model_path),
        }
        
        if self.is_model_loaded():
            info['model_type'] = type(self.model).__name__
            
            if hasattr(self.model, 'n_features_in_'):
                info['n_features'] = self.model.n_features_in_
            
            if hasattr(self.model, 'n_estimators'):
                info['n_estimators'] = self.model.n_estimators
        
        return info


# Singleton instance for reuse
_predictor_instance = None


def get_predictor() -> PriorityPredictor:
    """
    Get or create the singleton predictor instance.
    
    Returns:
        PriorityPredictor instance
    """
    global _predictor_instance
    
    if _predictor_instance is None:
        _predictor_instance = PriorityPredictor()
    
    return _predictor_instance
