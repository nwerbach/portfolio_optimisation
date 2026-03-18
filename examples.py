"""
Quick Start Examples - Portfolio Optimizer
Shows various ways to use the optimization engine
"""

import pandas as pd
import numpy as np
from optimization_engine import PortfolioOptimizer, AdvancedPortfolioOptimizer
from data_handler import DataHandler, ConstraintBuilder, ResultsFormatter
import os


def example_1_basic_optimization():
    """Example 1: Basic optimization with sample data"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Optimization")
    print("="*60)
    
    # Create sample data
    data = pd.DataFrame({
        'ID': range(1, 6),
        'Asset': ['Bond A', 'Bond B', 'Bond C', 'Bond D', 'Bond E'],
        'Spread': [0.045, 0.052, 0.038, 0.048, 0.055],
        'Duration': [5.2, 4.8, 6.1, 5.5, 4.2],
        'Rating': [9, 8, 7, 8, 9],  # Higher is better
    })
    
    print("\nInput Data:")
    print(data)
    
    # Create optimizer
    optimizer = PortfolioOptimizer()
    
    # Run optimization - maximize spread
    results = optimizer.optimize(
        data=data,
        objective_column='Spread',
        direction='Maximize'
    )
    
    print("\nOptimization Results:")
    print(results['summary'])
    print("\nAllocations:")
    print(results['allocations'][['Asset', 'Spread', 'allocation']])


def example_2_with_constraints():
    """Example 2: Optimization with constraints"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Optimization with Constraints")
    print("="*60)
    
    # Create sample data
    data = pd.DataFrame({
        'ID': range(1, 11),
        'Asset': [f'Asset_{i}' for i in range(1, 11)],
        'Return': np.random.uniform(0.03, 0.08, 10),
        'Risk': np.random.uniform(0.05, 0.15, 10),
        'Duration': np.random.uniform(3, 8, 10),
    })
    
    print("\nInput Data:")
    print(data)
    
    # Define constraints
    constraints = [
        {'column': 'Duration', 'min': 4.0, 'max': 6.0},
        {'column': 'Risk', 'min': 0, 'max': 0.10}
    ]
    
    print("\nConstraints:")
    for c in constraints:
        print(f"  {c['column']}: [{c['min']}, {c['max']}]")
    
    optimizer = PortfolioOptimizer()
    results = optimizer.optimize(
        data=data,
        objective_column='Return',
        direction='Maximize',
        custom_constraints=constraints
    )
    
    print("\nOptimization Results:")
    print(results['summary'])
    print("\nTop Allocations:")
    top = results['allocations'].nlargest(5, 'allocation')
    print(top[['Asset', 'Return', 'Duration', 'Risk', 'allocation']])


