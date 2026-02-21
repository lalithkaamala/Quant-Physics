import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Polymath Aesthetic
plt.style.use('dark_background')

def heston_model_sim(S0, v0, rho, kappa, theta, sigma, T, N, M):
    """
    Inputs:
     - S0, v0: Initial stock price and variance
     - rho:    Correlation between asset returns and variance
     - kappa:  Rate of mean reversion
     - theta:  Long-run average variance
     - sigma:  Vol of vol
     - T:      Time of simulation
     - N:      Number of time steps
     - M:      Number of simulations
    """
    dt = T/N
    mu = np.array([0,0])
    cov = np.array([[1,rho],
                    [rho,1]])
    
    # Generate correlated Brownian motions
    Z = np.random.multivariate_normal(mu, cov, (M, N))
    
    S = np.full((M, N+1), S0)
    v = np.full((M, N+1), v0)
    
    for t in range(N):
        # Euler-Maruyama discretization
        # Reflecting boundary for variance to keep it positive
        v[:, t+1] = np.abs(v[:, t] + kappa*(theta - v[:, t])*dt + sigma*np.sqrt(v[:, t])*np.sqrt(dt)*Z[:, t, 1])
        S[:, t+1] = S[:, t] * np.exp((0.05 - 0.5*v[:, t])*dt + np.sqrt(v[:, t])*np.sqrt(dt)*Z[:, t, 0])
        
    return S, v

def animate_heston():
    print("🎬 Simulating Stochastic Volatility (Heston Model)...")
    
    # Parameters
    params = {
        'S0': 100, 'v0': 0.04, 'rho': -0.7, 'kappa': 3.0, 
        'theta': 0.04, 'sigma': 0.6, 'T': 1.0, 'N': 100, 'M': 50
    }
    
    S, v = heston_model_sim(**params)
    
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle('Heston Model: The Dance of Price & Volatility', fontsize=18, color='white', fontweight='bold')
    
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Remove panes
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Axis labels
    ax.set_xlabel('Time Steps', color='white')
    ax.set_ylabel('Volatility ($\sqrt{v_t}$)', color='white')
    ax.set_zlabel('Asset Price ($)', color='white')
    
    # Create lines
    lines = [ax.plot([], [], [], alpha=0.5, linewidth=1)[0] for _ in range(params['M'])]
    
    # Set limits
    volatility = np.sqrt(v)
    ax.set_xlim(0, params['N'])
    ax.set_ylim(volatility.min(), volatility.max())
    ax.set_zlim(S.min(), S.max())

    def update(frame):
        # Rotate view for cinematic effect
        ax.view_init(elev=20, azim=frame/2)
        
        current_step = int(frame)
        if current_step > params['N']:
            current_step = params['N']
            
        time_steps = np.arange(current_step + 1)
        
        for i, line in enumerate(lines):
            # X: Time, Y: Volatility, Z: Price
            line.set_data(time_steps, volatility[i, :current_step+1])
            line.set_3d_properties(S[i, :current_step+1])
            
            # Color by volatility intensity
            line.set_color(plt.cm.inferno(volatility[i, current_step] * 2))
            
        return lines

    anim = animation.FuncAnimation(fig, update, frames=np.arange(0, params['N']*1.5, 2), interval=30)
    
    filename = 'heston_3d.gif'
    anim.save(filename, writer='pillow', fps=30)
    print(f"🌪️ Stochastic simulation saved to {filename}")
    
    # Static save
    plt.savefig('heston_static.png', dpi=300)

if __name__ == "__main__":
    animate_heston()
