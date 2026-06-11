# minimax/minimax-m3

## Assumptions I'm making (stated upfront)

- **AI capability continues advancing at roughly the current pace** to 2030–32, then broadens/deepens: today's frontier models are like 1995's internet — already transformative in narrow settings, not yet fully diffused. I assume the pattern of "impressive demos, uneven deployment" continues.
- **Embodied AI/robotics lags software AI by 3–6 years.** Useful home robots by ~2033, generally capable domestic robots by ~2038–42, but expensive and not yet mass-market at sub-$25k.
- **No AGI/superintelligence by 2046**, but AI is integrated into most white-collar and many service jobs. Compute costs fall ~30–40%/yr, but absolute energy demand grows faster.
- **Energy is a binding constraint** in some regions, especially where AI datacenters cluster. Renewables + storage expand but unevenly.
- **Geopolitical fragmentation is moderate**, not a new Cold War, not full integration. AI is treated as a strategic asset; export controls on chips stay in place.
- **Demographic decline** continues in most developed economies; population aging creates labor demand in care/health but strains fiscal capacity.
- **Political systems respond slowly** to economic disruption. I do not assume proactive, anticipatory redistribution.

---

## 1. Trajectories

I sort outcomes by **how the political economy resolves the tension between AI-driven productivity gains and labor displacement**. Five trajectories, my own categories.

### A. Slow Burn Stagnation — 20%
**Mechanism:** AI capability grows but deployment is bottlenecked by organizational inertia, regulation, trust deficits, and energy constraints. Productivity gains are real but modest in aggregate. Displacement is gradual and concentrated in clerical, customer service, and routine cognitive work, but not fast enough to cause crisis. Median wages drift down slowly as bargaining power erodes; GDP grows but the median captures little of it.

**Median person, 2046:** Household real disposable income roughly flat or 5–10% below 2026. One earner in healthcare, retail, trades, or care work; the other partner in similarly "sticky" work or has exited the labor force. They own a home in a secondary city, mortgage paid down, but real purchasing power for goods has stagnated. A small AI subscription ($30–80/month) handles scheduling, taxes, research, and basic medical triage. Health and energy costs eat a growing share of budget. Some means-tested transfers. They feel busier but not poorer — until they check savings.

### B. Capital Concentrates the Surplus — 30%
**Mechanism:** AI deploys fast in sectors where it's plug-and-play (software, finance, marketing, legal research, parts of logistics, biotech design). Productivity surges in those sectors; corporate margins and asset prices rise sharply. Median wages barely move because (i) most workers aren't in AI-augmented occupations, (ii) union density continues to fall, and (iii) competition for talent is confined to the top quintile. The labor share of income drops meaningfully. Fiscal pressure builds, but tax reform lags. Net: GDP up substantially, median flat.

**Median person, 2046:** Working full-time, possibly two jobs or one job plus gig work. Real income up 0–5% from 2026. Housing is the dominant cost — 35–45% of household budget in the US/UK/Canada/Australia. A small AI assistant handles scheduling, bill payment, and lots of consumer research, but the person's job is unchanged in nature (or slightly more intense, with AI monitoring their output). Health insurance via employer; one serious illness is a financial catastrophe. They are heavily invested in equities, mostly through retirement accounts, and feel the wealth effect — even though they don't sell. Some modest transfers (child credit, healthcare subsidy). The household is two paychecks from insolvency.

### C. Mundane Diffusion — 20%
**Mechanism:** AI diffuses broadly enough to lower consumer prices meaningfully (especially in services, healthcare admin, education tutoring, software, entertainment) and lift productivity growth to 2.5–3.5%. Some policy response: expanded EITC/negative income tax, modest housing reform, more aggressive antitrust. Real median income grows 5–15%. Inequality rises, but not dramatically. Boring version of a good future.

**Median person, 2046:** Real income up 10–15%. Works in a job that didn't exist in 2026 (e.g., AI trainer, robot fleet technician, remote care coordinator, climate retrofitter) or in a traditional job augmented by AI that lets them do 1.5x the previous workload. Healthcare and childcare still expensive but improved by AI. Housing still the largest cost but policy has eased it marginally (more construction, some rent stabilization). Tuition costs down due to AI tutoring. Net: more comfortable than 2026, but aware that the top 1% are doing much better.

