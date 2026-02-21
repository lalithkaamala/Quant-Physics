import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft

plt.style.use('dark_background')

def get_data(symbol, period='1y'):
    print(f"🎼 Listening to the market rhythm of {symbol}...")
    df = yf.download(symbol, period=period, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        close = df['Close'][symbol]
    else:
        close = df['Close']
    return close.values

def animate_fourier(symbol):
    print("🎬 Decomposing Market Frequencies...")
    
    prices = get_data(symbol)
    N = len(prices)
    
    # Detrend data for FFT
    linear_trend = np.polyfit(np.arange(N), prices, 1)
    trend_line = np.polyval(linear_trend, np.arange(N))
    detrended = prices - trend_line
    
    # FFT
    fft_coeffs = fft(detrended)
    
    # Reconstruct with gradually more components
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    fig.patch.set_facecolor('black')
    
    # Top Plot: Price & Reconstruction
    ax1.set_facecolor('black')
    ax1.set_title('Signal Reconstruction', fontsize=14, color='white')
    ax1.plot(prices, color='gray', alpha=0.5, label='Original Price')
    line_recon, = ax1.plot([], [], color='cyan', linewidth=2, label='Fourier Approximation')
    ax1.legend()
    
    # Bottom Plot: Frequency Spectrum
    ax2.set_facecolor('black')
    ax2.set_title('Dominant Frequencies', fontsize=14, color='white')
    freqs = np.fft.fftfreq(N)
    magnitudes = np.abs(fft_coeffs)
    ax2.stem(freqs[:N//2], magnitudes[:N//2], linefmt='lime', markerfmt='go', basefmt=" ")
    
    def update(frame):
        # Use top 'frame' components
        num_components = int(frame) + 1
        
        # Filter coeffs
        coeffs_filtered = np.copy(fft_coeffs)
        # Keep only indices of top magnitude components
        # Sort by magnitude
        indices = np.argsort(np.abs(fft_coeffs))[::-1]
        
        # Create a mask of zeros
        mask = np.zeros(N, dtype=bool)
        # Set top 'num_components' to True
        mask[indices[:num_components]] = True
        
        # Zero out weak frequencies
        coeffs_filtered[~mask] = 0
        
        reconstructed = ifft(coeffs_filtered).real + trend_line
        
        line_recon.set_data(np.arange(N), reconstructed)
        ax1.set_title(f'Reconstruction using Top {num_components} Frequencies', color='white')
        
        return line_recon,

    import matplotlib.animation as animation
    # Animate up to 50 components
    anim = animation.FuncAnimation(fig, update, frames=np.linspace(1, 50, 100), interval=50)
    
    output_file = 'fourier_cycles.gif'
    anim.save(output_file, writer='pillow', fps=20)
    print(f"🎹 Symphony saved to {output_file}")
    plt.savefig('fourier_static.png', dpi=300)

if __name__ == "__main__":
    animate_fourier('SPY')
