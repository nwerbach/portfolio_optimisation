"""
Configuration file for Portfolio Optimizer
Customize solver settings, constraints, and UI preferences
"""

# ============================================================================
# SOLVER CONFIGURATION
# ============================================================================

SOLVER_CONFIG = {
    # Solver engine: 'CBC' (recommended), 'PULP_CBC_CMD', 'CPLEX', 'GLPK'
    'engine': 'PULP_CBC_CMD',
    
    # Solver verbosity: 0=quiet, 1=verbose
    'verbosity': 0,
    
    # Maximum time in seconds for solver (0=no limit)
    'max_seconds': 300,
    
    # Number of processing threads (-1=auto)
    'threads': -1,
    
    # Gap tolerance (stops when within this % of optimal): 0-1
    'gap': 0.0,
    
    # Problem writing format: 'LP', 'MPS'
    'format': 'LP',
}

# ============================================================================
# DATA HANDLING
# ============================================================================

DATA_CONFIG = {
    # How to handle missing values: 'mean', 'median', 'drop', 'forward_fill'
    'missing_value_strategy': 'mean',
    
    # Whether to normalize data between 0-1
    'normalize_data': False,
    
    # Columns to exclude from constraint selection
    'exclude_columns': ['ID', 'Name', 'Ticker'],
    
    # Default decimal precision for display
    'decimal_precision': 6,
    
    # Allocation precision for results
    'allocation_precision': 4,
}

# ============================================================================
# OPTIMIZATION DEFAULTS
# ============================================================================

OPTIMIZATION_CONFIG = {
    # Default optimization direction: 'Maximize' or 'Minimize'
    'default_direction': 'Maximize',
    
    # Minimum allocation threshold (assets with less ignored in results)
    'min_allocation_threshold': 1e-6,
    
    # Default total portfolio size (1.0 = 100%)
    'portfolio_size': 1.0,
    
    # Whether to force integer allocations
    'force_integer': False,
}

# ============================================================================
# UI CONFIGURATION
# ============================================================================

UI_CONFIG = {
    # Window size (width, height)
    'window_size': (1400, 850),
    
    # Theme: 'clam', 'alt', 'default'
    'theme': 'clam',
    
    # Colors (can be hex or named colors)
    'colors': {
        'bg': '#f0f0f0',
        'fg': '#333333',
        'accent': '#0078d4',
        'success': '#107c10',
        'warning': '#ffb900',
        'error': '#d13438',
        'light_bg': '#f5f5f5',
    },
    
    # Font settings
    'fonts': {
        'default': ('Arial', 10),
        'bold': ('Arial', 10, 'bold'),
        'title': ('Arial', 12, 'bold'),
        'mono': ('Courier New', 9),
    },
    
    # Show detailed logging
    'show_logs': False,
}

# ============================================================================
# DEFAULT CONSTRAINTS
# ============================================================================

DEFAULT_CONSTRAINTS = [
    # Uncomment to add default constraints that apply to all optimizations
    # {
    #     'column': 'Duration',
    #     'min': 4.0,
    #     'max': 8.0,
    #     'description': 'Portfolio duration between 4-8 years'
    # },
]

# ============================================================================
# EXPORT CONFIGURATION
# ============================================================================

EXPORT_CONFIG = {
    # Include summary sheet in Excel exports
    'include_summary': True,
    
    # Include analysis sheet in Excel exports
    'include_analysis': True,
    
    # Default export location
    'default_export_dir': '.',
    
    # File naming convention (use {timestamp} for date-time)
    'filename_template': 'portfolio_results_{timestamp}.xlsx',
}

# ============================================================================
# LOGGING
# ============================================================================

LOGGING_CONFIG = {
    # Log level: 'DEBUG', 'INFO', 'WARNING', 'ERROR'
    'level': 'INFO',
    
    # Log file name (empty string = no logging)
    'file': 'portfolio_optimizer.log',
    
    # Max log file size in MB before rotating
    'max_size_mb': 10,
}

# ============================================================================
# ADVANCED FEATURES
# ============================================================================

ADVANCED_CONFIG = {
    # Enable sensitivity analysis
    'enable_sensitivity': True,
    
    # Enable what-if analysis
    'enable_whatif': True,
    
    # Enable portfolio comparison
    'enable_comparison': True,
    
    # Cache optimization results
    'cache_results': True,
    
    # Maximum number of results to keep in cache
    'cache_size': 100,
}

# ============================================================================
# CONSTRAINTS BY ASSET CLASS
# ============================================================================

# Automatically apply constraints based on detected asset class
ASSET_CLASS_DEFAULTS = {
    'bonds': {
        'duration_range': (2, 10),
        'max_concentration': 0.20,
    },
    'stocks': {
        'max_volatility': 0.35,
        'min_market_cap': 1.0,  # billions
    },
    'real_estate': {
        'max_concentration': 0.15,
        'min_yield': 0.03,
    },
    'crypto': {
        'max_concentration': 0.05,
        'max_volatility': 0.50,
    },
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_solver_kwargs():
    """Get solver keyword arguments for PuLP"""
    config = SOLVER_CONFIG
    kwargs = {
        'msg': config['verbosity'],
        'maxSeconds': config['max_seconds'],
        'threads': config['threads'] if config['threads'] > 0 else 4,
    }
    if config['gap'] > 0:
        kwargs['gap'] = config['gap']
    
    return kwargs


def get_colors():
    """Get UI colors"""
    return UI_CONFIG['colors']


def get_constraint_by_asset_class(asset_class):
    """Get default constraints for asset class"""
    return ASSET_CLASS_DEFAULTS.get(asset_class.lower(), {})


if __name__ == "__main__":
    # Print configuration summary
    print("Portfolio Optimizer Configuration")
    print("="*60)
    print(f"Solver: {SOLVER_CONFIG['engine']}")
    print(f"Missing value strategy: {DATA_CONFIG['missing_value_strategy']}")
    print(f"Default direction: {OPTIMIZATION_CONFIG['default_direction']}")
    print(f"UI Theme: {UI_CONFIG['theme']}")
    print(f"Export dir: {EXPORT_CONFIG['default_export_dir']}")
    print("="*60)
