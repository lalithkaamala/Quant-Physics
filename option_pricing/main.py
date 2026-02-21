import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Headless backend for CI
from scipy.stats import norm

# Apply "Polymath" dark aesthetic
plt.style.use('dark_background')

class BlackScholes:
    """
    The Black-Scholes model: A mathematical model for the dynamics of a financial market.
    It estimates the theoretical value of options.
    """
    def __init__(self, S, K, T, r, sigma):
        self.S = S      # Spot price
        self.K = K      # Strike price
        self.T = T      # Time to maturity (years)
        self.r = r      # Risk-free interest rate
        self.sigma = sigma  # Volatility

    def d1(self):
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def d2(self):
        return self.d1() - self.sigma * np.sqrt(self.T)

    def call_price(self):
        return self.S * norm.cdf(self.d1()) - self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2())

    def put_price(self):
        return self.K * np.exp(-self.r * self.T) * norm.cdf(-self.d2()) - self.S * norm.cdf(-self.d1())

    # --- THE GREEKS ---
    # Delta: Sensitivity to Spot Price
    def delta_call(self):
        return norm.cdf(self.d1())

    # Gamma: Sensitivity to Delta (Convexity)
    def gamma(self):
        return norm.pdf(self.d1()) / (self.S * self.sigma * np.sqrt(self.T))

    # Theta: Sensitivity to Time Decay
    def theta_call(self):
        term1 = -(self.S * norm.pdf(self.d1()) * self.sigma) / (2 * np.sqrt(self.T))
        term2 = -self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(self.d2())
        return term1 + term2

    # Vega: Sensitivity to Volatility
    def vega(self):
        return self.S * norm.pdf(self.d1()) * np.sqrt(self.T)

def visualize_greeks_surface():
    """
    Visualizes the Option "Greeks" as a 3D surface to show the multi-dimensional nature of risk.
    """
    S = np.linspace(50, 150, 50)  # Spot Price Range
    T = np.linspace(0.1, 2.0, 50) # Time to Expiry Range
    S, T = np.meshgrid(S, T)

    # Fixed parameters
    K = 100
    r = 0.05
    sigma = 0.2

    # Vectorized calculation manually for grid
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    fig = plt.figure(figsize=(16, 12))
    
    # Custom "Polymath" title
    fig.suptitle('The Geometry of Risk: Gamma Surface', fontsize=20, color='white', fontweight='bold', y=0.95)
    
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(S, T, gamma, cmap='inferno', edgecolor='none', alpha=0.9)
    
    ax.set_xlabel('Spot Price ($)', fontsize=12, labelpad=10)
    ax.set_ylabel('Time to Expiry (Years)', fontsize=12, labelpad=10)
    ax.set_zlabel('Gamma (Convexity)', fontsize=12, labelpad=10)
    
    # Stylized view angle
    ax.view_init(elev=30, azim=225)
    
    # Remove pane backgrounds for sleek look
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    fig.colorbar(surf, shrink=0.5, aspect=10, label='Gamma Intensity')

    # Narrative Annotation
    ax.text2D(0.05, 0.9, "Insight: Gamma peaks when the option is 'At-The-Money' and nearing expiry.\nThis is where hedging becomes most volatile.", transform=ax.transAxes, color='cyan', fontsize=12)

    output_path = 'option_greeks_surface.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"🌌 3D Surface saved to {output_path}")

def animate_greeks_cinema():
    """
    Creates a cinematic rotating animation of the Gamma Surface.
    """
    import matplotlib.animation as animation
    
    print("🎬 Lights, Camera, Action! Rendering 3D Animation...")
    
    S = np.linspace(50, 150, 50)
    T = np.linspace(0.1, 2.0, 50)
    S, T = np.meshgrid(S, T)

    K = 100
    r = 0.05
    sigma = 0.2

    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    fig = plt.figure(figsize=(16, 9)) # 16:9 Cinematic Aspect Ratio
    fig.suptitle('The Geometry of Risk: Gamma Surface', fontsize=24, color='white', fontweight='bold', y=0.92)
    
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(S, T, gamma, cmap='inferno', edgecolor='none', alpha=0.9)
    
    ax.set_xlabel('Spot Price ($)', fontsize=12, labelpad=10)
    ax.set_ylabel('Time to Expiry (Years)', fontsize=12, labelpad=10)
    ax.set_zlabel('Gamma (Convexity)', fontsize=12, labelpad=10)
    
    # Remove pane backgrounds
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    # Set initial view
    ax.view_init(elev=30, azim=0)
    
    def update(frame):
        # Rotate the azimuth angle
        ax.view_init(elev=30, azim=frame)
        return fig,

    # Create animation (360 frames for a full rotation)
    anim = animation.FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=50)
    
    output_file = 'gamma_surface_cinematic.gif'
    anim.save(output_file, writer='pillow', fps=30)
    print(f"📽️ Scene wrapped! Animation saved to {output_file}")

if __name__ == "__main__":
    print("🔮 Calculating The Greeks...")
    
    # Single Option Calculation
    bs = BlackScholes(S=100, K=100, T=1, r=0.05, sigma=0.2)
    
    # Run the cinematic animation
    animate_greeks_cinema()
