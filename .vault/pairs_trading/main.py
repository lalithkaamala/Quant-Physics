import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Headless backend for CI
import matplotlib.animation as animation
from statsmodels.tsa.stattools import coint

plt.style.use('dark_background')

def get_data(tickers, start='2023-01-01'):
    print(f"⚖️ Analyzing spread between {tickers[0]} and {tickers[1]}...")
    data = yf.download(tickers, start=start)['Close']
    return data

def find_cointegration(data):
    # Engle-Granger Test
    score, pvalue, _ = coint(data.iloc[:,0], data.iloc[:,1])
    return pvalue

def visualize_pairs(asset1='KO', asset2='PEP'):
    print("🎬 Generating Pairs Trading Signal...")
    
    df = get_data([asset1, asset2])
    
    # Calculate Spread ratio
    # Simple linear regression for hedge ratio usually, here simplified for visual
    S1 = df[asset1]
    S2 = df[asset2]
    score = find_cointegration(df)
    
    ratio = S1 / S2
    # Z-Score of the ratio
    zscore = (ratio - ratio.mean()) / ratio.std()
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    fig.patch.set_facecolor('black')
    
    # Top: Normalized Prices
    ax1.set_facecolor('black')
    ax1.plot(S1/S1.iloc[0], color='cyan', label=asset1)
    ax1.plot(S2/S2.iloc[0], color='orange', label=asset2)
    ax1.set_title(f'Pairs Trading: {asset1} vs {asset2} (Coint p-value: {score:.4f})', color='white', fontsize=14)
    ax1.legend()
    ax1.grid(color='gray', linestyle=':', alpha=0.3)
    
    # Bottom: Z-Score Spread
    ax2.set_facecolor('black')
    ax2.set_title('Spread Z-Score (Mean Reversion Signal)', color='white')
    ax2.axhline(0, color='white', linestyle='--')
    ax2.axhline(2.0, color='red', linestyle='--', alpha=0.5, label='Sell Threshold (+2)')
    ax2.axhline(-2.0, color='green', linestyle='--', alpha=0.5, label='Buy Threshold (-2)')
    ax2.legend()
    
    line_z, = ax2.plot([], [], color='magenta', linewidth=1.5)
    
    def update(frame):
        current_idx = int(frame)
        if current_idx >= len(zscore):
            current_idx = len(zscore) - 1
            
        data = zscore.iloc[:current_idx]
        line_z.set_data(data.index, data.values)
        
        # Color the line logic impossible with single line object efficiently in matplotlib animation
        # simplified to just drawing the path
        
        return line_z,

    frames = np.linspace(0, len(zscore), 100)
    anim = animation.FuncAnimation(fig, update, frames=frames, interval=30)
    
    filename = 'pairs_trading.gif'
    anim.save(filename, writer='pillow', fps=30)
    print(f"⚖️ Arbitrage opportunity saved to {filename}")
    plt.savefig('pairs_static.png', dpi=300)

if __name__ == "__main__":
    visualize_pairs('KO', 'PEP') # Classic pair
