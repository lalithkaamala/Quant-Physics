import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Polymath Aesthetic
plt.style.use('dark_background')

def get_data(symbol, period='2y'):
    print(f"🔮 Analyzing market cycles for {symbol}...")
    df = yf.download(symbol, period=period, progress=False)
    # Ensure we're working with a Series, handling multi-level columns if present
    if isinstance(df.columns, pd.MultiIndex):
        close = df['Close'][symbol]
    else:
        close = df['Close']
    return close

def calculate_bollinger_bands(series, window=20, num_std=2):
    rolling_mean = series.rolling(window=window).mean()
    rolling_std = series.rolling(window=window).std()
    upper_band = rolling_mean + (rolling_std * num_std)
    lower_band = rolling_mean - (rolling_std * num_std)
    return rolling_mean, upper_band, lower_band

def animate_strategy(symbol):
    print("🎬 Rendering Mean Reversion Cinema...")
    
    price_data = get_data(symbol)
    rolling_mean, upper_band, lower_band = calculate_bollinger_bands(price_data)
    
    # Align data
    data = pd.DataFrame({
        'Price': price_data,
        'Mean': rolling_mean,
        'Upper': upper_band,
        'Lower': lower_band
    }).dropna()
    
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    ax.set_title(f'Mean Reversion: The Elasticity of Price ({symbol})', fontsize=18, color='white', fontweight='bold')
    ax.set_ylabel('Price ($)', fontsize=12, color='white')
    ax.grid(color='gray', linestyle=':', alpha=0.3)
    
    # Plot elements
    line_price, = ax.plot([], [], color='cyan', linewidth=1.5, label='Price')
    line_mean, = ax.plot([], [], color='white', linestyle='--', alpha=0.5, label='Moving Average')
    line_upper, = ax.plot([], [], color='red', alpha=0.3)
    line_lower, = ax.plot([], [], color='green', alpha=0.3)
    ax.fill_between([], [], [], color='gray', alpha=0.1)

    ax.legend(loc='upper left', frameon=False, labelcolor='white')
    
    # Set limits
    ax.set_xlim(data.index[0], data.index[-1])
    ax.set_ylim(data['Lower'].min() * 0.95, data['Upper'].max() * 1.05)
    
    def init():
        line_price.set_data([], [])
        line_mean.set_data([], [])
        line_upper.set_data([], [])
        line_lower.set_data([], [])
        return line_price, line_mean, line_upper, line_lower
        
    def update(frame):
        # Animate in chunks to speed up
        current_idx = frame * 5
        if current_idx >= len(data):
            current_idx = len(data) - 1
            
        subset = data.iloc[:current_idx]
        
        # Redraw
        line_price.set_data(subset.index, subset['Price'])
        line_mean.set_data(subset.index, subset['Mean'])
        line_upper.set_data(subset.index, subset['Upper'])
        line_lower.set_data(subset.index, subset['Lower'])
        
        # Remove old fill
        for collection in ax.collections:
            collection.remove()
            
        # Add new fill
        ax.fill_between(subset.index, subset['Upper'], subset['Lower'], color='purple', alpha=0.15)
        
        return line_price, line_mean, line_upper, line_lower

    frames = len(data) // 5
    anim = animation.FuncAnimation(fig, update, init_func=init, frames=frames, interval=30, blit=False)
    
    output_file = 'mean_reversion.gif'
    anim.save(output_file, writer='pillow', fps=30)
    print(f"📼 Visualization archived to {output_file}")
    
    # Save static image too
    plt.savefig('mean_reversion_static.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    animate_strategy('BTC-USD') # Crypto implies higher volatility, better for mean reversion visuals
