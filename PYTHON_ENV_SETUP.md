# Python Environment Setup - Your System

## ✅ Your Python Configuration

**Environment Type**: System Python (global installation)  
**Python Version**: 3.13.12 (latest)  
**Installation Location**: `C:\Users\nico\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.13_qbz5n2kfra8p0`

## ✅ All Required Packages Are Installed

```
✓ PuLP       3.3.0   (Linear programming solver)
✓ Pandas     2.2.3   (Data manipulation)
✓ NumPy      2.2.2   (Numerical computing)
✓ SciPy      1.17.1  (Scientific computing)
✓ OpenPyXL   3.1.5   (Excel file handling)
```

## 🚀 How to Run the Application

### Option 1: Simple Command (Recommended)
```powershell
python portfolio_optimizer_advanced.py
```

### Option 2: Using Full Python Path
```powershell
C:/Users/nico/AppData/Local/Microsoft/WindowsApps/python3.13.exe portfolio_optimizer_advanced.py
```

### Option 3: Using Batch File
```powershell
.\launch.bat
```

### Option 4: With Sample Data First
```powershell
python generate_sample_data.py
python portfolio_optimizer_advanced.py
```

## 📋 Testing Your Setup

```powershell
# Verify all packages are working
python -c "import pulp, pandas, openpyxl, numpy, scipy; print('✓ All packages ready!')"

# Or just run the app
python portfolio_optimizer_advanced.py
```

## ⚡ Quick Start (Once Environment is Ready)

```powershell
# 1. Generate test data (optional but recommended)
python generate_sample_data.py

# 2. Launch the GUI
python portfolio_optimizer_advanced.py

# 3. In the GUI:
#    - Click "📊 Data" tab
#    - Click "📁 Select File"
#    - Load sample_data/sample_bonds.xlsx
#    - Go to "⚙️ Optimization" tab
#    - Select "Spread" as objective
#    - Click "▶ Run Optimization"
#    - View results!
```

## 🔧 Alternative: Virtual Environment (Optional)

If you want to isolate this project from other Python projects:

```powershell
# Create virtual environment
python -m venv portfolio_env

# Activate it
portfolio_env\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run the app
python portfolio_optimizer_advanced.py

# To deactivate later
deactivate
```

## 📝 Notes

- System Python is fine for this project
- All packages are up-to-date for Python 3.13
- No additional configuration needed
- The GUI will start in a new window

---

**Ready to go!** Run this command:
```powershell
python portfolio_optimizer_advanced.py
```