### D. Broad AI Dividend — 15%
**Mechanism:** AI deployment is broad and deep, productivity growth hits 4–5%, and — critically — political systems respond with major redistribution: a meaningful UBI or citizen dividend, public options in housing/healthcare, serious antitrust and capital taxation. Median real income rises 25–50%. Working hours fall. Cultural change: many people work less, start households later, do more care work, make more art. Wealth inequality may still grow in stock form but consumption inequality narrows.

**Median person, 2046:** Household real disposable income up 30–40%, driven by a UBI/dividend of roughly $15–25k/yr per adult, plus one earner working 25–30 hrs/week. Healthcare is largely public. Housing: still the biggest budget item, but a public-housing push has made it manageable. They use AI assistants that meaningfully reduce time spent on admin, shopping, and coordination. Work is more voluntary and project-based. They have more time, less money stress, but a vague sense that the system is fragile and political.

### E. Crisis and Reset — 15%
**Mechanism:** A shock in 2028–2034 (financial crisis triggered by AI-driven displacement of white-collar work, a major AI-involved accident, severe climate/energy shock, or geopolitical conflict over chips) causes a deep recession and political crisis. Populist left and right both surge. Outcomes of the crisis: in the most likely version, a major rebalancing — UBI or job guarantee enacted, public options expanded, antitrust action, capital taxation. By 2046, the median is roughly back to 2026 real income, but the system is more equal, more public, and more brittle. In a darker version (5% embedded in this 15%), democratic backsliding, AI-facilitated authoritarianism, persistent stagnation.

**Median person, 2046:** Has lived through a difficult 2029–2034. Now has a UBI plus a public job (teaching, care, infrastructure maintenance, climate work). Housing is partly public. They are more politically engaged, more skeptical of institutions, and aware of how close the system came to breakdown. Real income similar to 2026; consumption more equal.

---

## 2. Calibrated estimates

Each statement treated independently.

- **a) Median real disposable income higher than 2026: 60%**
- **b) Median real disposable income more than 20% lower than 2026: 15%**
- **c) Labor share of national income below 40% (vs ~55–60% today): 40%**
- **d) More than 25% of prime-age adults who want paid work cannot find any: 22%**
- **e) Ordinary citizens' influence over government policy is substantially weaker than 2026: 65%**
- **f) Top 1%'s share of national wealth at least 10pp higher than 2026: 50%**
- **g) Housing + energy + food consume a larger share of the median household budget than 2026: 55%**
- **h) A typical household can buy a robot/AI system performing most domestic + basic production tasks for <6 months median income: 35%** *(if "system" is interpreted as software AI only, this is 90%; if embodied robot is required, ~25%)*
- **i) Government transfers are the largest income source for the median working-age household: 20%**
- **j) AI systems / their operators make most consequential resource-allocation decisions with little effective human oversight: 35%**

---

## 3. Drivers

The quantitative parameters that most determine which trajectory obtains:

1. **AI capability doubling time on economically relevant benchmarks** (currently ~12–18 months on coding, math, reasoning). Why it matters: drives the speed of displacement and the ceiling on productivity gains. My best guess: holds near current pace through 2030, then extends to 18–30 months as benchmark saturation and energy/compute constraints bite. **Critical parameter #1.**

2. **Diffusion rate — fraction of firms in each sector that have meaningfully deployed AI in production.** Why it matters: the gap between capability and deployment is enormous, and that gap is where the political economy is decided. My best guess: software/finance/marketing hit 70–80% deployment by 2030; healthcare, education, legal at 50–60% by 2035; physical work (construction, care, food service) lags 8–12 years behind software.

3. **Labor share elasticity to AI deployment** (how much of each marginal AI-driven productivity gain goes to workers vs. capital in a given institutional setting). Why it matters: determines whether the gains lift median or top. My best guess: continues the 1990s–2020s trend, with labor share falling 5–10pp in economies that don't actively intervene.

4. **Speed of fiscal/political response** — years between widespread displacement and a major transfer or tax reform. Why it matters: separates trajectory C/D from B/E. My best guess: slow in most countries (5–10 years lag), fast only under crisis (E path) or with unusually capable government (D path). This is partly endogenous to displacement severity.

