"""
Feature engineering for the priority scoring model.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional

from utils.constants import MAX_GPA, MIN_GPA, ALLOCATION_CONSTRAINTS, PRIORITY_WEIGHTS


class FeatureEngineer:
    """
    Feature engineering for student housing priority scoring.
    """
    
    def __init__(self):
        self.max_distance = ALLOCATION_CONSTRAINTS['max_distance_cap']
    
    def normalize_gpa(self, gpa: Optional[float]) -> float:
        """
        Normalize GPA to 0-1 range.
        
        Args:
            gpa: Raw GPA value (0.0 - 5.0)
        
        Returns:
            Normalized GPA (0.0 - 1.0)
        """
        if gpa is None or gpa < MIN_GPA:
            return 0.0
        
        normalized = (gpa - MIN_GPA) / (MAX_GPA - MIN_GPA)
        return max(0.0, min(1.0, normalized))
    
    def encode_level(self, level: int) -> int:
        """
        Encode academic level.
        
        Args:
            level: Academic level (100, 200, 300, 400, 500)
        
        Returns:
            Encoded level (1, 2, 3, 4, 5)
        """
        level_map = {100: 1, 200: 2, 300: 3, 400: 4, 500: 5}
        return level_map.get(level, 1)
    
    def transform_distance(self, distance: Optional[float]) -> float:
        """
        Transform distance using log scale and cap at max.
        
        Args:
            distance: Distance in kilometers
        
        Returns:
            Transformed distance score (0-1, higher for longer distances)
        """
        if distance is None or distance < 0:
            return 0.0
        
        # Cap at max distance
        capped_distance = min(distance, self.max_distance)
        
        # Normalize to 0-1
        normalized = capped_distance / self.max_distance
        
        return normalized
    
    def encode_binary(self, value: bool) -> int:
        """
        Encode boolean to binary.
        
        Args:
            value: Boolean value
        
        Returns:
            1 if True, 0 if False
        """
        return 1 if value else 0
    
    def calculate_seniority_score(self, level: int, gpa: Optional[float]) -> float:
        """
        Calculate seniority score based on level and GPA.
        
        Args:
            level: Academic level
            gpa: Current GPA
        
        Returns:
            Seniority score
        """
        level_encoded = self.encode_level(level)
        gpa_normalized = self.normalize_gpa(gpa) if gpa else 0.0
        
        return level_encoded * (1 + gpa_normalized)
    
    def extract_features(self, student_profile) -> Dict[str, float]:
        """
        Extract features from student profile.
        
        Args:
            student_profile: StudentProfile model instance
        
        Returns:
            Dictionary of extracted features
        """
        features = {
            'gpa_normalized': self.normalize_gpa(student_profile.current_gpa),
            'level_encoded': self.encode_level(student_profile.level),
            'distance_transformed': self.transform_distance(student_profile.distance_from_campus),
            'disability_flag': self.encode_binary(student_profile.disability_status),
            'financial_aid_flag': self.encode_binary(student_profile.financial_aid_status),
            'seniority_score': self.calculate_seniority_score(
                student_profile.level,
                student_profile.current_gpa
            ),
        }
        
        return features
    
    def extract_features_from_dict(self, data: Dict) -> Dict[str, float]:
        """
        Extract features from dictionary.
        
        Args:
            data: Dictionary containing student data
        
        Returns:
            Dictionary of extracted features
        """
        features = {
            'gpa_normalized': self.normalize_gpa(data.get('gpa')),
            'level_encoded': self.encode_level(data.get('level', 100)),
            'distance_transformed': self.transform_distance(data.get('distance')),
            'disability_flag': self.encode_binary(data.get('disability', False)),
            'financial_aid_flag': self.encode_binary(data.get('financial_aid', False)),
            'seniority_score': self.calculate_seniority_score(
                data.get('level', 100),
                data.get('gpa')
            ),
        }
        
        return features
    
    def prepare_model_input(self, features: Dict[str, float]) -> np.ndarray:
        """
        Prepare features for model input.
        
        Args:
            features: Dictionary of features
        
        Returns:
            Numpy array for model input
        """
        # Order matters - must match training order
        feature_order = [
            'gpa_normalized',
            'level_encoded',
            'distance_transformed',
            'disability_flag',
            'financial_aid_flag',
        ]
        
        return np.array([[features[f] for f in feature_order]])
    
    def create_feature_dataframe(self, students_data: List[Dict]) -> pd.DataFrame:
        """
        Create a DataFrame from multiple student records.
        
        Args:
            students_data: List of student data dictionaries
        
        Returns:
            Pandas DataFrame with features
        """
        features_list = []
        
        for data in students_data:
            features = self.extract_features_from_dict(data)
            features['student_id'] = data.get('id')
            features_list.append(features)
        
        df = pd.DataFrame(features_list)
        
        return df


def generate_synthetic_priority_score(features: Dict[str, float]) -> float:
    """
    Generate a synthetic priority score based on domain knowledge.
    Used for training data generation.
    
    Formula:
    - 40% GPA
    - 30% Distance (capped)
    - 20% Level (seniority)
    - 10% Need-based (disability + financial aid)
    
    Args:
        features: Dictionary of features
    
    Returns:
        Priority score (0-100)
    """
    gpa_score = features['gpa_normalized'] * PRIORITY_WEIGHTS['gpa'] * 100
    
    distance_score = features['distance_transformed'] * PRIORITY_WEIGHTS['distance'] * 100
    
    level_score = (features['level_encoded'] / 5) * PRIORITY_WEIGHTS['level'] * 100
    
    need_score = (
        (features['disability_flag'] + features['financial_aid_flag']) > 0
    ) * PRIORITY_WEIGHTS['need_based'] * 100
    
    total_score = gpa_score + distance_score + level_score + need_score
    
    # Clamp to valid range
    return max(0.0, min(100.0, total_score))
