This repository is structured as follows:

```
.
├── robot_reachability_analysis/
│   ├── assets/
│   ├── dynamics/
│   ├── experiments/
│   ├── intuition_plots/
│   ├── notebooks/
│   ├── utils/
│   └── README.md
├── README.md
└── deepreach_paper_analysis.md
```

---

### File and Folder Descriptions

#### Root

- **robot_reachability_analysis/**  
  Cod used to implement and analyze a 2D planar robot reachability problem.
- **deepreach_paper_analysis.md**  
  A review of the paper "_DeepReach: A Deep Learning Approach to High-Dimensional Reachability_", covering:
  - Key Contributions of the DeepReach approach
  - Few limitations and ideas/suggestions for addressing those

#### robot_reachability_analysis/

- **assets/**: Stores static plot images from experiments and sample figures used in the intuition section.
- **dynamics/**: Defines a new `Dynamics` sub-class for a 2D planar robot model.
- **experiments/**: Original DeepReach experiment scripts, adapted to visualize and compute BRTs for 2D systems.
- **intuition_plots/**: Contains illustrative scripts that generate toy plots for the intuition section.
- **notebooks/**: Jupyter notebooks with outputs and visualizations for each experiment.
- **utils/**: Unmodified utility functions and modules from the original DeepReach public release.
- **README.md**: Contains intuition report, hamiltonian calculation and observations from experiments.