5. **Energy supply and cost growth**, especially clean baseload. Why it matters: caps total AI deployment and shapes which economies benefit. My best guess: 2–3%/yr growth in electricity demand from AI; nuclear restart in some jurisdictions, storage expansion, but persistent regional bottlenecks. AI is energy-gated before it's labor-gated in many places.

6. **Housing supply elasticity** in major developed-economy metros. Why it matters: housing is the single largest budget item and the biggest source of real welfare loss or gain. My best guess: marginal improvement in US/Australia/Canada, continued tightness in UK, modest improvement in dense European cities. **Net: housing burden stays high or rises** in most developed economies.

7. **Antitrust / market concentration trajectory** in AI-adjacent industries. Why it matters: determines whether AI productivity gains are competed away to consumers or captured as rents. My best guess: weak enforcement, AI markets consolidate to 3–5 dominant general-purpose providers plus sector specialists. Rents persist.

8. **Geopolitical fragmentation index** — degree of decoupling between US/EU and China blocs on AI/chips/data. Why it matters: shapes global supply chains, talent flows, and the cost of compute. My best guess: continued moderate fragmentation, with two parallel AI ecosystems. Slightly raises costs globally; doesn't break the forecast.

---

## 4. The mechanism I'd bet on

The single most predictive mechanism for the median person's economic welfare in 2046 is **the gap between AI productivity gains and the speed of political redistribution, combined with capital's structural advantage in capturing returns when bargaining power is low**. AI lowers the marginal cost of producing many goods and services, but it also lowers labor's bargaining position: when your employer can substitute an AI for your cognitive output, your wage is set by your reservation utility, not your productivity. In an institutional environment where unions are weak, antitrust is permissive, and transfer programs are slow to build, the surplus from AI accrues to owners of capital, owners of data, and the small set of workers whose labor is complementary to AI (a top-quintile slice). The median's welfare in this scenario depends almost entirely on (a) how much consumer-price decline they actually capture, (b) how much housing they can secure, and (c) whether the state insulates them from health and energy shocks. None of those three are easy. My base case is that the median ends 2046 with real income roughly flat to slightly down, much more time-pressure (work intensity rises, but at-home convenience rises too), and substantially more inequality of wealth and consumption — with the central question being whether the 2030s produce enough political pressure to trigger the kind of redistribution seen in trajectory D, or whether the system grinds along the B/C path.

---

## 5. Confidence and failure

**What would make my central forecast wrong:**

- **AI capability plateaus** in 2027–2029 (we stop seeing reliable capability gains on hard benchmarks, scaling laws hit a wall that's clearly not just temporary). This would push probability mass from B/C/D back into A. Watch for: stall in math/reasoning benchmarks, persistent inability of models to do multi-step autonomous work over weeks, or a major architectural dead-end.
- **AI capability explodes** in 2027–2030 in ways that produce clearly agentic systems capable of running entire business processes. This would shift mass toward D or E and raise (i) and (j) substantially.
- **A major democratic-political realignment in 2028–2032** in the US, UK, or EU that genuinely reorganizes fiscal policy (serious wealth/capital taxation, large UBI, public option in housing). This would push toward D. The most likely single trigger is a deep recession hitting white-collar employment hard.
- **Energy/climate shock much worse than I expect** — major grid failures, AI datacenter buildout hits hard limits, climate migration disrupts labor markets. This would push toward A or the dark variant of E.
- **Embodied AI/robotics progresses faster than I expect** (e.g., useful general-purpose home robots under $20k by 2032). This would make (h) much more likely and shift trajectories.

**Claims I am least confident in (ranked by uncertainty):**

1. **(b) P = 15%** — a >20% real income decline requires either a severe crisis, persistent stagflation, or a deep distributive failure. The probability of a *bad enough* outcome is genuinely hard to bound from below. Could easily be 8% or 22%.
2. **(i) P = 20%** — this depends heavily on the path through the 2030s and whether UBI gets enacted. Could be 10% or 30%.
3. **(h) P = 35%** — depends on whether one interprets the question as software AI (in which case 90%) or embodied robots (in which case 25%). Honest answer: I don't know what the median person in 2046 considers a "robot/AI system that performs most domestic and basic production tasks
