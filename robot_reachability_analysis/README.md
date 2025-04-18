

## Intuition on Reachability for a Planar Robot

We consider a planar autonomous robot whose state $x=(p_x, p_y)$ evolves as:

$$
\dot p_x = v \cos\theta, \quad \dot p_y = v \sin\theta
$$

with constant speed $v = 1$ m/s and direct control of the heading $\theta \in [-\pi, \pi]$. Unlike systems with angular rate control, this robot can **instantaneously** choose any heading $\theta$ at any time.

---

### Cases Considered

We analyze three cases over a time horizon $T = 1$ s:

1. **BRT for Obstacle Avoidance**: An obstacle of radius 0.5m is at the origin. Compute the set of initial states from which collision is unavoidable.
2. **Safe Set for Obstacle Avoidance**: An obstacle of radius 0.5m is at the origin. Compute the set of initial states from which the robot is guaranteed to avoid the obstacle.
3. **BRT for Goal Reachability**: A goal of radius 0.25m is at the origin. Compute the set of initial states from which the robot can reach the goal.


The system is considered to have "reached" a target if it reaches **any point within a circle** of the given radius.

---

### Notation

We define the circle of center $c = (x, y)$ and radius $r$ as:

```math
C(c, r) = \{ p \in \mathbb{R}^2 \mid \|p - c\| \leq r \}
```

Note: While the term "circle" traditionally refers to points on the circumference, I use $C(c, r)$ to represent all points **within and on** the boundary (the closed region of radius $r$ centered at $c$). 

This is used in this section to represent goal regions, obstacles, and reachable sets.

---

### 1. BRT for Obstacle Avoidance

**Definition:**  
The Backward Reachable Tube (BRT) in this case is the set of initial states from where the system **cannot avoid** hitting the obstacle within the given time horizon, even with optimal control.

**Observation:**  
The robot has the ability to directly and instantaneously control its heading $\theta$.  
This means that even in extreme cases, e.g. starting on the boundary of the obstacle and heading toward it, the robot can immediately change its direction to avoid the obstacle.  

Thus, the only **unsafe** states are those **already inside** the obstacle at $t=0$.

### Therefore:

For all $t = 0$, $0.5$, and $1.0$ s:

$$
\text{BRT}_{t} = C\left((0, 0),\, 0.5\right)
$$

#### Visualization (placeholders)

| $t = 0s$ | $t = 0.5s$ | $t = 1.0s$ |
|:--------:|:-----------:|:-----------:|
| ![BRT0](assets/brt_obstacle_05m.png) | ![BRT05](assets/brt_obstacle_05m.png)  | ![BRT1](assets/brt_obstacle_05m.png)   |

---

### 2. Safe Set for Obstacle Avoidance

**Definition:**  
The **safe set** is the set of initial states from which the robot is guaranteed to **never enter** the obstacle region, regardless of the control input (i.e., no matter how $\theta$ is chosen over time).

#### Derivation

1. The robot can move up to a distance of $vT$ in time $T$.

2. So, starting from state $x$, the reachable region within time $T$ is:

```math
C(x, vT)
```

3. A collision is possible if the circle of radius \(vT\) around \(x\) and the obstacle circle of radius \(r_o\) around the origin **overlap**. Two circles of radii \(R\) and \(r\) overlap if and only if the distance between their centers is at most \(R + r\).

```math
\|x - (0,0)\| \;\le\; vT + r_o
\quad\Longleftrightarrow\quad
\|x\|\;\le\;vT + r_o.
```

4. The safe set is the complement of the above:

```math
\mathcal{S}_T = \left\{ x \mid \|x\| > vT + r_o \right\}
```

5. Substituting $v = 1$, $r_o = 0.5$:

```math
\mathcal{S}_T = \left\{ x \mid \|x\| > T + 0.5 \right\}
```

#### Interpretation

At each time point, the safe set excludes a circle centered at the origin with radius $T + 0.5$.

#### Visualization (placeholders)

| $t = 0s$ | $t = 0.5s$ | $t = 1.0s$ |
|:--------:|:-----------:|:-----------:|
| ![Safe0](assets/safeset_t0.png) | ![Safe05](assets/safeset_t05.png) | ![Safe1](assets/safeset_t10.png)  |

---

### 3. BRT for Goal Reachability

**Definition:**  
This BRT is the set of initial states from which the robot **can reach** a goal region within the time horizon $T$.

#### Derivation

1. Reachable region from state $x$ in time $T$ is again:

```math
C(x, vT)
```

2. The robot can **reach** the goal centered at the origin with radius $ r_g $ if the reachable region from $ x $ overlaps with the goal region. Two circles overlap if and only if the distance between their centers is at most the sum of their radii:

```math
\|x\| \leq vT + r_g
```

4. Therefore, the BRT for reaching the goal is:

```math
\text{BRT}_T = C\left((0, 0),\, vT + r_g\right)
```

5. Substituting $v = 1$, $r_g = 0.25$:

```math
\text{BRT}_T = C\left((0, 0),\, T + 0.25\right)
```

#### Interpretation
At each time point, the BRT includes a circle centered at the origin with radius $T + 0.25$.

#### Visualization (placeholders)

| $t = 0s$ | $t = 0.5s$ | $t = 1.0s$ |
|:--------:|:-----------:|:-----------:|
| ![Goal0](assets/goalreach_t0.png) | ![Goal05](assets/goalreach_t05.png) | ![Goal1](assets/goalreach_t10.png)  |
