# Portfolio Optimizer Pro - Complete Application

A professional portfolio optimization application with an intuitive GUI that uses linear programming (PuLP) to find optimal asset allocations.

## Features

### 🎯 Core Optimization
- **Flexible Objectives**: Optimize for any metric in your data (spread, return, yield, etc.)
- **Direction Control**: Maximize or minimize your chosen objective
- **Linear Programming**: Uses industry-standard PuLP solver (CBC)
- **Custom Constraints**: Add unlimited linear constraints for portfolio control

### 📊 Data Management
- **Excel Support**: Load .xlsx files directly into the app
- **Data Preview**: View column statistics and data types
- **Validation**: Automatic data validation and error handling
- **Missing Value Handling**: Handles missing values gracefully

### 🔧 Advanced Features
- **Category-Based Constraints**: Limit allocations by category (sector, rating, etc.)
- **Interactive Constraints**: Add/remove constraints in real-time
- **Results Analysis**: Comprehensive analysis of optimization results
- **Export Functionality**: Save results to Excel with summary statistics

### 📈 Results & Reporting
- **Summary Statistics**: Objective value, total allocation, number of assets
- **Detailed Allocations**: See exactly which assets to select and how much
- **Analysis Reports**: Insights into portfolio composition
- **Easy Export**: Export to Excel for further analysis

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or Download the Repository**
   ```bash
   cd d:\Python\portfolio_optimisation
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or manually install:
   ```bash
   pip install pulp pandas openpyxl numpy
   ```

## Usage

### Quick Start

1. **Run the Application**
   ```bash
   python portfolio_optimizer_advanced.py
   ```

2. **Load Data**
   - Click "📊 Data" tab
   - Click "📁 Select Excel File"
   - Choose your .xlsx file

3. **Configure Optimization**
   - Go to "⚙️ Optimization" tab
   - Select column to optimize
   - Choose Maximize or Minimize
   - (Optional) Add constraints

4. **Run Optimization**
   - Click "▶ Run Optimization"
   - Wait for optimization to complete
   - View results in "📈 Results" tab

5. **Export Results**
   - Click "💾 Export to Excel"
   - Choose save location
   - Results saved with summary statistics

## Quick Launch

To run the basic GUI version:
```bash
python portfolio_optimizer.py
```

To run the advanced version (recommended):
```bash
python portfolio_optimizer_advanced.py
```

## File Structure

```
portfolio_optimisation/
├── portfolio_optimizer.py              # Basic GUI version
├── portfolio_optimizer_advanced.py     # Feature-rich GUI version (RECOMMENDED)
├── optimization_engine.py              # Core optimization logic
├── data_handler.py                     # Data processing utilities
├── requirements.txt                    # Python dependencies
├── README.md                          # Documentation
└── LP_pulp_optmize.py                 # Original reference implementation
```

## Data Format

Your Excel file should have one row per asset and columns for various metrics:

Example structure:
```
ID | Ticker | Spread | Duration | Sector   | Rating
---|--------|--------|----------|----------|--------
1  | BOND1  | 0.045  | 5.2      | Finance  | AAA
2  | BOND2  | 0.052  | 4.8      | Finance  | AA
3  | BOND3  | 0.038  | 6.1      | Energy   | BBB
```

## Adding Constraints

Constraints control portfolio composition. Examples:

1. **Column Value Limit**
   - Min: 0, Max: value (controls average/total of that metric)

2. **Sector Maximum**: Cap allocation to specific sectors

3. **Rating Quality**: Ensure minimum average rating

4. **Duration Control**: Portfolio duration range

## API Usage

### Using the Optimization Engine

```python
from optimization_engine import PortfolioOptimizer
import pandas as pd

# Load your data
data = pd.read_excel('portfolio_data.xlsx')

# Create optimizer
optimizer = PortfolioOptimizer()

# Define constraints
constraints = [
    {'column': 'spread', 'min': 0.03, 'max': 0.08},
    {'column': 'duration', 'min': 4.0, 'max': 6.0}
]

# Run optimization
results = optimizer.optimize(
    data=data,
    objective_column='spread',
    direction='Maximize',
    custom_constraints=constraints
)

# Access results
print(results['summary'])
print(results['allocations'])
```

## Troubleshooting

### "Optimization failed with status: Infeasible"
- Constraints are too restrictive
- Check min values aren't > max values
- Verify constraints exclude all assets

### "Column not found"
- Ensure column name matches Excel header exactly (case-sensitive)

### Solver errors
- Ensure PuLP is installed: `pip install pulp`
- CBC solver comes bundled with PuLP

## Technical Details

- **Solver**: CBC (Coin-or-branch and cut)
- **Optimization**: Linear Programming via PuLP
- **Allocations**: All assets sum to 100%
- **Data Format**: XLSX (Excel 2007+)
- **Python Version**: 3.7+

## Original Implementation

This application builds upon the original `LP_pulp_optmize.py` which provided:
- Bond portfolio optimization
- Fixed constraints for ratings
- Duration and score constraints
- Sector/country diversification

The new GUI generalizes this to support any portfolio optimization scenario.

---

**Version**: 2.0  
**Last Updated**: 2026  
**Optimization Engine**: PuLP with CBC solver
