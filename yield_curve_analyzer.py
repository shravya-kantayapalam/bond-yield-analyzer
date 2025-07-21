"""
Bond Yield Curve Analyzer (Fixed Version)
-----------------------------------------
Fetches US Treasury yield data and analyzes yield curve dynamics.
Author: [Your Name]
Date: 2025-07-22
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def fetch_treasury_data(period_days=365):
    """
    Fetch US Treasury yields for different maturities
    """
    end_date = datetime.today()
    start_date = end_date - timedelta(days=period_days)
    
    print("Generating simulated Treasury yield data...")
    
    # Create realistic yield curve data
    np.random.seed(42)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Base yields for normal upward-sloping curve
    base_yields = [2.0, 2.5, 3.2, 3.5]  # 3M, 2Y, 10Y, 30Y
    maturities = [0.25, 2, 10, 30]
    
    yield_curves = {}
    for i, maturity in enumerate(['3M', '2Y', '10Y', '30Y']):
        variations = np.random.normal(0, 0.1, len(dates))
        yields = base_yields[i] + np.cumsum(variations * 0.01)
        yield_curves[maturity] = yields
    
    # Create DataFrame with ONLY the 4 yield columns
    df = pd.DataFrame(yield_curves, index=dates)
    df.index.name = 'Date'
    
    return df, maturities

def calculate_curve_metrics(df):
    """
    Calculate key yield curve metrics
    """
    latest = df.iloc[-1]
    
    metrics = {
        'Curve Slope (10Y-2Y)': latest['10Y'] - latest['2Y'],
        'Curve Steepness (30Y-3M)': latest['30Y'] - latest['3M'],
        'Short Rate': latest['3M'],
        'Long Rate': latest['30Y'],
        'Inversion Check': 'Inverted' if latest['2Y'] > latest['10Y'] else 'Normal'
    }
    
    return metrics

def plot_yield_curve(df, maturities):
    """
    Plot current yield curve and historical trends
    """
    # FIX: Explicitly select the 4 yield columns in the correct order
    yield_columns = ['3M', '2Y', '10Y', '30Y']
    latest_yields = df[yield_columns].iloc[-1].values
    
    # Debug print to verify dimensions
    print(f"Maturities length: {len(maturities)}")
    print(f"Latest yields length: {len(latest_yields)}")
    print(f"Latest yields: {latest_yields}")
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Current yield curve
    ax1.plot(maturities, latest_yields, 'bo-', linewidth=2, markersize=8)
    ax1.set_xlabel('Maturity (Years)')
    ax1.set_ylabel('Yield (%)')
    ax1.set_title(f'US Treasury Yield Curve - {df.index[-1].strftime("%Y-%m-%d")}')
    ax1.grid(True, alpha=0.3)
    ax1.set_xticks(maturities)
    ax1.set_xticklabels(['3M', '2Y', '10Y', '30Y'])
    
    # Add yield values as text on the plot
    for i, (x, y) in enumerate(zip(maturities, latest_yields)):
        ax1.annotate(f'{y:.2f}%', (x, y), textcoords="offset points", 
                    xytext=(0,10), ha='center')
    
    # Historical yield trends
    ax2.plot(df.index, df['3M'], label='3-Month', alpha=0.8)
    ax2.plot(df.index, df['2Y'], label='2-Year', alpha=0.8)
    ax2.plot(df.index, df['10Y'], label='10-Year', alpha=0.8)
    ax2.plot(df.index, df['30Y'], label='30-Year', alpha=0.8)
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Yield (%)')
    ax2.set_title('Historical Treasury Yields')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('yield_curve_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def analyze_inversions(df):
    """
    Detect and analyze yield curve inversions
    """
    # 2Y-10Y spread (most watched indicator)
    df['2Y_10Y_Spread'] = df['10Y'] - df['2Y']
    
    inversions = df[df['2Y_10Y_Spread'] < 0]
    
    print(f"\nInversion Analysis:")
    print(f"Days with 2Y-10Y inversion: {len(inversions)}")
    print(f"Percentage of time inverted: {len(inversions)/len(df)*100:.1f}%")
    
    if len(inversions) > 0:
        print(f"Most recent inversion: {inversions.index[-1].strftime('%Y-%m-%d')}")
        print(f"Deepest inversion: {inversions['2Y_10Y_Spread'].min():.2f}%")
    else:
        print("No inversions detected in the analyzed period.")

def main():
    print("Bond Yield Curve Analyzer")
    print("=" * 40)
    
    # Fetch data
    df, maturities = fetch_treasury_data(period_days=365)
    
    print(f"\nDataFrame shape: {df.shape}")
    print(f"DataFrame columns: {list(df.columns)}")
    
    print(f"\nData Summary:")
    print(f"Date range: {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
    print(f"Total observations: {len(df)}")
    
    # Calculate metrics
    metrics = calculate_curve_metrics(df)
    
    print(f"\nCurrent Yield Curve Metrics:")
    print("-" * 30)
    for metric, value in metrics.items():
        if isinstance(value, (int, float)):
            print(f"{metric}: {value:.2f}%")
        else:
            print(f"{metric}: {value}")
    
    # Analyze inversions
    analyze_inversions(df)
    
    # Create visualizations
    plot_yield_curve(df, maturities)
    
    # Save data (only the 4 yield columns)
    yield_data = df[['3M', '2Y', '10Y', '30Y']]
    yield_data.to_csv('treasury_yields_data.csv')
    print(f"\nData saved to 'treasury_yields_data.csv'")
    print(f"Chart saved to 'yield_curve_analysis.png'")
    
    print(f"\nAnalysis complete! Check your files for detailed results.")

if __name__ == "__main__":
    main()
