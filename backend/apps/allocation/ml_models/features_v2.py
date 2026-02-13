"""
Feature engineering v2 for the enhanced priority scoring model.

This version supports 17 features used by the v2 model:
- level, gpa, distance_km
- disability, medical_condition, financial_need
- first_generation, international, previous_housing
- semesters_completed, academic_probation
- family_size, family_income_bracket, employment_hours
- gender_M, gender_F, gender_Other (one-hot encoded)
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional

from utils.constants import MAX_GPA, MIN_GPA, ALLOCATION_CONSTRAINTS


class FeatureEngineerV2:
    """
    Feature engineering for student housing priority scoring (v2 model).
    """
    
    # Feature order must match training
    FEATURE_ORDER = [
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
    
    def __init__(self):
        self.max_distance = ALLOCATION_CONSTRAINTS.get('max_distance_cap', 500)
    
    def extract_features_from_profile(self, student_profile) -> Dict[str, float]:
        """
        Extract all 17 features from student profile.
        
        Args:
            student_profile: StudentProfile model instance
            
        Returns:
            Dictionary with 17 features
        """
        # Handle missing values with defaults
        level = getattr(student_profile, 'current_level', 100) or 100
        gpa = getattr(student_profile, 'current_gpa', 3.0) or 3.0
        distance = getattr(student_profile, 'distance_from_campus', 50) or 50
        
        # Disability and medical
        disability = getattr(student_profile, 'disability_status', False) or False
        medical_condition = getattr(student_profile, 'chronic_medical_condition', False) or False
        
        # Financial and demographic
        financial_need = getattr(student_profile, 'financial_aid_status', False) or False
        first_generation = getattr(student_profile, 'first_generation_student', False) or False
        international = getattr(student_profile, 'international_student', False) or False
        
        # Housing history
        previous_housing = getattr(student_profile, 'previous_housing_status', False) or False
        
        # Academic progress
        semesters_completed = getattr(student_profile, 'semesters_completed', 0) or 0
        academic_probation = getattr(student_profile, 'academic_probation_status', False) or False
        
        # Family info
        family_size = getattr(student_profile, 'family_size', 4) or 4
        family_income_bracket = getattr(student_profile, 'family_income_bracket', 5) or 5
        employment_hours = getattr(student_profile, 'employment_hours_per_week', 0) or 0
        
        # Gender (one-hot encoding)
        gender = getattr(student_profile, 'gender', 'M')
        if gender not in ['M', 'F', 'Other']:
            gender = 'M'
        
        features = {
            'level': float(level),
            'gpa': float(gpa),
            'distance_km': float(min(distance, self.max_distance)),
            'disability': 1.0 if disability else 0.0,
            'medical_condition': 1.0 if medical_condition else 0.0,
            'financial_need': 1.0 if financial_need else 0.0,
            'first_generation': 1.0 if first_generation else 0.0,
            'international': 1.0 if international else 0.0,
            'previous_housing': 1.0 if previous_housing else 0.0,
            'semesters_completed': float(semesters_completed),
            'academic_probation': 1.0 if academic_probation else 0.0,
            'family_size': float(family_size),
            'family_income_bracket': float(family_income_bracket),
            'employment_hours': float(employment_hours),
            'gender_M': 1.0 if gender == 'M' else 0.0,
            'gender_F': 1.0 if gender == 'F' else 0.0,
            'gender_Other': 1.0 if gender == 'Other' else 0.0,
        }
        
        return features
    
    def extract_features_from_dict(self, data: Dict) -> Dict[str, float]:
        """
        Extract features from dictionary with fallbacks for missing keys.
        
        Args:
            data: Dictionary containing student data
            
        Returns:
            Dictionary with 17 features
        """
        features = {
            'level': float(data.get('level', data.get('current_level', 100))),
            'gpa': float(data.get('gpa', data.get('current_gpa', 3.0))),
            'distance_km': float(data.get('distance', data.get('distance_km', data.get('distance_from_campus', 50)))),
            'disability': 1.0 if data.get('disability', data.get('disability_status', False)) else 0.0,
            'medical_condition': 1.0 if data.get('medical_condition', data.get('chronic_medical_condition', False)) else 0.0,
            'financial_need': 1.0 if data.get('financial_need', data.get('financial_aid_status', False)) else 0.0,
            'first_generation': 1.0 if data.get('first_generation', data.get('first_generation_student', False)) else 0.0,
            'international': 1.0 if data.get('international', data.get('international_student', False)) else 0.0,
            'previous_housing': 1.0 if data.get('previous_housing', data.get('previous_housing_status', False)) else 0.0,
            'semesters_completed': float(data.get('semesters_completed', 0)),
            'academic_probation': 1.0 if data.get('academic_probation', data.get('academic_probation_status', False)) else 0.0,
            'family_size': float(data.get('family_size', 4)),
            'family_income_bracket': float(data.get('family_income_bracket', 5)),
            'employment_hours': float(data.get('employment_hours', data.get('employment_hours_per_week', 0))),
            'gender_M': 1.0 if data.get('gender', 'M') == 'M' else 0.0,
            'gender_F': 1.0 if data.get('gender', 'M') == 'F' else 0.0,
            'gender_Other': 1.0 if data.get('gender', 'M') == 'Other' else 0.0,
        }
        
        # Cap distance
        features['distance_km'] = min(features['distance_km'], self.max_distance)
        
        return features
    
    def prepare_model_input(self, features: Dict[str, float]) -> np.ndarray:
        """
        Prepare features for model input (17 features).
        
        Args:
            features: Dictionary of features
            
        Returns:
            Numpy array (1, 17) for model input
        """
        return np.array([[features[f] for f in self.FEATURE_ORDER]])
    
    def prepare_batch_input(self, features_list: List[Dict[str, float]]) -> np.ndarray:
        """
        Prepare batch of features for model input.
        
        Args:
            features_list: List of feature dictionaries
            
        Returns:
            Numpy array (n_samples, 17) for model input
        """
        return np.array([[f[feat] for feat in self.FEATURE_ORDER] for f in features_list])


# For backwards compatibility, create alias
FeatureEngineer = FeatureEngineerV2
