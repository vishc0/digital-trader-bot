# Candlesticks Masterclass

[Training Hub](../README.md) | [Section Index](./README.md) | [Technical Deep Dive](../02_Technical_Deep_Dive/README.md)

A comprehensive training foundation for reading, interpreting, and trading candlesticks as a professional trader and educator.

---

## Table of Contents

1. [Why Candlesticks Matter](#why-candlesticks-matter)
2. [Candlestick Anatomy: The Non-Negotiable Basics](#candlestick-anatomy-the-non-negotiable-basics)
3. [Five Conceptual Lenses to Understand Candlesticks](#five-conceptual-lenses-to-understand-candlesticks)
4. [Core Single-Candle Signals](#core-single-candle-signals)
5. [Core Multi-Candle Patterns](#core-multi-candle-patterns)
6. [Advanced Pattern Families and Narrative Logic](#advanced-pattern-families-and-narrative-logic)
7. [Context Hierarchy: When a Pattern Matters (or Fails)](#context-hierarchy-when-a-pattern-matters-or-fails)
8. [Detailed Scenarios with Trade Logic](#detailed-scenarios-with-trade-logic)
9. [Entry, Stop, Target Frameworks from Candlestick Structure](#entry-stop-target-frameworks-from-candlestick-structure)
10. [Multi-Timeframe Candlestick Reading](#multi-timeframe-candlestick-reading)
11. [Volume + Volatility + Session Context](#volume--volatility--session-context)
12. [Related Training Modules](#related-training-modules)
13. [Common Mistakes and Misconceptions](#common-mistakes-and-misconceptions)
14. [Professional Candlestick Checklist](#professional-candlestick-checklist)
15. [Practice Curriculum (Training Path)](#practice-curriculum-training-path)
16. [Glossary](#glossary)

---

## Why Candlesticks Matter

Candlesticks are not magic shapes; they are compressed stories of **auction behavior**:

- Open: where value began for that period.
- High/Low: the extremes where one side temporarily overpowered the other.
- Close: where the market agreed to end that period.

A candlestick chart helps you answer:

1. Who had control (buyers/sellers)?
2. Did that control persist or get rejected?
3. Is momentum accelerating, stalling, or reversing?
4. Is this move likely continuation or exhaustion?

As an expert mindset: candlesticks are evidence, not certainty.

---

## Candlestick Anatomy: The Non-Negotiable Basics

Each candle has:

- **Body**: distance from open to close.
- **Upper wick**: high minus max(open, close).
- **Lower wick**: min(open, close) minus low.
- **Range**: high minus low.

### Practical Interpretation

- Large body + small wicks = directional conviction.
- Small body + large wicks = disagreement/indecision.
- Long upper wick = higher prices rejected.
- Long lower wick = lower prices rejected.

### Quantitative Lens

For systematic interpretation, convert candle parts to ratios:

- Body ratio = `abs(close - open) / (high - low)`
- Upper wick ratio = `(high - max(open, close)) / (high - low)`
- Lower wick ratio = `(min(open, close) - low) / (high - low)`

These ratios standardize interpretation across symbols/timeframes.

---

## Five Conceptual Lenses to Understand Candlesticks

### 1) Structure Lens (Geometry of Price)

Focus on shape only:

- Is body dominant?
- Which wick dominates?
- Is candle expanding or contracting relative to recent candles?

**Use case:** Quick triage of momentum vs rejection.

---

### 2) Psychology Lens (Battle Narrative)

Translate shape into behavior:

- Strong bullish candle: buyers accepted higher prices.
- Shooting star after rally: buyers pushed up, then got absorbed/rejected by sellers.
- Doji at key resistance: neither side willing to commit beyond level.

**Use case:** Trade planning and post-trade review.

---

### 3) Context Lens (Location > Shape)

A bullish hammer at support after a selloff means more than the same hammer in the middle of a range.

Context priority:

1. Market structure (trend/range)
2. Key levels (support/resistance, prior high/low)
3. Volatility regime
4. Session timing/news
5. Pattern shape

**Use case:** Avoid false confidence from isolated patterns.

---

### 4) Probability Lens (Evidence Stacking)

A pattern alone has weak edge. Combine with confluence:

- Trend alignment
- Level interaction
- Volume confirmation
- Momentum divergence/continuation
- Risk/reward feasibility

Think in terms of expected value, not “right/wrong prediction.”

---

### 5) Execution Lens (What Will You Actually Do?)

Every pattern must map to a full plan:

- Trigger
- Invalidity
- Stop placement
- Position size
- Target logic
- Management rule

If the pattern cannot produce clear invalidation, skip it.

---

## Core Single-Candle Signals

### 1) Marubozu (Strong Conviction Candle)

**Definition:** Long body, tiny or no wicks.

- Bullish marubozu: persistent buying pressure.
- Bearish marubozu: persistent selling pressure.

**Interpretation:** Momentum likely continues short-term, unless it slams into major level/news shock.

**Example Scenario:**

- 15m chart, breakout above prior day high with bullish marubozu + high volume.
- Plan: continuation entry on small pullback, stop below marubozu midpoint/low depending risk profile.

---

### 2) Doji (Indecision/Balance)

**Definition:** Open and close near equal.

Types: standard, long-legged, dragonfly, gravestone.

**Interpretation:** Pause in conviction. Signal quality increases at important levels.

**Example Scenario:**

- Uptrend reaches weekly resistance, prints gravestone doji.
- Next candle closes bearish below doji low.
- Plan: tactical short retracement trade to nearest demand zone.

---

### 3) Hammer / Hanging Man

Same shape, different location.

- **Hammer** (after decline): potential bullish reversal.
- **Hanging Man** (after rise): potential bearish warning.

**Key idea:** Long lower wick = strong rejection of lower prices.

**Confirmation rule:** Wait for next candle close above hammer high (bullish) or below hanging man low (bearish context).

---

### 4) Shooting Star / Inverted Hammer

Same geometry, different context.

- **Shooting star** after rally: bearish rejection.
- **Inverted hammer** after decline: potential bullish reversal (needs confirmation).

**Key idea:** Buyers achieved extension but failed to hold it.

---

## Core Multi-Candle Patterns

### 1) Engulfing Pattern

- **Bullish engulfing:** second candle body fully engulfs prior bearish body.
- **Bearish engulfing:** second candle body fully engulfs prior bullish body.

**Best context:** At key levels, after an extended directional move.

**Scenario:**

- Price drops into daily support.
- First candle small bearish, second large bullish engulfing with volume spike.
- Entry: break of engulfing high.
- Stop: below engulfing low.
- Target: prior swing high / 2R-3R.

---

### 2) Harami (Inside Body Reversal/Pause)

Small second body contained within previous large body.

- Bullish harami after down move: selling pressure is slowing.
- Bearish harami after up move: buying pressure is slowing.

**Interpretation:** Transition, not instant reversal certainty.

---

### 3) Piercing Pattern / Dark Cloud Cover

- **Piercing:** bullish two-candle reversal after decline; second candle closes deep into prior bearish body.
- **Dark cloud cover:** bearish counterpart after rise.

**Use:** Stronger in trending pullbacks than in noisy ranges.

---

### 4) Morning Star / Evening Star

Three-candle reversal structures:

- Morning star: bearish candle -> indecision/small candle -> strong bullish candle.
- Evening star: bullish candle -> indecision/small candle -> strong bearish candle.

**Interpretation:** Control transfer from one side to the other.

---

### 5) Three White Soldiers / Three Black Crows

- Three white soldiers: 3 strong bullish candles after decline or base.
- Three black crows: 3 strong bearish candles after rally.

**Warning:** Late-stage appearance can also signal blow-off/exhaustion.

---

## Advanced Pattern Families and Narrative Logic

### A) Compression to Expansion

- Sequence of small candles/inside bars indicates reduced volatility.
- Breakout candle with range expansion reveals directional intent.

**Educational framing:** Market stores energy during compression; release often produces impulse.

---

### B) Exhaustion Spike then Failure

- One large directional candle extends too far from mean/structure.
- Follow-up candles fail to continue and start reclaiming prior range.

**Interpretation:** Trapped breakout participants fuel reversal.

---

### C) Wick Clusters at Levels

Multiple candles showing repeated upper-wick rejection at resistance (or lower-wick rejection at support).

**Interpretation:** Passive limit orders absorbing aggressive order flow.

---

### D) Break-and-Retest Candlestick Logic

1. Candle closes beyond major level.
2. Pullback candles show reduced momentum.
3. Rejection candle at retest triggers continuation.

This is one of the cleanest institutional-style candlestick workflows.

---

## Context Hierarchy: When a Pattern Matters (or Fails)

Use this hierarchy before acting:

1. **Regime:** trend, range, or transition?
2. **Location:** at meaningful level or random mid-range?
3. **Timing:** normal session liquidity vs thin session?
4. **Catalyst:** major news nearby?
5. **Pattern quality:** clean or messy?

A perfect pattern in poor context is usually a poor trade.

---

## Detailed Scenarios with Trade Logic

### Scenario 1: Hammer at Daily Support in Uptrend Pullback

**Context**

- Daily trend up (higher highs/higher lows).
- Price pulls back to daily demand/support zone.
- 1h chart prints hammer with long lower wick.

**Interpretation**

- Sellers attempted continuation down but failed.
- Buyers defended a known higher-timeframe level.

**Execution**

- Trigger: break and close above hammer high (or lower-timeframe confirmation).
- Stop: below hammer low.
- Target 1: prior swing high.
- Target 2: trend extension measured move.

**Failure Case**

- Next candle closes below hammer low with high volume.
- Interpretation flips: support failed, exit immediately.

---

### Scenario 2: Bearish Engulfing at Weekly Resistance

**Context**

- Multi-day rally into weekly supply/resistance.
- Momentum slowing (smaller bullish candles before reversal).
- Bearish engulfing appears on 4h chart.

**Interpretation**

- Late buyers got trapped.
- Sellers gained short-term control at key location.

**Execution**

- Entry: close below engulfing low or retest of engulfing midpoint.
- Stop: above engulfing high.
- Targets: nearest support, then next demand zone.

**Educational note:** Even this setup can fail in strong macro uptrends. Size accordingly.

---

### Scenario 3: Doji Cluster Before Breakout

**Context**

- Price consolidates below resistance.
- Multiple doji/small candles form tight range.
- Volume contracts.

**Interpretation**

- Neither side commits; energy buildup likely.

**Execution Paths**

- Breakout long: close above range high + hold retest.
- Breakdown short: close below range low + hold retest.

**Risk Control**

- Avoid anticipatory entry inside chop; wait for confirmed expansion candle.

---

### Scenario 4: Shooting Star into News Volatility

**Context**

- Fast pre-news rally.
- Post-release candle spikes above resistance, closes near open (long upper wick).

**Interpretation**

- Stop-run above level, then aggressive reversal.

**Execution**

- Conservative: wait one full candle confirmation post-news.
- Stop: above shooting star high.
- Target: VWAP / pre-news base.

**Caution**

- News conditions increase slippage; use smaller size and wider invalidation tolerance.

---

### Scenario 5: Three White Soldiers After Base Formation

**Context**

- Long base after downtrend.
- Three consecutive bullish candles with constructive closes.

**Interpretation**

- Demand rebuilding and control transfer to buyers.

**Execution**

- Entry: pullback to second/third candle body zone.
- Stop: below first soldier low.
- Target: overhead supply and previous structure pivots.

**Invalidation**

- Sharp bearish reclaim of entire 3-candle move.

---

## Entry, Stop, Target Frameworks from Candlestick Structure

### Entry Methods

1. **Break entry:** enter after candle high/low breaks.
2. **Close confirmation:** require candle close beyond trigger level.
3. **Retest entry:** wait for pullback and rejection candle.

### Stop Placement Methods

- Structural stop beyond wick extreme.
- Volatility-adjusted stop (e.g., ATR buffer beyond extreme).
- Time stop (if no follow-through in N candles, exit).

### Target Methods

- Nearest opposing liquidity zone.
- Fixed R multiple (e.g., 2R, 3R).
- Trailing via swing highs/lows or moving average.

### Position Sizing Reminder

Risk per trade should be based on stop distance, not confidence in pattern.

---

## Multi-Timeframe Candlestick Reading

### Top-Down Workflow

1. **Higher timeframe (HTF):** determine regime and key levels.
2. **Mid timeframe:** locate active setup zone.
3. **Lower timeframe (LTF):** time entry using candlestick trigger.

### Practical Example

- Daily: uptrend.
- 4h: pullback into support.
- 15m: bullish engulfing + retest hold.

This stack generally outperforms isolated single-timeframe pattern trading.

---

## Volume + Volatility + Session Context

### Volume Confirmation

- Reversal pattern at level + above-average volume = stronger signal.
- Breakout candle with weak volume = higher fakeout risk.

### Volatility Regime

- Low volatility: patterns may take longer to resolve.
- High volatility: wider stops needed; false breaks increase.

### Session Effects

- London/NY overlaps often provide cleaner continuation.
- Illiquid sessions produce noisier wicks and more false triggers.

---

## Related Training Modules

This candlestick module is intentionally focused on price action structure.

For deeper chart integration with participation and positioning data, continue with:

- [Volume Analysis](../02_Technical_Deep_Dive/volume-analysis.md)
- [Open Interest Analysis](../02_Technical_Deep_Dive/interest-open-interest-analysis.md)

For complete chart trading development, use the [Training Hub](../README.md) and [Chart Foundations Section Index](./README.md).

---

## Common Mistakes and Misconceptions

1. **Mistake:** Trading every hammer/engulfing everywhere.
   - Fix: only trade patterns at meaningful structure.

2. **Mistake:** Ignoring trend direction.
   - Fix: prioritize setups aligned with higher-timeframe bias.

3. **Mistake:** Entering before confirmation.
   - Fix: wait for close/trigger/retest rules.

4. **Mistake:** Stop too tight under noisy volatility.
   - Fix: adapt stop to ATR/session volatility.

5. **Mistake:** No invalidation criteria.
   - Fix: define exactly what disproves setup before entry.

6. **Mistake:** Overfitting names of patterns.
   - Fix: focus on order-flow story and location.

---

## Professional Candlestick Checklist

Before every candlestick-based trade, confirm:

- What is the higher-timeframe regime?
- Is the setup at a key level?
- Does candle structure show clear rejection/acceptance?
- Is there volume or momentum confirmation?
- Where is invalidation (hard stop)?
- Is reward at least acceptable versus risk?
- Is there upcoming news/event risk?
- What is the management plan after entry?

No checklist compliance, no trade.

---

## Practice Curriculum (Training Path)

### Phase 1: Visual Literacy (Week 1)

- Label 200 candles as momentum, rejection, indecision.
- Annotate body/wick ratios.
- Build intuition for candle quality.

### Phase 2: Pattern-in-Context (Week 2-3)

- Collect 50 examples each of hammer, engulfing, doji cluster.
- Tag context: trend/range, level type, session, outcome.
- Record what worked and why.

### Phase 3: Rule-Based Execution (Week 4-5)

- Define one long setup and one short setup.
- Backtest with fixed entry/stop/target rules.
- Measure win rate, expectancy, max drawdown, average hold time.

### Phase 4: Forward Simulation (Week 6+)

- Paper trade only.
- Journal screenshots pre/post trade.
- Track errors: early entry, no confirmation, emotional exits.

### Suggested Journal Fields

- Date/time/session
- Instrument/timeframe
- Pattern name + candle metrics
- Context notes (trend, level, volume)
- Entry/stop/target
- Outcome (R multiple)
- Lessons learned

---

## Glossary

- **Acceptance:** Price staying above/below a level with supportive closes.
- **Rejection:** Price probes a level and quickly fails to hold beyond it.
- **Confluence:** Multiple independent factors supporting a directional thesis.
- **Invalidation:** Specific condition proving trade idea wrong.
- **Liquidity sweep/stop-run:** Brief move beyond obvious highs/lows to trigger stops before reversal.
- **Range expansion:** Candle range significantly larger than recent average.

---

## Final Expert Guidance

Candlesticks are a language. Mastery comes from reading grammar (structure), meaning (psychology), and context (market location). The strongest edge appears when:

- Pattern quality is clean,
- Context is favorable,
- Risk is defined,
- Execution is disciplined,
- And review is consistent.

Use this document as a foundational training module, then evolve it with your own market-specific stats and screenshots from your trading journal.
