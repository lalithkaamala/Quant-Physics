import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg') # Headless backend for CI
import matplotlib.animation as animation

# Polymath Aesthetic
plt.style.use('dark_background')

def generate_volatility_surface(S, T, base_vol=0.2, skew=0.05, smile=0.1, pulse_factor=0.0):
    """
    Generates a synthetic implied volatility surface with skew and smile.
    pulse_factor: increases the overall volatility level (simulating fear)
    """
    # Create the meshgrid again inside to apply changes
    # But for efficiency we can just operate on arrays
    pass

def animate_volatility_surface():
    print("🎬 Rendering Pulsating Market Heartbeat...")
    
    # Grid
    strikes = np.linspace(80, 120, 40)
    times = np.linspace(0.1, 2.0, 40)
    S, T = np.meshgrid(strikes, times)
    
    fig = plt.figure(figsize=(14, 10))
    fig.suptitle('The Heartbeat of Fear: Implied Volatility Surface', fontsize=18, color='white', fontweight='bold')
    
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    
    # Remove panes
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    
    ax.set_xlabel('Strike Price ($)', color='white')
    ax.set_ylabel('Time to Expiry (Years)', color='white')
    ax.set_zlabel('Implied Volatility (%)', color='white')
    
    # Initial plot
    ax.plot_surface(S, T, np.zeros_like(S), cmap='magma', edgecolor='none', alpha=0.8)
    
    def update(frame):
        ax.clear()
        
        # Reset axes properties after clear
        ax.set_facecolor('black')
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        ax.set_xlabel('Strike Price ($)', color='white')
        ax.set_ylabel('Time to Expiry (Years)', color='white')
        ax.set_zlabel('Implied Volatility (%)', color='white')
        ax.set_zlim(0.1, 0.7) # Fixed Z-limit to prevent jumping
        
        # Pulsating effect: Sine wave breathing
        # Breath cycle: simple harmonic motion
        pulse = np.sin(frame * 0.1) * 0.05 + 0.02 
        
        # Recalculate Surface
        moneyness = (S - 100) / 100
        current_base_vol = 0.2 + pulse
        current_skew = -0.5 * (1 + pulse*5) 
        
        iv_surface = current_base_vol + current_skew * moneyness + 2.0 * (moneyness**2)
        
        # Plot
        surf = ax.plot_surface(S, T, iv_surface, cmap='magma', vmin=0.1, vmax=0.6, edgecolor='cyan', linewidth=0.2, alpha=0.85)
        
        # View rotation
        ax.view_init(elev=30 + 5*np.sin(frame*0.05), azim=frame*0.5)
        
        return surf,

    anim = animation.FuncAnimation(fig, update, frames=np.arange(0, 200, 1), interval=40)
    
    filename = 'volatility_surface.gif'
    anim.save(filename, writer='pillow', fps=24)
    print(f"💓 Heartbeat saved to {filename}")
    plt.savefig('volatility_static.png', dpi=300)

if __name__ == "__main__":
    animate_volatility_surface()
