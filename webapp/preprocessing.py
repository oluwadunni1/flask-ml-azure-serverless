import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# ==========================================
# 1. CUSTOM FEATURE ENGINEERING CLASS
# ==========================================
class HousingFeatureEngineer(BaseEstimator, TransformerMixin):
    def __init__(self, current_year=2021):
        self.current_year = current_year
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        X_df = X.copy()
        # Ensure we don't crash if columns are missing during inference (defensive coding)
        if 'YearBuilt' in X_df.columns:
            X_df['HouseAge'] = self.current_year - X_df['YearBuilt']
            X_df = X_df.drop(columns=['YearBuilt'])
        else:
             # Fallback if YearBuilt is missing (though it should be there)
            X_df['HouseAge'] = 0 

        if 'Bedrooms' in X_df.columns:
            safe_bedrooms = X_df['Bedrooms'].clip(lower=1)
            if 'SquareFeet' in X_df.columns:
                X_df['RoomSize'] = X_df['SquareFeet'] / safe_bedrooms
            else:
                X_df['RoomSize'] = 0
        
        if 'SquareFeet' in X_df.columns and 'HouseAge' in X_df.columns:
            X_df['Size_Age_Interaction'] = X_df['SquareFeet'] * X_df['HouseAge']
            
        return X_df

# ==========================================
# 2. PIPELINE FACTORY
# ==========================================
def create_preprocessing_pipeline():
    CATEGORICAL_FEATURES = ['Neighborhood']
    # These features must match EXACTLY what HousingFeatureEngineer creates
    NUMERICAL_FEATURES = ['SquareFeet', 'Bedrooms', 'Bathrooms', 'HouseAge', 'RoomSize', 'Size_Age_Interaction']

    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), CATEGORICAL_FEATURES),
            ('num', StandardScaler(), NUMERICAL_FEATURES)
        ],
        remainder='drop'
    )
    
    pipeline = Pipeline(steps=[
        ('engineer', HousingFeatureEngineer()),
        ('preprocessor', preprocessor)
    ])
    
    return pipeline

if __name__ == "__main__":
    print("Unit test block loaded.")
