# Pymoo

## Python 多目标优化

<div class="presenter-footer">
Felix Li • <a href="mailto:felix.li12397@gmail.com">felix.li12397@gmail.com</a>
</div>

---

## Pymoo介绍

- 优化 -> 工程、数据、科学、人工智能
- 相关作品：jMetalPy、PyGMO、Platypus、DEAP、Inspyred
- Pymoo同时: 多目标优化、可视化、做决策
- 模块化和可扩展性：“即插即用”设计

--

## Pymoo建筑
![建筑](./images/Table1.png)

---

## 建筑主要模块

1.	Problems（处理问题）
-	问题设计的启示，自动微分梯度和并行化计算

2.	Optimization (优化)
-	为算法提供了进化算子、处理约束的方法、分解策略以及终止准则

3.	Analytics（分析）
-	提供可视化、性能指标和决策支持工具

---

## Problems（处理问题）

-	提供测试问题（单目标、多目标、超多目标），用于算法开发和基准测试
-	问题的梯度都使用自动微分 (Autograd) 自动计算
-	只需在输出请求中添加一个 "d" (return_value_of = ["F", "dF"] )

---

## Problems（处理问题）

### 并行化计算

-	pymoo 提供了多种内置策略来实现并行化：
  - 向量化（vectorize）：使用NumPy操作来同时处理整个种群矩阵
  - 多线程（threaded）：使用爬虫的线程池来并行评估种群中的每个解
  - 分布式（Dask）： 将不同的解发送到不同的机器上进行评估

---

## Optimization（优化）：进化算子

![建筑](./images/Table1Outline.png)

---

## Sampling（采取）

- 目的：创建候选解的初始种群
- 支持对实数、整数、和而今此变量的随机采样
- 还为实数变量提供**拉丁超立方采样**（LHS）

---

## Crossover（交叉）

- 目的：结合两个父代的遗传信息创新新的后代
1. 二进制/字符串变量：
  - 使用经典算子：单点、两点、均匀 (UX)、拌均匀 (HUX)
  - 原理：交换片段或随机从每个附带选择位
![建筑](./images/binaries.png)

