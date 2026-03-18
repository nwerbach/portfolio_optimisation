# Getting Started - Portfolio Optimizer Pro

Welcome to Portfolio Optimizer Pro! This guide will walk you through installation and your first optimization.

## System Requirements

- **Python**: 3.7 or higher
- **OS**: Windows, macOS, or Linux
- **RAM**: 2GB minimum (4GB+ recommended)
- **Disk**: 500MB free space

## Installation - 5 Minutes

### Step 1: Install Python

If you don't have Python installed:
1. Visit https://www.python.org/downloads/
2. Download Python 3.10 or higher
3. Run the installer
4. **IMPORTANT**: Check "Add Python to PATH"
5. Click "Install Now"

### Step 2: Install Dependencies

Open a terminal/command prompt and navigate to the portfolio_optimisation folder:

```bash
cd d:\Python\portfolio_optimisation
```

Install the required packages:

```bash
pip install -r requirements.txt
```

This installs:
- `pulp` - Linear programming solver
- `pandas` - Data handling
- `openpyxl` - Excel file support
- `numpy` - Numerical computations

### Step 3: Verify Installation

Test that everything works:

```bash
python -c "import pulp, pandas, openpyxl; print('✓ All packages installed')"
```

## First Run - 10 Minutes

### Option A: Using the GUI (Recommended)

**On Windows:**
- Double-click `launch.bat`
- OR run in command prompt: `python portfolio_optimizer_advanced.py`

**On Mac/Linux:**
```bash
python launch.py
```

Or directly:
```bash
python portfolio_optimizer_advanced.py
```

### Option B: Generate Sample Data First

Before running, generate sample data to test with:

```bash
python generate_sample_data.py
```

This creates a `sample_data/` folder with example portfolios:
- `sample_bonds.xlsx` - Bond portfolio
- `sample_stocks.xlsx` - Stock portfolio
- `sample_mixed.xlsx` - Mixed asset classes
- `sample_crypto.xlsx` - Cryptocurrency portfolio

## Using the Application

### Main Steps

1. **Load Data**
   - Click the "📊 Data" tab
   - Click "📁 Select Excel File"
   - Choose your .xlsx file
   - View statistics and preview

2. **Configure Optimization**
   - Go to "⚙️ Optimization" tab
   - Select a numeric column as your objective (what to optimize)
   - Choose "Maximize" or "Minimize"
   - (Optional) Add constraints to control the portfolio

3. **Add Constraints** (Optional)
   - Select a column
   - Set minimum and maximum values
   - Click "Add Constraint"
   - Repeat for multiple constraints

4. **Run Optimization**
   - Click "▶ Run Optimization"
   - Wait for completion (usually 1-10 seconds)
   - Results appear automatically

5. **View Results**
   - Go to "📈 Results" tab
   - See allocation percentages
   - View analysis in "🔍 Analysis" tab

6. **Export Results**
   - Click "💾 Export to Excel"
   - Choose where to save
   - File includes allocations and summary

## Data Format

Your Excel file should look like this:

```
| ID  | Asset  | Return | Risk  | Sector   |
|-----|--------|--------|-------|----------|
| 1   | Asset1 | 0.08   | 0.15  | Tech     |
| 2   | Asset2 | 0.06   | 0.12  | Finance  |
| 3   | Asset3 | 0.07   | 0.13  | Energy   |
| ... | ...    | ...    | ...   | ...      |
```

Requirements:
- One row per asset
- At least one numeric column (for optimization)
- No required column names (your headers will work)
- Can include text columns (Ticker, Sector, etc.)

## Examples & Tutorials

### Example 1: Maximize Returns with Risk Control

```
Data: sample_stocks.xlsx

Optimization:
  Objective: Expected_Return
  Type: Maximize

Constraints:
  Column: Volatility, Min: 0, Max: 0.25
  Column: Beta, Min: 0, Max: 1.5
```

**Result**: Portfolio maximizing returns while controlling risk

### Example 2: Bond Portfolio with Duration Target

```
Data: sample_bonds.xlsx

Optimization:
  Objective: Spread
  Type: Maximize

Constraints:
  Column: Duration, Min: 4.0, Max: 6.0
```

**Result**: Highest spread portfolio with 4-6 year duration

### Example 3: Sector Diversification

For sector diversification, you need to create a helper column showing sector weights in your Excel file. See Advanced Usage below.

