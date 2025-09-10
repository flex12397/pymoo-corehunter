import numpy as np
import pandas as pd
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM
from pymoo.operators.sampling.rnd import IntegerRandomSampling
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics.pairwise import euclidean_distances
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

class CoreHunterProblem(Problem):
  def __init__(self, genotype_data, phenotype_data, core_size, distance_metric='euclidean'):
    self.genotype_data = genotype_data
    self.phenotype_data = phenotype_data
    self.core_size = core_size
    self.total_accessions = genotype_data.shape[0]
    self.distance_metric = distance_metric
    
    self.combined_data = self._prepare_data()

    self.distance_matrix = self._calculate_distance_matrix()
        
    super().__init__(
      n_var=self.total_accessions,
      n_obj=2,
      n_constr=1,
      xl=0,
      xu=1,
      vtype=int
    )

  def _prepare_data(self):
    genotype_clean = np.nan_to_num(self.genotype_data, nan=0.0)
    phenotype_clean = np.nan_to_num(self.phenotype_data, nan=0.0)
    
    scaler = StandardScaler()
    genotype_scaled = scaler.fit_transform(genotype_clean)
    phenotype_scaled = scaler.fit_transform(phenotype_clean)

    combined = np.hstack([genotype_scaled, phenotype_scaled])
    return combined

  def _calculate_distance_matrix(self):
    if self.distance_metric == 'euclidean':
      return euclidean_distances(self.combined_data)
    elif self.distance_metric == 'mahalanobis':
      cov = np.cov(self.combined_data, rowvar=False)
      try:
        inv_cov = np.linalg.inv(cov)
      except:
        inv_cov = np.linalg.pinv(cov)
            
        n = self.combined_data.shape[0]
            dist_matrix = np.zeros((n, n))
            for i in range(n):
                for j in range(i+1, n):
                    diff = self.combined_data[i] - self.combined_data[j]
                    dist = np.sqrt(diff.T @ inv_cov @ diff)
                    dist_matrix[i, j] = dist
                    dist_matrix[j, i] = dist
            return dist_matrix
        else:
            raise ValueError("Unsupported distance metric")

  def _evaluate(self, X, out, *args, **kwargs):
    # 评估每个解决方案的目标

def load_data(genotype_file, phenotype_file):
  # 从 Excel 文件加载基因型和表型数据

def run_corehunter(genotype_file, phenotype_file, core_size_ratio=0.2, pop_size=100, n_gen=200):
  genotype_data, phenotype_data, accession_names = load_data("geno.csv", "pheno.csv")
  problem = CoreHunterProblem(genotype_data, phenotype_data, core_size)
  
  algorithm = NSGA2(
    pop_size=pop_size,
    sampling=IntegerRandomSampling(),
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(prob=1.0, eta=20),
    eliminate_duplicates=True
  )

  res = minimize(
    problem,
    algorithm,
    ('n_gen', n_gen),
    seed=42,
    verbose=True
  )

  return res, accession_names, core_size

def analyze_results(res, accession_names, core_size):
  # 分析并可视化结果
