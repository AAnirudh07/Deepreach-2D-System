This report presents an analysis of the paper, "DeepReach: A Deep Learning Approach to High-Dimensional Reachability". 

## Table of Contents
* [Key Contributions](#key-contributions)
* [Limitations and Extensions](#limitations-and-extensions)
* [References](#references)

## Key Contributions

In safety-critical systems, it is important to verify that the system can remain within safe bounds despite uncertainties or worst-case disturbances. Hamilton-Jacobi (HJ) reachability[[1]](#references) is a formal method for computing the set of safe (or unsafe) initial states by solving for a value function that encodes system safety. This value function is the solution to a partial differential equation, specifically, a Hamilton-Jacobi-Isaacs (HJI) or Hamilton-Jacobi-Bellman (HJB) variational inequality and is traditionally solved using dynamic programming by discretizing the state space into a grid.

While HJ reachability provides safety guarantees, it suffers from the "curse of dimensionality". The number of grid points and computation time grow exponentially with the number of state variables. Even with modern optimized solvers such as BEACLS[[2]](#references), classical methods are limited to systems with at most six state dimensions.

DeepReach introduces an approach for learning/approximating the value function of nonlinear systems using deep neural networks. It offers the following benefits over traditional methods:
- The computational complexity now scales with the complexity of the value function, not the dimensionality of the state space.
- Unlike other approximation methods, DeepReach can handle disturbances and constraints.

To achieve this, DeepReach integrates the following machine learning techniques:
- **Self-supervised learning of the value function**: The PDE serves as the supervisory signal during training. A second term corresponding to the additional term in the HJI variational inequality (or more in the case of BRAT) is used to handle edge cases such as constant value functions with zero gradient.
- **Sine activation functions** – These represent the underlying function and gradients well[[3]](#references). This is required as the loss term includes gradients of the value function.
- **Curriculum learning**: Training proceeds backward in time from the terminal set helping the network learn easier subproblems first and progressively solve the full problem.


## Limitations and Extensions
This section outlines a few limitations of the DeepReach framework and suggests possible extensions, with a focus on safety and computational efficiency. 

### Safety

**Safety Guarantees**

DeepReach replaces a provably convergent solver with a neural network that only approximately satisfies the HJI/HJB PDE. Since the PDE is enforced as a soft constraint, the learned value function often deviates from the exact $V=0$ condition, potentially misclassifying safe and unsafe states. Several types of safety guarantees can be explored:
- Emperical: Build a benchmark of reachability problems with known ground-truth value functions (via analytical or classical solvers) to empirically evaluate DeepReach's approximation error.
- Probabilistic: Inspired by classical relaxations like $V(x,t)≤δ$ (e.g. to account for sensor noise) define probabilistic safety bands around the predicted BRT. Sample and simulate trajectories starting near the boundary to estimate the likelihood of staying safe.
- Deterministic: : In special cases (e.g. time-invariant avoid problems), conservative BRT over-approximations can be derived using known geometric structures (e.g. ellipsoids).
- Evolving Safety Guarantees: In real-world deployments, system parameters (velocity, sensor accuracy) may be uncertain.Sensitivity of the learned value function to such changes can be analyzed using gradient-based or perturbation methods to assess robustness (e.g. simulating changes in parameters and observing the stability of predicted safety margins).


**Error Rates**

Building on the limitations introduced by approximation errors, misclassifications of safe and unsafe states can arise. Corrective strategies can be explored:
- Post-training Methods: Perform a round of supervised train using error samples, either from random resampling or drawn from prior safety guarantee evaluations. Beyond simply flipping misclassified states, the loss function could also include:
    - Penalizing overly-optimistic errors, such as large positive $V$ values for unsafe states.
    - In reach settings, under-approximation might be safer, and vice versa for avoid. versa. This could be implemented by adding loss terms that asymmetrically penalize the model based on the task (e.g., extra penalty for $V>0$ in avoid settings when true value is $V<0$). This could also be extended to BRAT.
- Training Methods: In multi-class self-supervised learning, auxiliary rankers/classifiers estimate the likelihood of class membership[[4]](#references). A similar idea could be applied in the reachability setting. An additional model could be trained alongside DeepReach to predict whether a state is safe or unsafe along with a confidence score. High-confidence predictions could then be validated through trajectory simulations, and the results used to further calibrate both the main model and the classifier.

**Uncertainty**

DeepReach assumes that control and disturbance dynamics and bounds are fully known. In practice, these may be partially known or uncertain. Mechanisms that can adapt to incomplete or evolving knowledge are needed.

- Uncertain Control: When the control model is unknown or only partially known, one option is to estimate it through input-output state sampling. Sampling strategies could be refined. As an example, adversarial sampling could be used to select the most challenging controls by performing a few gradient ascent steps on each sampled control maximizing the PDE residual.
- Uncertain Disturbance:
    - When disturbances are uncertain, it can be useful to maintain conservative estimates that adapt over time with more data. Building on work such as [[5]](#references), we could use a Bayesian belief over disturbance dynamics. When $V_t + H$ deviates from zero, it can serve as a proxy for how unexpected an adversarial action is (mismatch between the modeled dynamics and reality), and be used to refine the belief.
    - If it is difficult to learn the disturbance directly, a scalar confidence parameter could be added to the DeepReach state space to encode uncertainty. During runtime, the system could observe the disturbance to evaluate a confidence score and determine the appropriate action.
- Adversaries with More Information: HJI reachability typically assumes a non-anticipative adversary. In reality, adversaries may have access to more information or act strategically. One idea could be to model the inverse of the FsSTrack[[6]] formulation and adapt to DeepReach. For example, the problem can be reframed as a pursuer-evader game instead of a tracker-planner setup, where the evader (controller) operates in a lower-dimensional space to reflect limited information, while the pursuer operates in a higher-dimensional state (e.g., additional knowledge of the environment or the evader's internal variables).


**On Reachability as a 'Safety Verifier'**

In practice, the optimal control is used as a _least-restrictive safety controller_ which is activated  near the boundary of unsafe regions, while a separate performance-oriented controller governs the rest of the state space. It raises some concerns:
- As mentioned earlier, the approximate nature of DeepReach's value function can lead to errors.
- More broadly, this results in jerky behavior which makes the safety control less reliable in practice if the system's true dynamics deviate slightly from the modeled ones.

To address this:
- One approach is to balance when and how strongly safety should be enforced. An area I have come across that does this is Control Barrier Function [[7]](#references) when combined with HJ reachability[[8]](#references). This could be integrated into DeepReach's loss function. Furthermore, the coefficient $\gamma$ could be parameterized, allowing the system to adapt to its current confidence in the environment in real time e.g. using a high $\gamma$ in low-confidence environments.
- Reachability constraints could be introduced directly into other learning frameworks (e.g., reinforcement learning). For instance, policy gradient or actor-critic methods could learn a control policy $π_θ(x, t)$ while including the HJI PDE as a constraint or regularization term.


**Recovery from Unsafe States**

While not a direct limitation of DeepReach, standard HJ reachability tends to define conservative boundary conditions (e.g. 5 mile safety radius for aircraft) and assumes worst-case disturbances. This leaves little room for exploring recovery strategies once a system enters an unsafe state.

I came across Control Lyapunov Functions[[9]](#references) which could help with this. It may be worth investigating whether similar effects exist in HJ reachability, and whether CLF-based recovery objectives could be integrated into DeepReach's training loss. This could also support softer safety guarantees.


### Efficiency

**Offline Learning Costs**

While recent improvements have reduced DeepReach's training time to around three hours (from 16), further optimizations are possible without altering the training setup.
- Sampling: Deepreach samples at random over a given time interval, but other sampling strategies could be explored to reduce the number of samples:
    - Bias sampling toward regions with high gradient magnitude (sharp changes in the value function).
    - Areas with large PDE residuals, where the model is least accurate.
    - Include regions near the zero level set where prediction accuracy is important.
    - Bias sampling away from certain regions when appropriate e.g., avoid sets, if soft guarantees can show that it is an avoid set.
- Training: Standard curriculum learning typically follows a fixed schedule. An adaptive curriculum could adjust progression based on learning performance:, slowing down if loss remains high or convergence stalls, and speeding up when learning is stable. This could help reduce error rates and improve convergence speed. 

**Adaptation to Online Learning**

As outlined in the paper, DeepReach is not feasible for online computation. Two approaches could help address this in settings where the environment is either unknown or known apriori. These are discussed here rather than in the safety section, as they relate more directly to efficiency.
- Unknown Environment: Inspired by methods like  in [[10]](#references), one could adapt DeepReach to incrementally explore an environment. The idea is to only recompute reachable sets for newly discovered regions and their neighbors. In DeepReach, this could be framed as a spatial curriculum gradually expanding the spatial domain during training as new areas are revealed.
- Known Environment: If a nominal model of the environment is known, one could use continual/incremental learning to refine the reachability estimate in real-time. For instance, start with a coarse approximation (e.g., by simplifying dynamics or using fewer samples), then update the model incrementally as more data or computational time becomes available.


**Learning Value Functions from Similar Settings**

DeepReach trains a neural network to approximate a value function. However, once trained, this model is not reused even for slightly modified scenarios. As an example, The multi-plane trajectory planning problem where three planes are given goals and obstacles, is decomposed into three sequential planning tasks, each differing slightly from the last (e.g., by introducing one or more additional planes as disturbances).

Transfer learning is a ML technique where a model trained on one task is adapted to a new but related task and could help here. In DeepReach's case, we could retain the core of the trained model (the three hidden layers of 512 neurons each and the output layer) and only adapt the input layer to reflect new state or disturbance dimensions. This could help 'warm-start' the model for similar configurations.


## References
1. Bansal, S., Chen, M., Herbert, S., & Tomlin, C. J. (2017). Hamilton-Jacobi Reachability: A Brief Overview and Recent Advances. ArXiv. https://arxiv.org/abs/1709.07523
2. S. Bansal, M. Chen, K. Tanabe and C. J. Tomlin, "Provably Safe and Scalable Multivehicle Trajectory Planning," in IEEE Transactions on Control Systems Technology, vol. 29, no. 6, pp. 2473-2489, Nov. 2021, doi: 10.1109/TCST.2020.3042815.
3. V. Sitzmann, J. N. Martel, A. W. Bergman, et al. “Implicit neural representations with periodic activation functions”. arXiv preprint arXiv:2006.09661 (2020).
4. R. T. Mullapudi, F. Poms, W. R. Mark, D. Ramanan and K. Fatahalian, "Learning Rare Category Classifiers on a Tight Labeling Budget," 2021 IEEE/CVF International Conference on Computer Vision (ICCV), Montreal, QC, Canada, 2021, pp. 8403-8412, doi: 10.1109/ICCV48922.2021.00831.
5. Fisac, J. F., Akametalu, A. K., Zeilinger, M. N., Kaynama, S., Gillula, J., & Tomlin, C. J. (2017). A General Safety Framework for Learning-Based Control in Uncertain Robotic Systems. ArXiv. https://arxiv.org/abs/1705.01292
6. Herbert, S. L., Chen, M., Han, S., Bansal, S., Fisac, J. F., & Tomlin, C. J. (2017). FaSTrack: A Modular Framework for Fast and Guaranteed Safe Motion Planning. ArXiv. https://doi.org/10.1109/CDC.2017.8263867
7. Ames, A. D., Coogan, S., Egerstedt, M., Notomista, G., Sreenath, K., & Tabuada, P. (2019). Control Barrier Functions: Theory and Applications. ArXiv. https://arxiv.org/abs/1903.11199
8. Tonkens, S., & Herbert, S. (2022). Refining Control Barrier Functions through Hamilton-Jacobi Reachability. ArXiv. https://arxiv.org/abs/2204.12507
9. Sontag, E.D. (1999). Control-Lyapunov functions. In: Blondel, V., Sontag, E.D., Vidyasagar, M., Willems, J.C. (eds) Open Problems in Mathematical Systems and Control Theory. Communications and Control Engineering. Springer, London. https://doi.org/10.1007/978-1-4471-0807-8_40
10. Bajcsy, Andrea & Bansal, Somil & Bronstein, Eli & Tolani, Varun & Tomlin, Claire. (2019). An Efficient Reachability-Based Framework for Provably Safe Autonomous Navigation in Unknown Environments. 1758-1765. 10.1109/CDC40024.2019.9030133. 