### Example 4: Mixed Asset Portfolio

```
Data: sample_mixed.xlsx

Optimization:
  Objective: Expected_Return
  Type: Maximize

Constraints:
  Column: Risk, Min: 0, Max: 0.20
  Column: Duration, Min: 2, Max: 12
```

**Result**: Multi-asset portfolio optimized for return with controlled risk

## Troubleshooting

### "Python is not recognized"

**Solution**: Add Python to PATH
- Windows: Reinstall Python and check "Add Python to PATH"
- Mac/Linux: Check that Python is in your PATH variable

```bash
# Check Python installation
python --version
```

### "No module named 'pulp'"

**Solution**: Reinstall dependencies
```bash
pip install --upgrade pulp pandas openpyxl numpy
```

### "Excel file not found"

**Solution**: 
- Use absolute path or place file in the working directory
- Check file is actually .xlsx (not .xls)

### "Optimization failed - Infeasible"

**Causes & Solutions**:
- Constraints are too restrictive → Relax constraint ranges
- Min value > max value → Check your values
- Not enough quality assets → Use fewer/easier constraints

### GUI window won't open

**Solution**:
```bash
# Try running with explicit module
python -m tkinter  # Check tkinter works

# If tkinter missing, install it
# Ubuntu/Debian: sudo apt-get install python3-tk
# Fed ora/CentOS: sudo dnf install python3-tkinter
# macOS: usually included with Python
```

## Advanced Usage

### Using the Library in Your Own Code

```python
from optimization_engine import PortfolioOptimizer
import pandas as pd

# Load data
data = pd.read_excel('my_portfolio.xlsx')

# Create optimizer
optimizer = PortfolioOptimizer()

# Run optimization
results = optimizer.optimize(
    data=data,
    objective_column='Return',
    direction='Maximize',
    custom_constraints=[
        {'column': 'Risk', 'min': 0, 'max': 0.15},
        {'column': 'Duration', 'min': 3, 'max': 7}
    ]
)

# Access results
print(results['summary'])
print(results['allocations'])

# Export
results['allocations'].to_excel('results.xlsx', index=False)
```

### Creating Custom Constraints

```python
# Constraint format
{
    'column': 'ColumnName',    # Column in your data
    'min': 0.0,                # Minimum value
    'max': 0.50                # Maximum value
}
```

Multiple constraints are applied simultaneously. All must be satisfied.

## Configuration

Edit `config.py` to customize:
- Solver settings
- UI theme and colors
- Default constraints
- Export options

## Performance Tips

1. **Faster optimization**:
   - Keep dataset under 1000 assets
   - Fewer constraints = faster solving
   - Use simpler data types (numbers instead of text)

2. **Better results**:
   - Start with one constraint and add gradually
   - Check results are realistic before using
   - Use multiple optimization runs with different parameters

## Files Explained

| File | Purpose |
|------|---------|
| `portfolio_optimizer_advanced.py` | Main GUI application |
| `optimization_engine.py` | Core optimization logic |
| `data_handler.py` | Data validation & processing |
| `config.py` | Configuration settings |
| `generate_sample_data.py` | Creates sample datasets |
| `examples.py` | Usage examples |
| `launch.bat` / `launch.py` | Application launcher |

## Next Steps

1. **Run with sample data**: `python generate_sample_data.py` → launch app → load sample
2. **Try your own data**: Prepare Excel file → launch app → load your data
3. **Explore examples**: Run `python examples.py` to see code examples
4. **Customize**: Edit `config.py` for your preferences

## Getting Help

**Check the README.md** for detailed documentation

**Review examples.py** for code examples

**Test with sample data** to learn the workflow

## Common Questions

**Q: Can I optimize multiple objectives?**
A: Not simultaneously, but you can run multiple optimizations and compare results.

**Q: What's the maximum portfolio size?**
A: Typically 1000+ assets, depending on constraints complexity.

**Q: Can I import from CSV?**
A: Yes, convert CSV to Excel first using pandas or Excel itself.

**Q: Is my data secure?**
A: All processing is local. No data is sent anywhere.

**Q: Can I run this on a server?**
A: Yes, remove the GUI component and use just `optimization_engine.py`.

---

**Ready to optimize?** Launch the app with:
```bash
python portfolio_optimizer_advanced.py
```

Good luck! 🚀
