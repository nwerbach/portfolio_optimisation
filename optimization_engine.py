"""
Portfolio Optimization Engine
Core optimization logic using PuLP
"""

import pulp
import pandas as pd
import numpy as np
from datetime import datetime


class PortfolioOptimizer:
    def __init__(self):
        self.problem = None
        self.variables = []
        self.data = None
        
    def optimize(self, data, objective_column, direction="Maximize", custom_constraints=None):
        """
        Main optimization function
        
        Parameters:
        -----------
        data : DataFrame
            Portfolio data
        objective_column : str
            Column to optimize
        direction : str
            "Maximize" or "Minimize"
        custom_constraints : list
            List of constraint dicts with 'column', 'min', 'max' keys
            
        Returns:
        --------
        dict : Results containing summary and allocations
        """
        
        self.data = data.copy()
        custom_constraints = custom_constraints or []
        
        # Create optimization problem
        sense = pulp.LpMaximize if direction == "Maximize" else pulp.LpMinimize
        self.problem = pulp.LpProblem(f'Portfolio Optimization - {objective_column}', sense)
        
        # Create decision variables
        self._create_decision_variables()
        
        # Set objective function
        self._set_objective(objective_column)
        
        # Add constraints
        self._add_default_constraints()
        self._add_custom_constraints(custom_constraints)
        
        # Solve
        status = self.problem.solve(pulp.PULP_CBC_CMD(msg=0))
        
        if status != pulp.LpStatusOptimal:
            raise Exception(f"Optimization failed with status: {pulp.LpStatus[status]}")
        
        # Extract results
        results = self._extract_results(objective_column, direction)
        
        return results
    
    def _create_decision_variables(self):
        """Create decision variables for each row in data"""
        self.variables = []
        
        for idx, row in self.data.iterrows():
            var_name = f'x_{idx}'
            # Variables are continuous between 0 and 1 (represent allocation percentages)
            var = pulp.LpVariable(var_name, lowBound=0, upBound=1, cat='Continuous')
            self.variables.append(var)
    
    def _set_objective(self, objective_column):
        """Set the objective function"""
        if objective_column not in self.data.columns:
            raise ValueError(f"Column '{objective_column}' not found in data")
        
        objective = pulp.lpSum([
            self.data.iloc[i][objective_column] * self.variables[i]
            for i in range(len(self.data))
        ])
        
        self.problem += objective
    
    def _add_default_constraints(self):
        """Add default constraints"""
        # Total allocation constraint (sum to 1)
        self.problem += pulp.lpSum(self.variables) == 1, "Total_Allocation"
        
        # Optional: Add non-negativity (already handled in variable bounds)
    
    def _add_custom_constraints(self, custom_constraints):
        """Add user-defined constraints"""
        for i, constraint in enumerate(custom_constraints):
            constraint_type = constraint.get('type', 'numeric')
            
            if constraint_type == 'numeric':
                self._add_numeric_constraint(constraint, i)
            elif constraint_type == 'category':
                self._add_category_constraint(constraint, i)
    
    def _add_numeric_constraint(self, constraint, index):
        """Add a numeric constraint (original functionality)"""
        col = constraint['column']
        min_val = constraint['min']
        max_val = constraint['max']
        
        if col not in self.data.columns:
            return
        
        # Create constraint expression
        constraint_expr = pulp.lpSum([
            self.data.iloc[j][col] * self.variables[j]
            for j in range(len(self.data))
        ])
        
        # Add min constraint
        if min_val > 0:
            self.problem += constraint_expr >= min_val, f"Numeric_Min_{index}"
        
        # Add max constraint
        if max_val < float('inf'):
            self.problem += constraint_expr <= max_val, f"Numeric_Max_{index}"
    
    def _add_category_constraint(self, constraint, index):
        """Add a category-based constraint"""
        col = constraint['column']
        min_val = constraint['min']
        max_val = constraint['max']
        category_value = constraint.get('category_value')
        
        if col not in self.data.columns:
            return
        
        if category_value is not None:
            # Constraint applies to a specific category value
            mask = self.data[col] == category_value
            indices = self.data[mask].index.tolist()
            
            if not indices:
                return  # No assets in this category
            
            # Sum allocations for this specific category
            category_sum = pulp.lpSum([self.variables[i] for i in indices])
            
            # Add constraints
            if min_val > 0:
                self.problem += category_sum >= min_val, f"Category_{category_value}_Min_{index}"
            if max_val < float('inf'):
                self.problem += category_sum <= max_val, f"Category_{category_value}_Max_{index}"
                
        else:
            # Constraint applies to ALL categories (each category gets the same limit)
            unique_categories = self.data[col].unique()
            
            for category in unique_categories:
                mask = self.data[col] == category
                indices = self.data[mask].index.tolist()
                
                if not indices:
                    continue
                
                # Sum allocations for this category
                category_sum = pulp.lpSum([self.variables[i] for i in indices])
                
                # Apply the same min/max to each category
                if min_val > 0:
                    self.problem += category_sum >= min_val, f"AllCategories_{category}_Min_{index}"
                if max_val < float('inf'):
                    self.problem += category_sum <= max_val, f"AllCategories_{category}_Max_{index}"
    
    def _extract_results(self, objective_col, direction):
        """Extract and format results"""
        
        # Get allocations
        allocations = []
        for i, var in enumerate(self.variables):
            if var.varValue and var.varValue > 1e-6:  # Only include non-zero allocations
                row_data = self.data.iloc[i].to_dict()
                row_data['allocation'] = var.varValue
                allocations.append(row_data)
        
        allocations_df = pd.DataFrame(allocations)
        
        # Calculate summary statistics
        objective_value = pulp.value(self.problem.objective)
        total_allocation = sum([v.varValue for v in self.variables if v.varValue])
        
        summary = {
            'Objective Value': f"{objective_value:.6f}" if objective_value else "N/A",
            'Objective Type': f"{direction} {objective_col}",
            'Total Allocation': f"{total_allocation:.2%}",
            'Number of Assets': len(allocations),
            'Optimization Time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        results = {
            'summary': summary,
            'allocations': allocations_df,
            'total_allocation': total_allocation,
            'objective_value': objective_value
        }
        
        return results


