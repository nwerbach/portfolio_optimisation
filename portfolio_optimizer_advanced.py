"""
Advanced Portfolio Optimizer with Enhanced Features
For portfolio managers and financial professionals
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import threading
from optimization_engine import AdvancedPortfolioOptimizer
from data_handler import DataHandler, ConstraintBuilder, ResultsFormatter
import traceback
from datetime import datetime
import json


class AdvancedPortfolioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Portfolio Optimizer Pro")
        self.root.geometry("1400x850")
        self.root.resizable(True, True)
        
        self.data = None
        self.optimizer = AdvancedPortfolioOptimizer()
        self.data_handler = DataHandler()
        self.results_data = None
        self.constraints = []
        
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        """Configure custom styles (dark / modern theme)"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Define colors (dark theme)
        self.colors = {
            'bg': '#1f1f2e',
            'panel': '#27293f',
            'entry': '#2e2f47',
            'tree': '#24253a',
            'fg': '#f0f0ff',
            'accent': '#3ea6ff',
            'accent2': '#6fcf97',
            'success': '#4bd37b',
            'warning': '#f2b93b',
            'error': '#ff5c5c'
        }
        
        # Root background
        self.root.configure(bg=self.colors['bg'])
        
        # General styling
        style.configure('.', background=self.colors['bg'], foreground=self.colors['fg'], font=('Segoe UI', 10))
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['fg'])
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('TLabelframe', background=self.colors['panel'], foreground=self.colors['fg'], bordercolor=self.colors['bg'])
        style.configure('TLabelframe.Label', background=self.colors['panel'], foreground=self.colors['fg'])
        style.configure('TButton', background=self.colors['accent'], foreground=self.colors['bg'], padding=6, relief='flat')
        style.map('TButton', background=[('active', self.colors['accent2']), ('pressed', self.colors['accent2'])])

        style.configure('TEntry', fieldbackground=self.colors['entry'], foreground=self.colors['fg'], bordercolor=self.colors['panel'], lightcolor=self.colors['accent'])
        style.map('TEntry', fieldbackground=[('active', self.colors['entry']), ('!disabled', self.colors['entry'])],
                  foreground=[('active', self.colors['fg']), ('!disabled', self.colors['fg'])])

        style.configure('TCombobox', fieldbackground=self.colors['entry'], background=self.colors['entry'], foreground=self.colors['fg'], bordercolor=self.colors['panel'])
        style.map('TCombobox', fieldbackground=[('readonly', self.colors['entry']), ('!disabled', self.colors['entry'])],
                  foreground=[('readonly', self.colors['fg']), ('!disabled', self.colors['fg'])])

        style.configure('Treeview', background=self.colors['tree'], foreground=self.colors['fg'], fieldbackground=self.colors['tree'], rowheight=25)
        style.configure('Treeview.Heading', background=self.colors['panel'], foreground=self.colors['fg'], relief='flat')
        style.map('Treeview', background=[('selected', self.colors['accent'])], foreground=[('selected', self.colors['bg'])])

        style.configure('TNotebook', background=self.colors['bg'])
        style.configure('TNotebook.Tab', background=self.colors['panel'], foreground=self.colors['fg'], padding=[10, 6], borderwidth=0)
        style.map('TNotebook.Tab', background=[('selected', self.colors['bg']), ('!selected', self.colors['panel'])],
                  foreground=[('selected', self.colors['fg']), ('!selected', self.colors['fg'])])
        
        # Scrollbar styling (ttk doesn't support much; falls back to system)
        style.configure('Vertical.TScrollbar', troughcolor=self.colors['panel'], background=self.colors['entry'])

    def setup_ui(self):
        """Create the main UI"""
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5, pady=5)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create tabs
        self.setup_data_tab()
        self.setup_optimization_tab()
        self.setup_results_tab()
        self.setup_analysis_tab()
        self.setup_help_tab()
    
    def setup_data_tab(self):
        """Data input and management tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Data")
        
        # Left panel - File upload
        left_frame = ttk.LabelFrame(tab, text="Data Source", padding="15")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        ttk.Label(left_frame, text="File Status:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.file_status_label = ttk.Label(left_frame, text="● No file loaded", foreground="gray")
        self.file_status_label.grid(row=0, column=1, sticky=tk.W, padx=10, pady=5)
        
        self.file_name_label = ttk.Label(left_frame, text="", font=('Arial', 8), foreground="#666")
        self.file_name_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Button(left_frame, text="📁 Select Excel File", command=self.load_file_advanced).grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Data preview
        ttk.Label(left_frame, text="Data Preview", font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=2, pady=(15, 5), sticky=tk.W)
        
        columns = ("Column", "Type", "Min", "Max", "Missing")
        self.data_tree = ttk.Treeview(left_frame, columns=columns, height=12, show="headings")
        
        self.data_tree.column("Column", width=120, anchor=tk.W)
        self.data_tree.column("Type", width=80, anchor=tk.W)
        self.data_tree.column("Min", width=80, anchor=tk.E)
        self.data_tree.column("Max", width=80, anchor=tk.E)
        self.data_tree.column("Missing", width=80, anchor=tk.E)
        
        for col in columns:
            self.data_tree.heading(col, text=col)
        
        scrollbar = ttk.Scrollbar(left_frame, orient='vertical', command=self.data_tree.yview)
        self.data_tree.configure(yscroll=scrollbar.set)
        
        self.data_tree.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        scrollbar.grid(row=4, column=2, sticky=(tk.N, tk.S))
        
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(4, weight=1)
        
        # Right panel - Statistics
        right_frame = ttk.LabelFrame(tab, text="Data Statistics", padding="15")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        self.stats_text = scrolledtext.ScrolledText(
            right_frame,
            height=25,
            width=40,
            background=self.colors['panel'],
            foreground=self.colors['fg'],
            insertbackground=self.colors['fg'],
            borderwidth=0,
            highlightthickness=0
        )
        self.stats_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)
        
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(0, weight=1)
    
    def setup_optimization_tab(self):
        """Optimization configuration tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="⚙️ Optimization")
        
        # Objective section
        obj_frame = ttk.LabelFrame(tab, text="Optimization Objective", padding="15")
        obj_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        ttk.Label(obj_frame, text="Column to Optimize:", font=('Arial', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        self.obj_col_var = tk.StringVar()
        self.obj_combo = ttk.Combobox(obj_frame, textvariable=self.obj_col_var, state="readonly", width=30)
        self.obj_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=10)
        
        ttk.Label(obj_frame, text="Optimization Type:", font=('Arial', 9, 'bold')).grid(row=0, column=2, sticky=tk.W, padx=(20, 5), pady=5)
        self.opt_type_var = tk.StringVar(value="Maximize")
        ttk.Radiobutton(obj_frame, text="Maximize", variable=self.opt_type_var, value="Maximize").grid(row=0, column=3, sticky=tk.W, pady=5)
        ttk.Radiobutton(obj_frame, text="Minimize", variable=self.opt_type_var, value="Minimize").grid(row=0, column=4, sticky=tk.W, pady=5)
        
        obj_frame.columnconfigure(1, weight=1)
        
        # Constraints section
        const_frame = ttk.LabelFrame(tab, text="Add Constraints", padding="15")
        const_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        # Constraint type selection
        ttk.Label(const_frame, text="Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.constraint_type_var = tk.StringVar(value="numeric")
        constraint_type_combo = ttk.Combobox(const_frame, textvariable=self.constraint_type_var, 
                                           state="readonly", width=18)
        constraint_type_combo['values'] = ["numeric", "category"]
        constraint_type_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        constraint_type_combo.bind("<<ComboboxSelected>>", self.on_constraint_type_changed)
        
        # Column selection
        ttk.Label(const_frame, text="Column:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.const_col_var = tk.StringVar()
        self.const_col_combo = ttk.Combobox(const_frame, textvariable=self.const_col_var, 
                                          state="readonly", width=18)
        self.const_col_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.const_col_combo.bind("<<ComboboxSelected>>", self.update_category_values)
        
        # Category value selection (for category constraints)
        ttk.Label(const_frame, text="Category:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.category_value_var = tk.StringVar()
        self.category_value_combo = ttk.Combobox(const_frame, textvariable=self.category_value_var, 
                                               state="readonly", width=18)
        self.category_value_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        self.category_value_combo['values'] = ["All Categories"]
        self.category_value_combo.current(0)
        
        # Min/Max values
        ttk.Label(const_frame, text="Min:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.const_min_var = tk.StringVar(value="0")
        ttk.Entry(const_frame, textvariable=self.const_min_var, width=18).grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        ttk.Label(const_frame, text="Max:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.const_max_var = tk.StringVar(value="1")
        ttk.Entry(const_frame, textvariable=self.const_max_var, width=18).grid(row=4, column=1, sticky=(tk.W, tk.E), padx=5, pady=2)
        
        # Add constraint button
        ttk.Button(const_frame, text="+ Add Constraint", command=self.add_constraint_advanced).grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Active constraints list
        ttk.Label(const_frame, text="Active Constraints:", font=('Arial', 9, 'bold')).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(15, 5))
        
        self.constraints_frame = ttk.Frame(const_frame)
        self.constraints_frame.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        const_frame.columnconfigure(1, weight=1)
        const_frame.rowconfigure(7, weight=1)
        
        # Run optimization
        run_frame = ttk.Frame(tab)
        run_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        ttk.Button(run_frame, text="▶ Run Optimization", command=self.run_optimization_advanced).grid(row=0, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.opt_status_var = tk.StringVar(value="Ready")
        ttk.Label(run_frame, textvariable=self.opt_status_var, foreground="blue").grid(row=0, column=1, sticky=tk.W, padx=20)
        
        run_frame.columnconfigure(0, weight=1)
        
        tab.columnconfigure(0, weight=1)
    
    def setup_results_tab(self):
        """Results display tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📈 Results")
        
        # Summary section
        summary_frame = ttk.LabelFrame(tab, text="Summary", padding="10")
        summary_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        self.summary_text = scrolledtext.ScrolledText(
            summary_frame,
            height=5,
            width=80,
            background=self.colors['panel'],
            foreground=self.colors['fg'],
            insertbackground=self.colors['fg'],
            borderwidth=0,
            highlightthickness=0
        )
        self.summary_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        summary_frame.columnconfigure(0, weight=1)
        
        # Results table section
        table_frame = ttk.LabelFrame(tab, text="Allocations", padding="10")
        table_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        columns = ("Index", "Data")
        self.results_tree = ttk.Treeview(table_frame, columns=columns, height=25, show="headings")
        self.results_tree.column("Index", width=50, anchor=tk.W)
        self.results_tree.column("Data", width=800, anchor=tk.W)
        self.results_tree.heading("Index", text="ID")
        self.results_tree.heading("Data", text="Details")
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar.set)
        
        self.results_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Export buttons
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=10)
        
        ttk.Button(button_frame, text="💾 Export to Excel", command=self.export_results_advanced).grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(button_frame, text="📋 Copy to Clipboard", command=self.copy_results).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
    
    def setup_analysis_tab(self):
        """Analysis and insights tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="🔍 Analysis")
        
        ttk.Label(tab, text="Asset Distribution Analysis", font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        
        self.analysis_text = scrolledtext.ScrolledText(
            tab,
            height=30,
            width=100,
            background=self.colors['panel'],
            foreground=self.colors['fg'],
            insertbackground=self.colors['fg'],
            borderwidth=0,
            highlightthickness=0
        )
        self.analysis_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
    
    def setup_help_tab(self):
        """Help and documentation tab"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="❓ Help")
        
        help_text = """
PORTFOLIO OPTIMIZER PRO - USER GUIDE

1. DATA UPLOAD
   • Upload an Excel (.xlsx) file with portfolio data
   • Each row represents an asset
   • Columns can contain any attribute (spread, duration, rating, sector, etc.)

2. OPTIMIZATION
   • Select which column to optimize (usually a return/yield metric)
   • Choose to Maximize or Minimize the objective
   • Set constraints on column values or categories

3. CONSTRAINT TYPES
   • NUMERIC CONSTRAINTS: Apply min/max limits to numeric column totals
     Example: Duration between 2.0 and 4.0 years
   • CATEGORY CONSTRAINTS: Apply diversification limits to categorical columns
     - All Categories: Each category gets the same min/max limit
       Example: Max 30% per sector for diversification
     - Specific Category: Apply limit to one category only
       Example: Finance sector max 20%

4. CONSTRAINTS
   • Add constraints to control portfolio composition
   • Min/Max constraints ensure diversified allocations
   • Constraints prevent extreme positions

5. RESULTS
   • View allocation percentages for each selected asset
   • View optimization summary statistics
   • Export results to Excel for further analysis

6. TIPS
   • Use category constraints for sector/country diversification
   • Start with the original objective and add constraints gradually
   • Check if results are realistic before deploying

TECHNICAL DETAILS
   • Uses PuLP for linear programming optimization
   • All allocations sum to 100% (normalized portfolio)
   • Solver: CBC (Coin-or-branch and cut)

For issues or questions, refer to the README file.
        """
        
        help_label = ttk.Label(tab, text=help_text, justify=tk.LEFT, wraplength=800)
        help_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        
        tab.columnconfigure(0, weight=1)
    
    def load_file_advanced(self):
        """Load Excel file with advanced preview"""
        file_path = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            self.data = pd.read_excel(file_path)
            
            # Update file status
            self.file_status_label.config(text="● File loaded", foreground="green")
            self.file_name_label.config(text=file_path)
            
            # Update combo boxes
            numeric_cols = self.data_handler.get_numeric_columns(self.data)
            all_cols = self.data.columns.tolist()
            
            self.obj_combo['values'] = numeric_cols
            if numeric_cols:
                self.obj_combo.current(0)
            
            # Initialize constraint columns based on current constraint type
            self.on_constraint_type_changed()
            
            # Update data preview
            self.update_data_preview()
            
            # Update statistics
            self.update_data_statistics()
            
            self.opt_status_var.set("✓ Data loaded successfully")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def update_data_preview(self):
        """Update data preview table"""
        for item in self.data_tree.get_children():
            self.data_tree.delete(item)
        
        for col in self.data.columns:
            dtype = str(self.data[col].dtype)
            
            if pd.api.types.is_numeric_dtype(self.data[col]):
                min_val = f"{self.data[col].min():.4f}"
                max_val = f"{self.data[col].max():.4f}"
            else:
                min_val = "-"
                max_val = "-"
            
            missing = self.data[col].isnull().sum()
            
            self.data_tree.insert('', tk.END, values=(col, dtype, min_val, max_val, missing))
    
    def update_data_statistics(self):
        """Update data statistics display"""
        summary = self.data_handler.get_data_summary(self.data)
        
        self.stats_text.config(state='normal')
        self.stats_text.delete(1.0, tk.END)
        
        stats_text = f"""
DATA STATISTICS
{'='*35}

Rows: {summary['rows']}
Columns: {summary['columns']}
Numeric Columns: {summary['numeric_cols']}
Categorical Columns: {summary['categorical_cols']}
Missing Values: {summary['missing_values']}

COLUMNS OVERVIEW
{'='*35}
"""
        
        for col in self.data.columns:
            stats_text += f"\n{col}:\n"
            if pd.api.types.is_numeric_dtype(self.data[col]):
                stats_text += f"  Type: Numeric\n"
                stats_text += f"  Mean: {self.data[col].mean():.4f}\n"
                stats_text += f"  Std: {self.data[col].std():.4f}\n"
                stats_text += f"  Min: {self.data[col].min():.4f}\n"
                stats_text += f"  Max: {self.data[col].max():.4f}\n"
            else:
                stats_text += f"  Type: Categorical\n"
                stats_text += f"  Unique: {self.data[col].nunique()}\n"
        
        self.stats_text.insert(tk.END, stats_text)
        self.stats_text.config(state='disabled')
    
    def add_constraint_advanced(self):
        """Add constraint with validation"""
        constraint_type = self.constraint_type_var.get()
        col = self.const_col_var.get()
        min_val = self.const_min_var.get()
        max_val = self.const_max_var.get()
        category_value = self.category_value_var.get()
        
        if not col:
            messagebox.showwarning("Warning", "Select a column")
            return
        
        try:
            min_val = float(min_val)
            max_val = float(max_val)
            
            builder = ConstraintBuilder()
            
            if constraint_type == "numeric":
                constraint = builder.create_constraint(col, min_val, max_val)
            elif constraint_type == "category":
                if category_value == "All Categories":
                    category_value = None
                # create_category_constraint signature: (column, category_value, min_val, max_val)
                constraint = builder.create_category_constraint(col, category_value, min_val, max_val)
            
            is_valid, msg = builder.validate_constraint(constraint, self.data)
            if not is_valid:
                messagebox.showwarning("Invalid Constraint", msg)
                return
            
            self.constraints.append(constraint)
            self.display_constraints()
            
            constraint_desc = f"{constraint_type} constraint on {col}"
            if constraint_type == "category" and constraint.get('category_value'):
                constraint_desc += f" ({constraint['category_value']})"
            self.opt_status_var.set(f"Added {constraint_desc}")
            
        except ValueError:
            messagebox.showerror("Error", "Min and Max must be numbers")
    
    def on_constraint_type_changed(self, event=None):
        """Update column list based on constraint type"""
        if self.data is None:
            return
        
        constraint_type = self.constraint_type_var.get()
        
        if constraint_type == "numeric":
            # Show only numeric columns
            columns = self.data_handler.get_numeric_columns(self.data)
        elif constraint_type == "category":
            # Show all columns (categorical constraints can be applied to any column)
            columns = self.data.columns.tolist()
        
        self.const_col_combo['values'] = columns
        if columns:
            self.const_col_combo.current(0)
            self.update_category_values()
        else:
            self.const_col_var.set("")
            self.category_value_combo['values'] = ["All Categories"]
            self.category_value_combo.current(0)
    
    def update_category_values(self, event=None):
        """Update category values dropdown based on selected column"""
        if self.data is None:
            return
        
        col = self.const_col_var.get()
        constraint_type = self.constraint_type_var.get()
        
        if constraint_type == "category" and col:
            # For category constraints, show unique values plus "All Categories"
            unique_values = sorted(self.data[col].dropna().unique().tolist())
            category_values = ["All Categories"] + unique_values
            self.category_value_combo['values'] = category_values
            self.category_value_combo.current(0)
        else:
            # For numeric constraints, hide category selection
            self.category_value_combo['values'] = ["All Categories"]
            self.category_value_combo.current(0)
    
    def display_constraints(self):
        """Display active constraints"""
        for widget in self.constraints_frame.winfo_children():
            widget.destroy()
        
        for i, constraint in enumerate(self.constraints):
            constraint_type = constraint.get('type', 'numeric')
            col = constraint['column']
            min_val = constraint['min']
            max_val = constraint['max']
            
            if constraint_type == "category":
                category_value = constraint.get('category_value')
                if category_value:
                    constraint_text = f"Category {col} ({category_value}): [{min_val}, {max_val}]"
                else:
                    constraint_text = f"Category {col} (all): [{min_val}, {max_val}]"
            else:
                constraint_text = f"{col}: [{min_val}, {max_val}]"
            
            frame = ttk.Frame(self.constraints_frame)
            frame.pack(fill=tk.X, pady=3)
            
            ttk.Label(frame, text=constraint_text, background="#e8f4f8", foreground="#333").pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=3)
            ttk.Button(frame, text="Remove", width=8, command=lambda idx=i: self.remove_constraint_advanced(idx)).pack(side=tk.RIGHT, padx=3)
    
    def remove_constraint_advanced(self, idx):
        """Remove constraint at index"""
        if 0 <= idx < len(self.constraints):
            self.constraints.pop(idx)
            self.display_constraints()
            self.opt_status_var.set("Constraint removed")
    
    def run_optimization_advanced(self):
        """Run optimization in thread"""
        if self.data is None:
            messagebox.showwarning("Warning", "Load data first")
            return
        
        if not self.obj_col_var.get():
            messagebox.showwarning("Warning", "Select objective column")
            return
        
        thread = threading.Thread(target=self._optimize_thread_advanced)
        thread.daemon = True
        thread.start()
    
    def _optimize_thread_advanced(self):
        """Optimization thread"""
        try:
            self.opt_status_var.set("⏳ Optimizing...")
            self.root.update()
            
            objective_col = self.obj_col_var.get()
            direction = self.opt_type_var.get()
            
            self.results_data = self.optimizer.optimize(
                data=self.data,
                objective_column=objective_col,
                direction=direction,
                custom_constraints=self.constraints
            )
            
            self.display_results_advanced()
            self.generate_analysis()
            
            self.opt_status_var.set("✓ Optimization complete!")
            
        except Exception as e:
            self.opt_status_var.set("✗ Error")
            messagebox.showerror("Error", f"{str(e)}\n\n{traceback.format_exc()}")
    
    def display_results_advanced(self):
        """Display results in results tab"""
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Display summary
        summary_info = self.results_data.get('summary', {})
        self.summary_text.config(state='normal')
        self.summary_text.delete(1.0, tk.END)
        
        summary_text = "OPTIMIZATION RESULTS\n" + "="*60 + "\n"
        for key, value in summary_info.items():
            summary_text += f"{key:.<40} {value}\n"
        
        self.summary_text.insert(tk.END, summary_text)
        self.summary_text.config(state='disabled')
        
        # Display allocations
        results_df = self.results_data.get('allocations', pd.DataFrame())
        
        for idx, row in results_df.iterrows():
            details = " | ".join([f"{col}: {row[col]}" for col in results_df.columns])
            self.results_tree.insert('', tk.END, values=(idx, details))
    
    def generate_analysis(self):
        """Generate analysis report"""
        if self.results_data is None:
            return
        
        results_df = self.results_data.get('allocations', pd.DataFrame())
        
        analysis = "PORTFOLIO ANALYSIS REPORT\n"
        analysis += "="*60 + "\n\n"
        
        analysis += f"Number of assets selected: {len(results_df)}\n"
        analysis += f"Total allocation: {results_df['allocation'].sum():.2%}\n\n"
        
        analysis += "Top 5 Allocations:\n"
        analysis += "-"*60 + "\n"
        top_allocations = results_df.nlargest(5, 'allocation')
        for idx, (_, row) in enumerate(top_allocations.iterrows(), 1):
            analysis += f"{idx}. Allocation: {row['allocation']:.2%}\n"
        
        analysis += "\n\nConstraint Summary:\n"
        analysis += "-"*60 + "\n"
        if self.constraints:
            for constraint in self.constraints:
                constraint_type = constraint.get('type', 'numeric')
                col = constraint['column']
                min_val = constraint['min']
                max_val = constraint['max']
                
                if constraint_type == "category":
                    category_value = constraint.get('category_value')
                    if category_value:
                        analysis += f"• Category {col} ({category_value}): [{min_val}, {max_val}]\n"
                    else:
                        analysis += f"• Category {col} (all categories): [{min_val}, {max_val}]\n"
                else:
                    analysis += f"• {col}: [{min_val}, {max_val}]\n"
        else:
            analysis += "No constraints applied\n"
        
        self.analysis_text.config(state='normal')
        self.analysis_text.delete(1.0, tk.END)
        self.analysis_text.insert(tk.END, analysis)
        self.analysis_text.config(state='disabled')
    
    def export_results_advanced(self):
        """Export results"""
        if self.results_data is None:
            messagebox.showwarning("Warning", "Run optimization first")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if file_path:
            try:
                results_df = self.results_data.get('allocations', pd.DataFrame())
                summary = self.results_data.get('summary', {})
                
                ResultsFormatter.export_to_excel(results_df, file_path, summary)
                messagebox.showinfo("Success", f"Exported to:\n{file_path}")
                self.opt_status_var.set("✓ Results exported")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed:\n{str(e)}")
    
    def copy_results(self):
        """Copy results to clipboard"""
        if self.results_data is None:
            return
        
        results_df = self.results_data.get('allocations', pd.DataFrame())
        results_text = results_df.to_string()
        
        self.root.clipboard_clear()
        self.root.clipboard_append(results_text)
        messagebox.showinfo("Success", "Results copied to clipboard")


def main():
    root = tk.Tk()
    app = AdvancedPortfolioGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
