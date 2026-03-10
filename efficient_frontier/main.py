import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.style.use('dark_background')

def get_data(stocks, period='2y'):
    print(f"💼 optimizing portfolio: {', '.join(stocks)}...")
    data = yf.download(stocks, period=period)['Close']
    return data.pct_change()

def visualize_efficient_frontier():
    print("🎬 Generating Efficient Frontier Cinema...")
    
    stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']
    returns = get_data(stocks)
    mean_returns = returns.mean()
    cov_matrix = returns.cov()
    num_portfolios = 2000
    risk_free_rate = 0.04
    
    # Arrays to store data
    results = np.zeros((3, num_portfolios))
    
    for i in range(num_portfolios):
        weights = np.random.random(len(stocks))
        weights /= np.sum(weights)
        
        portfolio_return = np.sum(mean_returns * weights) * 252
        portfolio_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
        
        results[0,i] = portfolio_std_dev
        results[1,i] = portfolio_return
        results[2,i] = (portfolio_return - risk_free_rate) / portfolio_std_dev # Sharpe Ratio

    # Animation
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    ax.set_xlabel('Volatility (Std. Deviation)', color='white')
    ax.set_ylabel('Expected Return', color='white')
    ax.set_title('The Efficient Frontier: Searching for Alpha', fontsize=18, color='white', fontweight='bold')
    ax.grid(color='gray', linestyle=':', alpha=0.3)
    
    scat = ax.scatter([], [], c=[], cmap='viridis', alpha=0.7, s=20)
    cb = plt.colorbar(scat)
    cb.set_label('Sharpe Ratio (Risk-Adjusted Return)', color='white')
    cb.ax.yaxis.set_tick_params(color='white')
    plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color='white')
    
    ax.set_xlim(results[0].min() * 0.9, results[0].max() * 1.1)
    ax.set_ylim(results[1].min() * 0.9, results[1].max() * 1.1)
    
    def update(frame):
        # Gradually reveal portfolios
        current_count = int(frame)
        if current_count > num_portfolios:
            current_count = num_portfolios
            
        x = results[0, :current_count]
        y = results[1, :current_count]
        c = results[2, :current_count]
        
        scat.set_offsets(np.c_[x, y])
        scat.set_array(c)
        
        # Highlight Max Sharpe on the fly
        if current_count > 10:
            max_sharpe_idx = np.argmax(c)
            ax.plot(x[max_sharpe_idx], y[max_sharpe_idx], 'r*', markersize=15, markeredgecolor='white')
            
        return scat,

    frames = np.linspace(10, num_portfolios, 100)
    anim = animation.FuncAnimation(fig, update, frames=frames, interval=30)
    
    filename = 'efficient_frontier.gif'
    anim.save(filename, writer='pillow', fps=30)
    print(f"🏹 Frontier saved to {filename}")
    plt.savefig('frontier_static.png', dpi=300)

if __name__ == "__main__":
    visualize_efficient_frontier()
