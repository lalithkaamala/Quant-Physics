import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# Apply a "Cyberpunk/Polymath" aesthetic
plt.style.use('dark_background')

def get_data(stocks, start, end):
    print(f"🔍 Analyzing historical data for: {', '.join(stocks)}...")
    stockData = yf.download(stocks, start=start, end=end, progress=False)
    stockData = stockData['Close']
    returns = stockData.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()
    return meanReturns, covMatrix

def run_simulation(stocks, start, end, days=365, simulations=2000, initial_portfolio=10000):
    weights = np.random.random(len(stocks))
    weights /= np.sum(weights)

    meanReturns, covMatrix = get_data(stocks, start, end)

    meanM = np.full(shape=(days, len(weights)), fill_value=meanReturns)
    meanM = meanM.T

    portfolio_sims = np.full(shape=(days, simulations), fill_value=0.0)

    print(f"🔮 Simulating {simulations} potential futures over the next {days} days...")
    
    for m in range(0, simulations):
        Z = np.random.normal(size=(days, len(weights)))
        L = np.linalg.cholesky(covMatrix)
        dailyReturns = meanM + np.inner(L, Z)
        portfolio_sims[:, m] = np.cumprod(np.inner(weights, dailyReturns.T) + 1) * initial_portfolio

    return portfolio_sims

if __name__ == "__main__":
    stocks = ['NVDA', 'TSLA', 'PLTR'] # High volatility tech stocks for better visualization
    end = dt.datetime.now()
    start = end - dt.timedelta(days=365)
    
    initial_value = 10000
    portfolio_sims = run_simulation(stocks, start, end, initial_portfolio=initial_value)

    # Visualization with "Polymath" touch
    plt.figure(figsize=(14, 8))
    
    # Custom colormap for lines (fade from blue to magenta)
    colors = plt.cm.plasma(np.linspace(0, 1, portfolio_sims.shape[1]))
    
    # Plot all simulations with transparency
    for i in range(portfolio_sims.shape[1]):
        plt.plot(portfolio_sims[:, i], color=colors[i], alpha=0.15, linewidth=1)

    # Plot the MEAN outcome
    plt.plot(portfolio_sims.mean(axis=1), color='cyan', linewidth=3, label='Mean Trajectory')
    
    # Plot Confidence Intervals
    upper_bound = np.percentile(portfolio_sims, 95, axis=1)
    lower_bound = np.percentile(portfolio_sims, 5, axis=1)
    
    plt.plot(upper_bound, color='lime', linestyle='--', linewidth=2, label='95% Optimistic')
    plt.plot(lower_bound, color='red', linestyle='--', linewidth=2, label='5% Pessimistic')

    plt.ylabel('Portfolio Value ($)', fontsize=12, color='white')
    plt.xlabel('Days into the Future', fontsize=12, color='white')
    plt.title('The Probabilistic Future: A Monte Carlo Study', fontsize=18, color='white', fontweight='bold')
    plt.legend(loc='upper left', frameon=False)
    plt.grid(color='gray', linestyle=':', alpha=0.5)
    
    # Save high-res plot
    output_path = 'monte_carlo_polymath.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n🎨 Masterpiece saved to {output_path}")

def animate_simulation_cinema(portfolio_sims):
    """
    Creates a time-lapse animation of the Monte Carlo simulation.
    """
    import matplotlib.animation as animation
    
    print("🎬 Rendering Monte Carlo Time-Lapse...")
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Setup the plot
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.set_ylabel('Portfolio Value ($)', fontsize=12, color='white')
    ax.set_xlabel('Days into the Future', fontsize=12, color='white')
    ax.set_title('The Probabilistic Future: A Monte Carlo Study', fontsize=18, color='white', fontweight='bold')
    ax.grid(color='gray', linestyle=':', alpha=0.5)
    
    # Initial empty lines
    lines = []
    colors = plt.cm.plasma(np.linspace(0, 1, portfolio_sims.shape[1]))
    
    # We will animate 50 lines only for performance in the GIF to keep file size reasonable
    num_lines_to_animate = 50
    sims_to_animate = portfolio_sims[:, :num_lines_to_animate]
    colors = colors[:num_lines_to_animate]
    
    for i in range(num_lines_to_animate):
        line, = ax.plot([], [], color=colors[i], alpha=0.6, linewidth=1.5)
        lines.append(line)
        
    mean_line, = ax.plot([], [], color='cyan', linewidth=3, label='Mean Trajectory')
    
    # Set axis limits
    ax.set_xlim(0, len(portfolio_sims))
    ax.set_ylim(np.min(portfolio_sims), np.max(portfolio_sims))
    
    def init():
        for line in lines:
            line.set_data([], [])
        mean_line.set_data([], [])
        return lines + [mean_line]
    
    def update(frame):
        # Frame goes from 0 to days (365)
        # We step by 5 days per frame to speed up
        current_day = frame * 5
        if current_day > len(portfolio_sims):
            current_day = len(portfolio_sims)
            
        x_data = np.arange(current_day)
        
        for i, line in enumerate(lines):
            line.set_data(x_data, sims_to_animate[:current_day, i])
            
        mean_data = portfolio_sims[:current_day, :].mean(axis=1)
        mean_line.set_data(x_data, mean_data)
        
        return lines + [mean_line]

    frames = len(portfolio_sims) // 5
    anim = animation.FuncAnimation(fig, update, init_func=init, frames=frames, interval=30, blit=True)
    
    output_file = 'monte_carlo_cinematic.gif'
    anim.save(output_file, writer='pillow', fps=30)
    print(f"📽️ Scene wrapped! Animation saved to {output_file}")


if __name__ == "__main__":
    stocks = ['NVDA', 'TSLA', 'PLTR'] # High volatility tech stocks for better visualization
    end = dt.datetime.now()
    start = end - dt.timedelta(days=365)
    
    initial_value = 10000
    portfolio_sims = run_simulation(stocks, start, end, initial_portfolio=initial_value)

    # Narrative Output (Pre-animation)
    final_values = portfolio_sims[-1, :]
    expected_value = final_values.mean()
    print(f"Expected Wealth: ${expected_value:,.2f}")
    
    # Run Animation
    animate_simulation_cinema(portfolio_sims)