class AdvancedPortfolioOptimizer(PortfolioOptimizer):
    """Extended optimizer with additional features"""
    
    def optimize_with_categories(self, data, objective_column, direction="Maximize", 
                                 category_column=None, category_limits=None, 
                                 custom_constraints=None):
        """
        Optimize with category-based constraints
        
        Parameters:
        -----------
        category_column : str
            Column name for categories
        category_limits : dict
            {category_name: max_allocation}
        """
        
        self.data = data.copy()
        custom_constraints = custom_constraints or []
        
        sense = pulp.LpMaximize if direction == "Maximize" else pulp.LpMinimize
        self.problem = pulp.LpProblem(f'Portfolio Optimization - {objective_column}', sense)
        
        self._create_decision_variables()
        self._set_objective(objective_column)
        self._add_default_constraints()
        
        # Add category constraints
        if category_column and category_limits:
            self._add_category_constraints(category_column, category_limits)
        
        self._add_custom_constraints(custom_constraints)
        
        status = self.problem.solve(pulp.PULP_CBC_CMD(msg=0))
        
        if status != pulp.LpStatusOptimal:
            raise Exception(f"Optimization failed with status: {pulp.LpStatus[status]}")
        
        results = self._extract_results(objective_column, direction)
        return results
    
    def _add_category_constraints(self, category_column, category_limits):
        """Add constraints for each category"""
        
        if category_column not in self.data.columns:
            return
        
        categories = self.data[category_column].unique()
        
        for category in categories:
            mask = self.data[category_column] == category
            indices = self.data[mask].index.tolist()
            
            category_sum = pulp.lpSum([self.variables[i] for i in indices])
            
            max_limit = category_limits.get(category, 1.0)
            self.problem += category_sum <= max_limit, f"Category_{category}"
