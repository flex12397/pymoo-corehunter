class CoreHunterProblem(Problem):
  def __init__(self, genotype_data, phenotype_data, core_size, distance_metric='euclidean'):
    # Genotype_data + phenotype_data -> numpy
    # 计算所有种质之间的距离矩阵

  def _prepare_data(self):
    # “准备并标准化组合的基因型和表型数据”

  def _calculate_distance_matrix(self):
    # 计算所有种质之间的距离矩阵

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