def example_3_category_constraints():
    """Example 3: Using category-based constraints"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Category-Based Constraints")
    print("="*60)
    
    # Create sample data with sectors
    data = pd.DataFrame({
        'ID': range(1, 11),
        'Asset': [f'Asset_{i}' for i in range(1, 11)],
        'Sector': ['Finance', 'Finance', 'Finance', 'Finance', 'Energy',
                   'Energy', 'Energy', 'Tech', 'Tech', 'Utilities'],
        'Return': np.random.uniform(0.03, 0.08, 10),
    })
    
    print("\nInput Data:")
    print(data)
    
    # Create category constraints (max 40% per sector)
    category_limits = {
        'Finance': 0.40,
        'Energy': 0.30,
        'Tech': 0.30,
        'Utilities': 0.20
    }
    
    print("\nCategory Limits:")
    for sector, limit in category_limits.items():
        print(f"  {sector}: max {limit:.0%}")
    
    optimizer = AdvancedPortfolioOptimizer()
    results = optimizer.optimize_with_categories(
        data=data,
        objective_column='Return',
        direction='Maximize',
        category_column='Sector',
        category_limits=category_limits
    )
    
    print("\nResults Summary:")
    print(results['summary'])
    print("\nAllocations by Sector:")
    allocations = results['allocations'].sort_values('allocation', ascending=False)
    for sector in category_limits.keys():
        sector_alloc = allocations[allocations['Sector'] == sector]['allocation'].sum()
        print(f"  {sector}: {sector_alloc:.2%}")


def example_4_data_handler():
    """Example 4: Using DataHandler utilities"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Data Handler Utilities")
    print("="*60)
    
    # Create sample data with missing values
    data = pd.DataFrame({
        'ID': range(1, 6),
        'Name': ['Asset A', 'Asset B', 'Asset C', 'Asset D', 'Asset E'],
        'Value': [100, np.nan, 110, 105, 95],
        'Score': [8, 9, 7, np.nan, 8],
        'Category': ['A', 'B', 'A', 'B', 'A']
    })
    
    print("\nOriginal Data:")
    print(data)
    print(f"\nMissing Values: {data.isnull().sum().sum()}")
    
    # Get data summary
    handler = DataHandler()
    summary = handler.get_data_summary(data)
    
    print("\nData Summary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    # Get numeric and categorical columns
    numeric_cols = handler.get_numeric_columns(data)
    category_cols = handler.get_categorical_columns(data)
    
    print(f"\nNumeric Columns: {numeric_cols}")
    print(f"Categorical Columns: {category_cols}")
    
    # Handle missing values
    data_filled = handler.handle_missing_values(data, strategy='mean')
    
    print("\nData After Filling Missing Values:")
    print(data_filled)
    
    # Normalize numeric columns
    data_normalized = handler.normalize_data(data_filled)
    
    print("\nNormalized Data (0-1 range):")
    print(data_normalized)


def example_5_export_results():
    """Example 5: Exporting results"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Exporting Results")
    print("="*60)
    
    # Create sample data and optimize
    data = pd.DataFrame({
        'ID': range(1, 6),
        'Asset': ['Bond A', 'Bond B', 'Bond C', 'Bond D', 'Bond E'],
        'Spread': [0.045, 0.052, 0.038, 0.048, 0.055],
        'Duration': [5.2, 4.8, 6.1, 5.5, 4.2],
    })
    
    optimizer = PortfolioOptimizer()
    results = optimizer.optimize(
        data=data,
        objective_column='Spread',
        direction='Maximize'
    )
    
    # Export to Excel
    output_file = 'portfolio_results_example.xlsx'
    
    try:
        formatter = ResultsFormatter()
        formatter.export_to_excel(
            results['allocations'],
            output_file,
            results['summary']
        )
        print(f"✓ Results exported to: {output_file}")
        
        # Read back the file to verify
        df_check = pd.read_excel(output_file, sheet_name='Allocations')
        print(f"\nExported data verification:")
        print(df_check)
        
    except Exception as e:
        print(f"✗ Export failed: {e}")


def example_6_generate_report():
    """Example 6: Generate text report"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Generate Report")
    print("="*60)
    
    # Create sample data and optimize
    data = pd.DataFrame({
        'ID': range(1, 6),
        'Asset': ['Bond A', 'Bond B', 'Bond C', 'Bond D', 'Bond E'],
        'Spread': [0.045, 0.052, 0.038, 0.048, 0.055],
    })
    
    constraints = [
        {'column': 'Spread', 'min': 0.04, 'max': 0.06}
    ]
    
    optimizer = PortfolioOptimizer()
    results = optimizer.optimize(
        data=data,
        objective_column='Spread',
        direction='Maximize',
        custom_constraints=constraints
    )
    
    # Generate report
    formatter = ResultsFormatter()
    report = formatter.create_summary_report(results['summary'], constraints)
    
    print(report)
    
    # Save report to file
    with open('portfolio_report_example.txt', 'w') as f:
        f.write(report)
    print("\n✓ Report saved to: portfolio_report_example.txt")


def run_all_examples():
    """Run all examples"""
    print("\n" + "#"*60)
    print("# PORTFOLIO OPTIMIZER - QUICK START EXAMPLES")
    print("#"*60)
    
    try:
        example_1_basic_optimization()
    except Exception as e:
        print(f"Example 1 error: {e}")
    
    try:
        example_2_with_constraints()
    except Exception as e:
        print(f"Example 2 error: {e}")
    
    try:
        example_3_category_constraints()
    except Exception as e:
        print(f"Example 3 error: {e}")
    
    try:
        example_4_data_handler()
    except Exception as e:
        print(f"Example 4 error: {e}")
    
    try:
        example_5_export_results()
    except Exception as e:
        print(f"Example 5 error: {e}")
    
    try:
        example_6_generate_report()
    except Exception as e:
        print(f"Example 6 error: {e}")
    
    print("\n" + "#"*60)
    print("# ALL EXAMPLES COMPLETED")
    print("#"*60)


if __name__ == "__main__":
    run_all_examples()
