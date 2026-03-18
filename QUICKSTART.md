# Portfolio Optimizer Pro - Installation & Quick Start Checklist

## ✅ Installation Checklist (5 minutes)

- [ ] **Step 1**: Open Command Prompt/Terminal
- [ ] **Step 2**: Navigate to portfolio folder: `cd d:\Python\portfolio_optimisation`
- [ ] **Step 3**: Install dependencies: `pip install -r requirements.txt`
- [ ] **Step 4**: Verify installation: `python -c "import pulp, pandas, openpyxl; print('✓ Success')"`

## 🚀 Quick Start (Choose One)

### Option A: Try with Sample Data (Easiest!) ⭐

```bash
# Step 1: Generate sample data
python generate_sample_data.py

# Step 2: Launch the app
python portfolio_optimizer_advanced.py

# Step 3: In the app
# - Click "📊 Data" tab
# - Click "📁 Select Excel File"
# - Choose file from sample_data/ folder
# - Go to "⚙️ Optimization" and select column to optimize
# - Click "▶ Run Optimization"
# - View results in "📈 Results" tab
```

### Option B: Use Your Own Data

```bash
# Step 1: Prepare your Excel file (.xlsx format)
# Rows = assets, Columns = metrics (any names work)

# Step 2: Launch the app
python portfolio_optimizer_advanced.py

# Step 3: In the app
# - Load your Excel file
# - Configure optimization
# - Add constraints (optional)
# - Run and view results
```

### Option C: Windows Users - Just Click!

```bash
# Simply double-click this file:
launch.bat

# It will:
# 1. Check Python installation
# 2. Install dependencies if needed
# 3. Launch the app automatically
```

## 📋 Files Checklist

### Core Application Files
- [x] `portfolio_optimizer_advanced.py` - Main GUI application (recommended)
- [x] `portfolio_optimizer.py` - Basic GUI version
- [x] `optimization_engine.py` - Core optimization logic
- [x] `data_handler.py` - Data utilities and validation
- [x] `config.py` - Configuration settings

### Launcher Scripts
- [x] `launch.py` - Cross-platform Python launcher
- [x] `launch.bat` - Windows batch launcher
- [x] `launch.sh` - Unix/Linux launcher

### Data & Examples
- [x] `generate_sample_data.py` - Create sample portfolios
- [x] `examples.py` - Code examples and usage patterns
- [x] `requirements.txt` - Python dependencies

### Documentation
- [x] `README.md` - Full documentation
- [x] `GETTING_STARTED.md` - Step-by-step guide
- [x] `PROJECT_SUMMARY.md` - What was built

## 🎯 What Each Application Does

### portfolio_optimizer_advanced.py (⭐ Recommended)
**For**: Professional use, full features
**Features**: 
- 5 tabbed interface (Data, Optimization, Results, Analysis, Help)
- Data statistics and preview
- Interactive constraint management
- Detailed analysis reports
- Easy export

**When to use**: Always! This is the best version

### portfolio_optimizer.py
**For**: Quick optimizations, simpler interface
**Features**:
- Single window interface
- Lighter weight
- All core features

**When to use**: If you prefer simpler UI

## 🔧 Common Tasks

### Task 1: Generate Sample Data
```bash
python generate_sample_data.py
```
Creates: `sample_data/` folder with 4 sample Excel files

### Task 2: View Code Examples
```bash
python examples.py
```
Shows 6 detailed usage examples

### Task 3: Run the Main Application
```bash
python portfolio_optimizer_advanced.py
```

### Task 4: Customize Settings
Edit `config.py` to change:
- Solver parameters
- UI colors and theme
- Export options
- Logging settings

## 🐐 Troubleshooting

### Problem: "Python not found"
```bash
# Install Python from https://python.org
# Make sure to check "Add Python to PATH"
```

### Problem: "No module named pulp"
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade
```

### Problem: GUI window won't open
```bash
# Check tkinter (usually included with Python)
python -m tkinter

# If missing, install: sudo apt-get install python3-tk (Linux)
```

### Problem: "optimization failed - infeasible"
- Your constraints are too restrictive
- Try relaxing the constraint ranges
- Remove one constraint and try again

## 📊 Data Format Required

Your Excel file should have:
- One row per asset
- Column headers (any names work)
- At least one numeric column for optimization
- Optional: more columns for constraints

Example:
```
Asset    | Spread | Duration | Risk  | Sector
---------|--------|----------|-------|--------
Bond_1   | 0.045  | 5.2      | 0.08  | Finance
Bond_2   | 0.052  | 4.8      | 0.10  | Energy
...
```

## 💡 Quick Tips

1. **First time**: Use sample data to learn the workflow
2. **Constraints**: Start simple, add more gradually
3. **Large files**: 1000+ assets = slower optimization
4. **Results check**: Always verify results make sense
5. **Export**: Save results for later analysis

## 🎓 Learning Path

1. **Beginner** (15 minutes):
   - Run generate_sample_data.py
   - Launch app and load sample file
   - Run one optimization
   
2. **Intermediate** (30 minutes):
   - Prepare your own Excel file
   - Add 2-3 constraints
   - Export and analyze results

3. **Advanced** (1 hour):
   - Read examples.py
   - Write custom optimization code
   - Integrate into your workflow

4. **Expert** (2+ hours):
   - Modify optimization_engine.py
   - Create custom constraints
   - Build automated pipelines

## 📞 Quick Help

**Error on startup?**
→ Make sure requirements.txt is installed: `pip install -r requirements.txt`

**Don't know what to optimize?**
→ Use sample data first: `python generate_sample_data.py`

**Want code examples?**
→ Read examples.py or check the README.md

**Need to customize?**
→ Edit config.py or modify optimization_engine.py

## ✨ Features Quick Reference

| Feature | How To |
|---------|--------|
| Load data | Data tab → Select File button |
| Choose objective | Optimization tab → select column |
| Add constraint | Optimization tab → fill fields → Add button |
| Run optimization | Optimization tab → Run button |
| View results | Results tab (auto-updates) |
| Get analysis | Click Analysis tab |
| Export results | Results tab → Export button |

## 🎬 Ready to Start?

### Start Here:
```bash
# 1. Generate sample data
python generate_sample_data.py

# 2. Launch the application
python portfolio_optimizer_advanced.py

# 3. Load sample_data/sample_bonds.xlsx
# 4. Select "Spread" to maximize
# 5. Click "Run Optimization"
# 6. View results!
```

## 📚 Next Steps

1. ✅ Install dependencies → `pip install -r requirements.txt`
2. ✅ Generate samples → `python generate_sample_data.py`
3. ✅ Launch app → `python portfolio_optimizer_advanced.py`
4. ✅ Try it out → Follow the in-app guide
5. ✅ Load your data → Use your own portfolio
6. ✅ Optimize → Find best allocations
7. ✅ Export → Save results

---

**You're all set! 🎉**

Run this to start:
```bash
python portfolio_optimizer_advanced.py
```

Need help? Check:
- `GETTING_STARTED.md` - Detailed guide
- `README.md` - Full documentation  
- `examples.py` - Code examples
- `config.py` - Customization options
