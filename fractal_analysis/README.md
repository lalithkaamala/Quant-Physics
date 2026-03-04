# The Texture of Time: Fractal Analysis ❄️

> *"How rough is a mountain? How jagged is a price chart?"*

## The Concept
Geometric Brownian Motion assumes markets are "smooth" randomness (Normal distribution). But real markets are rough. The **Hurst Exponent (H)** measures this roughness:
- **H = 0.5**: True Random Walk (Efficient Market).
- **H > 0.5**: Persistent Trend (Memory).
- **H < 0.5**: Mean Reverting (Rough/Choppy).

We calculate the rolling Hurst exponent to visualize the changing "regime" of the market.

## The Visuals
- **`fractal_hurst.png`**: A dual-plot showing price action overlaid with its changing fractal dimension.

## Execute
```bash
python3 main.py
```
