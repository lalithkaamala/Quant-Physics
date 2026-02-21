# Experiments in Financial Physics 🌌

> *"Randomness is not chaos; it has a shape."*

This repository is a collection of experiments at the intersection of quantitative finance, mathematics, and visual storytelling. It is an attempt to see the market not just as numbers, but as a complex system governed by beautiful laws.

## The Archives

### 1. The Probabilistic Future: Monte Carlo Simulations
Located in: `monte_carlo/`

**Concept**:
We cannot predict the future, but we can map the probability of all possible futures. Using the **Geometric Brownian Motion** model, we simulate thousands of potential price paths to understand the shape of risk and reward.

**The Output**:
- A static visualization (`monte_carlo_polymath.png`) of the "cone of uncertainty".
- **A Cinematic Animation** (`monte_carlo_cinematic.gif`) showing the simulation paths growing over time, visually demonstrating the accumulation of variance.

**Execute**:
```bash
python3 monte_carlo/main.py
```

---

### 2. The Geometry of Risk: Black-Scholes 3D
Located in: `option_pricing/`

**Concept**:
An option's value is derived from the underlying asset, time, and volatility. This relationship forms a multi-dimensional surface. The **Black-Scholes Model** is the differential equation that describes this surface.

**The Output**:
- A static visualization (`option_greeks_surface.png`) of the Gamma risk surface.
- **A Cinematic Animation** (`gamma_surface_cinematic.gif`) that rotates around the risk surface, revealing its complex geometry from every angle.

**Execute**:
```bash
python3 option_pricing/main.py
```

## 🤖 Automaton
This repository is alive. A **GitHub Action** (`.github/workflows/daily_quant_update.yml`) wakes up every weekday at 23:00 UTC to:
1.  Fetch the latest market data.
2.  Run the Monte Carlo simulations.
3.  Recalculate the Option Greeks.
4.  **Auto-commit** the fresh visualizations back to this repo.

It is a self-updating journal of financial probability.

## Tools of the Trade
- `numpy`: The bedrock of computation.
- `matplotlib` & `scipy`: For visualizing the unseen.
- `yfinance`: The connection to the living market.

## Installation
```bash
pip install -r requirements.txt
```
