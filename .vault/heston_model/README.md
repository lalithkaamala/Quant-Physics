# The Volatility Storm: Heston Model 🌪️

> *"Volatility is not a constant; it is a living, breathing beast."*

## The Concept
The Black-Scholes model assumes volatility is constant. The **Heston Model** assumes volatility itself is random (Stochastic). It models two correlated processes: the asset price and its variance. This allows us to simulate "fat tails" and market crashes that standard models miss.

## The Visuals
- **`heston_3d.gif`**: A 3D particle simulation where the Z-axis is price, Y-axis is volatility, and X-axis is time. Watch how high volatility creates "storms" of price movement.
- **`heston_static.png`**: A static render of the stochastic paths.

## Execute
```bash
python3 main.py
```
