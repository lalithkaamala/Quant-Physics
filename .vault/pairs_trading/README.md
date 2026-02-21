# The Arbitrage Radar: Pairs Trading ⚖️

> *"History doesn't repeat, but it rhymes."*

## The Concept
**Statistical Arbitrage**. We find two assets that are "cointegrated" (tied together by economic forces, like Coke and Pepsi). When they drift apart, we short the winner and buy the loser, betting they will snap back. The **Z-Score** of the spread tells us when to pull the trigger.

## The Visuals
- **`pairs_trading.gif`**: An oscilloscope view of the spread. As the line crosses the red/green thresholds, it signals a trade opportunity.
- **`pairs_static.png`**: The historical performance of the pair.

## Execute
```bash
python3 main.py
```
