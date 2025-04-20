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
This section outlines a fre limitations of the DeepReach framework and suggests possible extensions, with a focus on safety and computational efficiency. 

### Safety

**Safety Guarantees**

DeepReach replaces a provably convergent solver with a neural network that only approximately satisfies the HJI/HJB PDE. Since the PDE is enforced as a soft constraint, the learned value function often deviates from the exact $V=0$ condition, potentially misclassifying safe and unsafe states. Several types of safety guarantees can be explored:
- Emperical: Build a benchmark of reachability problems with known ground-truth value functions (via analytical or classical solvers) to empirically evaluate DeepReach’s approximation error.
- Probabilistic: Inspired by classical relaxations like $V(x,t)≤δ$ (e.g. to account for sensor noise) define probabilistic safety bands around the predicted BRT. Sample and simulate trajectories starting near the boundary to estimate the likelihood of staying safe.
- Deterministic: : In special cases (e.g. time-invariant avoid problems), conservative BRT over-approximations can be derived using known geometric structures (e.g. ellipsoids).
- Evolving Safety Guarantees: In real-world deployments, system parameters (velocity, sensor accuracy) may be uncertain.Sensitivity of the learned value function to such changes can be analyzed using gradient-based or perturbation methods to assess robustness (e.g. simulating changes in parameters and observing the stability of predicted safety margins).


**Lowering Error Rates**

Building on the limitations introduced by approximation errors, misclassifications of safe and unsafe states can arise. Corrective strategies can be explored:
- Post-training Methods: Perform a round of supervised train using error samples, either from random resampling or drawn from prior safety guarantee evaluations. Beyond simply flipping misclassified states, the loss function could also include:
    - Penalizing overly-optimistic errors, such as large positive $V$ values for unsafe states.
    - In reach settings, under-approximation might be safer, and vice versa for avoid. versa. This could be implemented by adding loss terms that asymmetrically penalize the model based on the task (e.g., extra penalty for $V>0$ in avoid settings when true value is $V<0$). This could also be extended to BRAT.
- Training Methods: In multi-class self-supervised learning, auxiliary rankers/classifiers estimate the likelihood of class membership[[4]](#references). A similar idea could be applied in the reachability setting. An additional model could be trained alongside DeepReach to predict whether a state is safe or unsafe along with a confidence score. High-confidence predictions could then be validated through trajectory simulations, and the results used to further calibrate both the main model and the classifier.














 


### Efficiency








## References
1. Bansal, S., Chen, M., Herbert, S., & Tomlin, C. J. (2017). Hamilton-Jacobi Reachability: A Brief Overview and Recent Advances. ArXiv. https://arxiv.org/abs/1709.07523
2. S. Bansal, M. Chen, K. Tanabe and C. J. Tomlin, "Provably Safe and Scalable Multivehicle Trajectory Planning," in IEEE Transactions on Control Systems Technology, vol. 29, no. 6, pp. 2473-2489, Nov. 2021, doi: 10.1109/TCST.2020.3042815.
3. V. Sitzmann, J. N. Martel, A. W. Bergman, et al. “Implicit neural representations with periodic activation functions”. arXiv preprint arXiv:2006.09661 (2020).
4. R. T. Mullapudi, F. Poms, W. R. Mark, D. Ramanan and K. Fatahalian, "Learning Rare Category Classifiers on a Tight Labeling Budget," 2021 IEEE/CVF International Conference on Computer Vision (ICCV), Montreal, QC, Canada, 2021, pp. 8403-8412, doi: 10.1109/ICCV48922.2021.00831.
