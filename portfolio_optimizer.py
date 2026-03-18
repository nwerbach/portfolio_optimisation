"""
Portfolio Optimizer GUI Application
Main entry point with GUI using tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import threading
from optimization_engine import PortfolioOptimizer
from data_handler import DataHandler
import traceback


class PortfolioOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Optimizer")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        self.data = None
        self.optimizer = PortfolioOptimizer()
        self.data_handler = DataHandler()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the main UI"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsive layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # ===== LEFT PANEL: Controls =====
        left_frame = ttk.LabelFrame(main_frame, text="Configuration", padding="10")
        left_frame.grid(row=0, column=0, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # File upload section
        ttk.Label(left_frame, text="Step 1: Upload Data", font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky=tk.W)
        
        self.file_label = ttk.Label(left_frame, text="No file selected", foreground="gray")
        self.file_label.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Button(left_frame, text="Select File (.xlsx)", command=self.load_file).grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Optimization settings section
        ttk.Label(left_frame, text="Step 2: Optimization", font=('Arial', 10, 'bold')).grid(row=3, column=0, columnspan=2, pady=(15, 10), sticky=tk.W)
        
        ttk.Label(left_frame, text="Objective:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.objective_var = tk.StringVar()
        self.objective_combo = ttk.Combobox(left_frame, textvariable=self.objective_var, state="readonly", width=20)
        self.objective_combo.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5)
        self.objective_combo.bind("<<ComboboxSelected>>", self.on_objective_changed)
        
        ttk.Label(left_frame, text="Optimize:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.direction_var = tk.StringVar(value="Maximize")
        ttk.Radiobutton(left_frame, text="Maximize", variable=self.direction_var, value="Maximize").grid(row=5, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(left_frame, text="Minimize", variable=self.direction_var, value="Minimize").grid(row=6, column=1, sticky=tk.W, pady=5)
        
        # Constraints section
        ttk.Label(left_frame, text="Step 3: Constraints", font=('Arial', 10, 'bold')).grid(row=7, column=0, columnspan=2, pady=(15, 10), sticky=tk.W)
        
        ttk.Label(left_frame, text="Constraint column:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.constraint_col_var = tk.StringVar()
        self.constraint_col_combo = ttk.Combobox(left_frame, textvariable=self.constraint_col_var, state="readonly", width=20)
        self.constraint_col_combo.grid(row=8, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(left_frame, text="Min value:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.constraint_min_var = tk.StringVar(value="0")
        ttk.Entry(left_frame, textvariable=self.constraint_min_var, width=20).grid(row=9, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(left_frame, text="Max value:").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.constraint_max_var = tk.StringVar(value="1")
        ttk.Entry(left_frame, textvariable=self.constraint_max_var, width=20).grid(row=10, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(left_frame, text="Add Constraint", command=self.add_constraint).grid(row=11, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Constraints list
        ttk.Label(left_frame, text="Active Constraints:", font=('Arial', 9, 'bold')).grid(row=12, column=0, columnspan=2, pady=(10, 5), sticky=tk.W)
        
        self.constraints_listbox = tk.Listbox(left_frame, height=6, width=30)
        self.constraints_listbox.grid(row=13, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        ttk.Button(left_frame, text="Remove Selected", command=self.remove_constraint).grid(row=14, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Run optimization button
        ttk.Button(left_frame, text="▶ Run Optimization", command=self.run_optimization).grid(row=15, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(20, 5))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(left_frame, textvariable=self.status_var, foreground="blue", wraplength=280)
        status_bar.grid(row=16, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))
        
        left_frame.columnconfigure(1, weight=1)
        
        # ===== RIGHT PANEL: Results =====
        right_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        right_frame.grid(row=0, column=1, rowspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Optimization summary
        self.summary_text = tk.Text(right_frame, height=8, width=60, background="#f0f0f0")
        self.summary_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Results table
        columns = ("Asset", "Values")
        self.results_tree = ttk.Treeview(right_frame, columns=columns, height=20, show="headings")
        self.results_tree.column("Asset", width=300, anchor=tk.W)
        self.results_tree.column("Values", width=200, anchor=tk.W)
        self.results_tree.heading("Asset", text="Asset Details")
        self.results_tree.heading("Values", text="Allocation")
        
        scrollbar = ttk.Scrollbar(right_frame, orient='vertical', command=self.results_tree.yview)
        self.results_tree.configure(yscroll=scrollbar.set)
        
        self.results_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        ttk.Button(right_frame, text="Export Results", command=self.export_results).grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        self.constraints = []
        self.results_data = None
        
    def load_file(self):
        """Load Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.data = pd.read_excel(file_path)
                self.file_label.config(text=f"✓ Loaded: {file_path.split('/')[-1]}", foreground="green")
                
                # Update objective column combo
                numeric_cols = self.data.select_dtypes(include=['number']).columns.tolist()
                self.objective_combo['values'] = numeric_cols
                if numeric_cols:
                    self.objective_combo.current(0)
                
                # Update constraint column combo
                self.constraint_col_combo['values'] = self.data.columns.tolist()
                
                self.status_var.set(f"Loaded {len(self.data)} rows, {len(self.data.columns)} columns")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def on_objective_changed(self, event=None):
        """Update direction based on objective"""
        pass
    
    def add_constraint(self):
        """Add a linear constraint"""
        col = self.constraint_col_var.get()
        min_val = self.constraint_min_var.get()
        max_val = self.constraint_max_var.get()
        
        if not col:
            messagebox.showwarning("Warning", "Please select a constraint column")
            return
        
        try:
            min_val = float(min_val)
            max_val = float(max_val)
            
            if min_val > max_val:
                messagebox.showwarning("Warning", "Min value cannot be greater than max value")
                return
            
            constraint = {
                'column': col,
                'min': min_val,
                'max': max_val
            }
            self.constraints.append(constraint)
            
            self.constraints_listbox.insert(tk.END, f"{col}: [{min_val}, {max_val}]")
            self.status_var.set(f"Added constraint: {col}")
            
        except ValueError:
            messagebox.showerror("Error", "Min and Max values must be numbers")
    
    def remove_constraint(self):
        """Remove selected constraint"""
        selection = self.constraints_listbox.curselection()
        if selection:
            idx = selection[0]
            self.constraints_listbox.delete(idx)
            self.constraints.pop(idx)
            self.status_var.set("Constraint removed")
    
    def run_optimization(self):
        """Run the optimization in a separate thread"""
        if self.data is None:
            messagebox.showwarning("Warning", "Please load a file first")
            return
        
        if not self.objective_var.get():
            messagebox.showwarning("Warning", "Please select an objective column")
            return
        
        # Run in thread to prevent GUI freezing
        thread = threading.Thread(target=self._optimize_thread)
        thread.start()
    
    def _optimize_thread(self):
        """Optimization thread"""
        try:
            self.status_var.set("⏳ Optimizing...")
            self.root.update()
            
            objective_col = self.objective_var.get()
            direction = self.direction_var.get()
            
            # Run optimization
            self.results_data = self.optimizer.optimize(
                data=self.data,
                objective_column=objective_col,
                direction=direction,
                custom_constraints=self.constraints
            )
            
            self.display_results()
            self.status_var.set("✓ Optimization complete!")
            
        except Exception as e:
            self.status_var.set("✗ Error during optimization")
            messagebox.showerror("Optimization Error", f"{str(e)}\n\n{traceback.format_exc()}")
    
    def display_results(self):
        """Display results in the results tree"""
        if self.results_data is None:
            return
        
        # Clear existing items
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Update summary
        summary_info = self.results_data.get('summary', {})
        self.summary_text.config(state='normal')
        self.summary_text.delete(1.0, tk.END)
        
        summary_text = "=== OPTIMIZATION SUMMARY ===\n\n"
        for key, value in summary_info.items():
            summary_text += f"{key}: {value}\n"
        
        self.summary_text.insert(tk.END, summary_text)
        self.summary_text.config(state='disabled')
        
        # Display results
        results_df = self.results_data.get('allocations', pd.DataFrame())
        
        for idx, row in results_df.iterrows():
            values = []
            for col in results_df.columns:
                val = row[col]
                if isinstance(val, float):
                    values.append(f"{col}: {val:.6f}")
                else:
                    values.append(f"{col}: {val}")
            
            self.results_tree.insert('', tk.END, values=(f"Row {idx}", " | ".join(values)))
    
    def export_results(self):
        """Export results to Excel"""
        if self.results_data is None:
            messagebox.showwarning("Warning", "No results to export. Run optimization first.")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        
        if file_path:
            try:
                results_df = self.results_data.get('allocations', pd.DataFrame())
                results_df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", f"Results exported to:\n{file_path}")
                self.status_var.set("✓ Results exported")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export:\n{str(e)}")


def main():
    root = tk.Tk()
    app = PortfolioOptimizerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
