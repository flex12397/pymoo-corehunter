import numpy as np
import pandas as pd
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from sklearn.metrics import pairwise_distances

# Universal import solution
try:
    from pymoo.operators.sampling.random import RandomSampling
except ImportError:
    try:
        from pymoo.operators.sampling.rnd import RandomSampling
    except ImportError:
        from pymoo.core.sampling import Sampling
        class RandomSampling(Sampling):
            def _do(self, problem, n_samples, **kwargs):
                return np.random.random((n_samples, problem.n_var))

# Load data
geno_data = pd.read_csv("geno.csv", index_col="ID")
pheno_data = pd.read_csv("pheno.csv", index_col="ID")
X_geno = geno_data.values.astype(int)

# Compute distance matrix
D = pairwise_distances(X_geno, metric="hamming")

# Problem definition
class CoreHunterProblem(Problem):
    def __init__(self, D, core_size):
        self.D = D
        self.core_size = core_size
        super().__init__(n_var=D.shape[0], n_obj=2, n_constr=0, xl=0, xu=1)

    def _evaluate(self, X, out, *args, **kwargs):
        F = np.zeros((X.shape[0], 2))
        for i in range(X.shape[0]):
            core_indices = np.argsort(X[i])[-self.core_size:]
            D_core = self.D[np.ix_(core_indices, core_indices)]
            D_all = self.D[core_indices, :]
            F[i] = [-np.mean(D_core), np.mean(D_all)]
        out["F"] = F

# Optimization
problem = CoreHunterProblem(D, core_size=20)
algorithm = NSGA2(
    pop_size=100,
    sampling=RandomSampling(),
    eliminate_duplicates=True
)
res = minimize(problem, algorithm, ('n_gen', 50), seed=1)

# Results
best_solution = res.X[np.argmin(res.F[:, 1])]
core_indices = np.argsort(best_solution)[-20:]
core_samples = geno_data.index[core_indices]
print("Optimal Core:", core_samples)
