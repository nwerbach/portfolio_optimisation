"""
Data Handler Module
Handles data processing and validation
"""

import pandas as pd
import numpy as np
from typing import Tuple


class DataHandler:
    """Handle data loading, validation, and preprocessing"""
    
    @staticmethod
    def load_excel(file_path: str) -> pd.DataFrame:
        """Load Excel file"""
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            raise Exception(f"Failed to load Excel file: {str(e)}")
    
    @staticmethod
    def validate_data(df: pd.DataFrame) -> Tuple[bool, str]:
        """
        Validate data
        
        Returns:
        --------
        Tuple[bool, str] : (is_valid, error_message)
        """
        
        if df is None or df.empty:
            return False, "DataFrame is empty"
        
        if len(df) < 2:
            return False, "Need at least 2 rows of data"
        
        # Check for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            return False, "No numeric columns found for optimization"
        
        return True, "Data is valid"
    
    @staticmethod
    def get_numeric_columns(df: pd.DataFrame) -> list:
        """Get numeric columns for objective selection"""
        return df.select_dtypes(include=[np.number]).columns.tolist()
    
    @staticmethod
    def get_categorical_columns(df: pd.DataFrame) -> list:
        """Get categorical columns for constraints"""
        return df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    @staticmethod
    def normalize_data(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
        """Normalize numeric columns to 0-1 range"""
        df_copy = df.copy()
        
        if columns is None:
            columns = DataHandler.get_numeric_columns(df)
        
        for col in columns:
            if col not in df_copy.columns:
                continue
            
            min_val = df_copy[col].min()
            max_val = df_copy[col].max()
            
            if max_val - min_val != 0:
                df_copy[col] = (df_copy[col] - min_val) / (max_val - min_val)
        
        return df_copy
    
    @staticmethod
    def handle_missing_values(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """
        Handle missing values
        
        Parameters:
        -----------
        strategy : str
            'mean', 'median', 'drop', or 'forward_fill'
        """
        
        df_copy = df.copy()
        
        if strategy == 'mean':
            df_copy = df_copy.fillna(df_copy.mean())
        elif strategy == 'median':
            df_copy = df_copy.fillna(df_copy.median())
        elif strategy == 'drop':
            df_copy = df_copy.dropna()
        elif strategy == 'forward_fill':
            df_copy = df_copy.fillna(method='ffill')
        
        return df_copy
    
    @staticmethod
    def get_data_summary(df: pd.DataFrame) -> dict:
        """Get summary statistics of data"""
        summary = {
            'rows': len(df),
            'columns': len(df.columns),
            'numeric_cols': len(DataHandler.get_numeric_columns(df)),
            'categorical_cols': len(DataHandler.get_categorical_columns(df)),
            'missing_values': df.isnull().sum().sum()
        }
        
        return summary


class ConstraintBuilder:
    """Build and validate constraints"""
    
    @staticmethod
    def create_constraint(column: str, min_val: float, max_val: float, 
                         constraint_type: str = "numeric", 
                         category_value: str = None) -> dict:
        """Create a constraint dictionary
        
        Parameters:
        -----------
        column : str
            Column name to constrain
        min_val : float
            Minimum value
        max_val : float
            Maximum value
        constraint_type : str
            "numeric" for numeric constraints, "category" for categorical
        category_value : str, optional
            Specific category value to constrain (if constraint_type="category")
        """
        
        if min_val > max_val:
            raise ValueError(f"Min value ({min_val}) cannot exceed max value ({max_val})")
        
        constraint = {
            'column': column,
            'min': min_val,
            'max': max_val,
            'type': constraint_type,
            'category_value': category_value
        }
        
        return constraint
    
    @staticmethod
    def create_category_constraint(column: str, category_value: str = None, 
                                 min_val: float = 0, max_val: float = 1.0) -> dict:
        """Create a category-based constraint
        
        Parameters:
        -----------
        column : str
            Categorical column name (e.g., 'Sector')
        category_value : str, optional
            Specific category value (e.g., 'Finance'). If None, applies to all categories
        min_val : float
            Minimum total allocation for the category
        max_val : float
            Maximum total allocation for the category
        """
        
        return {
            'column': column,
            'min': min_val,
            'max': max_val,
            'type': 'category',
            'category_value': category_value
        }
    
    @staticmethod
    def validate_constraint(constraint: dict, df: pd.DataFrame) -> Tuple[bool, str]:
        """Validate constraint against data"""
        
        col = constraint.get('column')
        constraint_type = constraint.get('type', 'numeric')
        
        if col not in df.columns:
            return False, f"Column '{col}' not found in data"
        
        if constraint_type == 'numeric':
            if not pd.api.types.is_numeric_dtype(df[col]):
                return False, f"Column '{col}' is not numeric for numeric constraint"
        elif constraint_type == 'category':
            # For category constraints, we need to check if the column exists
            # The actual validation happens in the optimization engine
            pass
        else:
            return False, f"Unknown constraint type: {constraint_type}"
        
        # Check min/max values
        min_val = constraint.get('min', 0)
        max_val = constraint.get('max', float('inf'))
        
        if min_val > max_val:
            return False, f"Min value ({min_val}) cannot exceed max value ({max_val})"
        
        # For category constraints with specific values, check if the value exists
        if constraint_type == 'category' and constraint.get('category_value'):
            category_value = constraint['category_value']
            if category_value not in df[col].unique():
                return False, f"Category value '{category_value}' not found in column '{col}'"
        
        return True, "Constraint is valid"
    
    @staticmethod
    def get_available_categories(df: pd.DataFrame, column: str) -> list:
        """Get unique values from a categorical column"""
        if column not in df.columns:
            return []
        return sorted(df[column].unique().tolist())


class ResultsFormatter:
    """Format and export results"""
    
    @staticmethod
    def format_results_table(results_df: pd.DataFrame) -> pd.DataFrame:
        """Format results table for display"""
        
        df = results_df.copy()
        
        # Format numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if 'allocation' in col.lower():
                df[col] = df[col].apply(lambda x: f"{x:.2%}" if x > 0 else "0%")
            else:
                df[col] = df[col].apply(lambda x: f"{x:.6f}")
        
        return df
    
    @staticmethod
    def export_to_excel(results_df: pd.DataFrame, file_path: str, 
                       summary_dict: dict = None) -> bool:
        """Export results to Excel"""
        
        try:
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                # Write allocations
                results_df.to_excel(writer, sheet_name='Allocations', index=False)
                
                # Write summary if provided
                if summary_dict:
                    summary_df = pd.DataFrame(list(summary_dict.items()), 
                                            columns=['Metric', 'Value'])
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            return True
        except Exception as e:
            raise Exception(f"Failed to export results: {str(e)}")
    
    @staticmethod
    def create_summary_report(summary_dict: dict, constraints: list = None) -> str:
        """Create text summary report"""
        
        report = "=" * 50 + "\n"
        report += "PORTFOLIO OPTIMIZATION REPORT\n"
        report += "=" * 50 + "\n\n"
        
        for key, value in summary_dict.items():
            report += f"{key}: {value}\n"
        
        if constraints:
            report += "\n" + "-" * 50 + "\n"
            report += "CONSTRAINTS APPLIED:\n"
            report += "-" * 50 + "\n"
            
            for i, constraint in enumerate(constraints, 1):
                col = constraint.get('column', 'Unknown')
                min_val = constraint.get('min', 'N/A')
                max_val = constraint.get('max', 'N/A')
                report += f"{i}. {col}: [{min_val}, {max_val}]\n"
        
        return report
