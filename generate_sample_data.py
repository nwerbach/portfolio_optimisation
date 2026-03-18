"""
Sample Data Generator for Portfolio Optimizer
Creates sample Excel files for testing the application
"""

import pandas as pd
import numpy as np
import os


def generate_bond_portfolio():
    """Generate sample bond portfolio data"""
    np.random.seed(42)
    
    n_bonds = 20
    sectors = ['Finance', 'Energy', 'Utilities', 'Healthcare', 'Tech']
    ratings = ['AAA', 'AA', 'A', 'BBB', 'BB']
    
    data = {
        'ID': range(1, n_bonds + 1),
        'Ticker': [f'BOND{i:03d}' for i in range(1, n_bonds + 1)],
        'Spread': np.random.uniform(0.03, 0.08, n_bonds),
        'Duration': np.random.uniform(2, 10, n_bonds),
        'Coupon': np.random.uniform(0.02, 0.06, n_bonds),
        'Rating': np.random.choice(ratings, n_bonds),
        'Sector': np.random.choice(sectors, n_bonds),
        'Maturity_Years': np.random.randint(1, 30, n_bonds),
        'Rating_Score': np.random.uniform(3, 9, n_bonds),  # 9=AAA, 3=BB
    }
    
    df = pd.DataFrame(data)
    return df


def generate_stock_portfolio():
    """Generate sample stock portfolio data"""
    np.random.seed(42)
    
    n_stocks = 25
    sectors = ['Tech', 'Finance', 'Healthcare', 'Energy', 'Consumer', 'Industrials']
    
    data = {
        'ID': range(1, n_stocks + 1),
        'Ticker': [f'STK{i:03d}' for i in range(1, n_stocks + 1)],
        'Expected_Return': np.random.uniform(0.05, 0.20, n_stocks),
        'Volatility': np.random.uniform(0.10, 0.40, n_stocks),
        'Beta': np.random.uniform(0.5, 2.0, n_stocks),
        'Market_Cap_Billions': np.random.uniform(1, 500, n_stocks),
        'Dividend_Yield': np.random.uniform(0, 0.05, n_stocks),
        'PE_Ratio': np.random.uniform(5, 50, n_stocks),
        'Sector': np.random.choice(sectors, n_stocks),
        'Growth_Score': np.random.uniform(1, 10, n_stocks),
    }
    
    df = pd.DataFrame(data)
    return df


def generate_mixed_portfolio():
    """Generate mixed portfolio with multiple asset classes"""
    np.random.seed(42)
    
    # Bonds (40% of portfolio)
    n_bonds = 15
    bonds_data = {
        'Asset': [f'Bond_{i}' for i in range(1, n_bonds + 1)],
        'Type': 'Bond',
        'Expected_Return': np.random.uniform(0.02, 0.05, n_bonds),
        'Risk': np.random.uniform(0.03, 0.08, n_bonds),
        'Duration': np.random.uniform(2, 10, n_bonds),
    }
    
    # Stocks (50% of portfolio)
    n_stocks = 20
    stocks_data = {
        'Asset': [f'Stock_{i}' for i in range(1, n_stocks + 1)],
        'Type': 'Stock',
        'Expected_Return': np.random.uniform(0.08, 0.20, n_stocks),
        'Risk': np.random.uniform(0.15, 0.35, n_stocks),
        'Duration': np.random.uniform(0, 2, n_stocks),
    }
    
    # Real Estate (10% of portfolio)
    n_re = 5
    re_data = {
        'Asset': [f'RealEstate_{i}' for i in range(1, n_re + 1)],
        'Type': 'RealEstate',
        'Expected_Return': np.random.uniform(0.05, 0.12, n_re),
        'Risk': np.random.uniform(0.10, 0.20, n_re),
        'Duration': np.random.uniform(5, 15, n_re),
    }
    
    # Combine all
    all_data = []
    for i, asset in enumerate(bonds_data['Asset']):
        all_data.append({
            'ID': i + 1,
            'Asset': asset,
            'Type': 'Bond',
            'Expected_Return': bonds_data['Expected_Return'][i],
            'Risk': bonds_data['Risk'][i],
            'Duration': bonds_data['Duration'][i],
        })
    
    for i, asset in enumerate(stocks_data['Asset']):
        all_data.append({
            'ID': len(all_data) + 1,
            'Asset': asset,
            'Type': 'Stock',
            'Expected_Return': stocks_data['Expected_Return'][i],
            'Risk': stocks_data['Risk'][i],
            'Duration': stocks_data['Duration'][i],
        })
    
    for i, asset in enumerate(re_data['Asset']):
        all_data.append({
            'ID': len(all_data) + 1,
            'Asset': asset,
            'Type': 'RealEstate',
            'Expected_Return': re_data['Expected_Return'][i],
            'Risk': re_data['Risk'][i],
            'Duration': re_data['Duration'][i],
        })
    
    df = pd.DataFrame(all_data)
    return df


