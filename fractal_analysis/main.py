import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Headless backend for CI

plt.style.use('dark_background')

def get_data(symbol, period='5y'):
    print(f"🌌 Measuring the roughness of {symbol}...")
    df = yf.download(symbol, period=period, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        close = df['Close'][symbol]
    else:
        close = df['Close']
    return close.values

def get_hurst_exponent(time_series, max_lag=20):
    """Returns the Hurst Exponent of the time series vector ts"""
    lags = range(2, max_lag)
    tau = [np.sqrt(np.std(np.subtract(time_series[lag:], time_series[:-lag]))) for lag in lags]
    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0] * 2

def visualize_fractal(symbol):
    print("🎬 Calculating Fractal Dimension...")
    prices = get_data(symbol)
    
    # Calculate rolling Hurst
    window = 100
    hurst_values = []
    for i in range(window, len(prices)):
        chunk = prices[i-window:i]
        h = get_hurst_exponent(chunk)
        hurst_values.append(h)
        
    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    fig.patch.set_facecolor('black')
    
    ax1.set_facecolor('black')
    ax1.plot(prices[window:], color='cyan', linewidth=1.5, label='Price')
    ax1.set_title(f'{symbol} Price Action', color='white', fontsize=14)
    ax1.grid(color='gray', linestyle=':', alpha=0.3)
    
    ax2.set_facecolor('black')
    
    # Hurst Visualization
    # H < 0.5: Mean Reverting (Rough)
    # H = 0.5: Random Walk (Brownian)
    # H > 0.5: Trending (Persistent)
    
    hurst_series = np.array(hurst_values)
    x_axis = np.arange(len(hurst_series))
    
    # Color code regions
    ax2.fill_between(x_axis, 0.5, hurst_series, where=(hurst_series > 0.5), color='lime', alpha=0.3, label='Trending (Persistent)')
    ax2.fill_between(x_axis, 0.5, hurst_series, where=(hurst_series < 0.5), color='red', alpha=0.3, label='Mean Reverting (Rough)')
    
    ax2.plot(hurst_series, color='white', linewidth=1, alpha=0.8)
    ax2.axhline(0.5, color='yellow', linestyle='--', linewidth=2, label='Random Walk (H=0.5)')
    
    ax2.set_title('Fractal Dimension (Hurst Exponent)', color='white', fontsize=14)
    ax2.set_ylabel('Hurst Exponent', color='white')
    ax2.legend(loc='lower right')
    ax2.grid(color='gray', linestyle=':', alpha=0.3)
    
    filename = 'fractal_hurst.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"Fractal saved to {filename}")
    
    # Narrative
    avg_hurst = np.mean(hurst_series)
    print("\n📜 FRACTAL INSIGHT")
    print(f"Average Hurst: {avg_hurst:.4f}")
    if avg_hurst > 0.5:
        print("Verdict: Market shows persistent trends (Memory).")
    else:
        print("Verdict: Market is mean-reverting (Roughness).")

if __name__ == "__main__":
    visualize_fractal('ETH-USD')