def generate_cryptocurrency_portfolio():
    """Generate sample cryptocurrency portfolio data"""
    np.random.seed(42)
    
    cryptos = ['Bitcoin', 'Ethereum', 'Cardano', 'Solana', 'Polkadot', 
               'Ripple', 'Litecoin', 'Chainlink', 'Uniswap', 'Polygon']
    
    data = {
        'ID': range(1, len(cryptos) + 1),
        'Ticker': cryptos,
        'Market_Cap_B': np.random.uniform(1, 1000, len(cryptos)),
        'Price_Change_24h': np.random.uniform(-10, 10, len(cryptos)),
        'Volume_B': np.random.uniform(0.1, 100, len(cryptos)),
        'Volatility': np.random.uniform(0.05, 0.35, len(cryptos)),
        'Sharpe_Ratio': np.random.uniform(-1, 3, len(cryptos)),
        'Community_Score': np.random.uniform(1, 100, len(cryptos)),
    }
    
    df = pd.DataFrame(data)
    return df


def main():
    """Generate all sample files"""
    print("="*60)
    print("Portfolio Optimizer - Sample Data Generator")
    print("="*60)
    print()
    
    # Create sample_data directory if it doesn't exist
    if not os.path.exists('sample_data'):
        os.makedirs('sample_data')
    
    # Generate Bond Portfolio
    print("Generating Bond Portfolio sample...")
    df_bonds = generate_bond_portfolio()
    bonds_file = 'sample_data/sample_bonds.xlsx'
    df_bonds.to_excel(bonds_file, index=False)
    print(f"✓ Created: {bonds_file} ({len(df_bonds)} bonds)")
    
    # Generate Stock Portfolio
    print("Generating Stock Portfolio sample...")
    df_stocks = generate_stock_portfolio()
    stocks_file = 'sample_data/sample_stocks.xlsx'
    df_stocks.to_excel(stocks_file, index=False)
    print(f"✓ Created: {stocks_file} ({len(df_stocks)} stocks)")
    
    # Generate Mixed Portfolio
    print("Generating Mixed Portfolio sample...")
    df_mixed = generate_mixed_portfolio()
    mixed_file = 'sample_data/sample_mixed.xlsx'
    df_mixed.to_excel(mixed_file, index=False)
    print(f"✓ Created: {mixed_file} ({len(df_mixed)} assets)")
    
    # Generate Cryptocurrency Portfolio
    print("Generating Cryptocurrency Portfolio sample...")
    df_crypto = generate_cryptocurrency_portfolio()
    crypto_file = 'sample_data/sample_crypto.xlsx'
    df_crypto.to_excel(crypto_file, index=False)
    print(f"✓ Created: {crypto_file} ({len(df_crypto)} cryptocurrencies)")
    
    print()
    print("="*60)
    print("Sample data files created successfully!")
    print("="*60)
    print()
    print("You can now use these files to test the Portfolio Optimizer:")
    print("  1. Launch: python portfolio_optimizer_advanced.py")
    print("  2. Click 'Select File' and choose a sample_*.xlsx file")
    print("  3. Configure your optimization and run")
    print()


if __name__ == "__main__":
    main()
