'''某投资者有100万元，可在3种资产中分配：

股票：预期收益15%，风险25%
债券：预期收益8%，风险10%
黄金：预期收益6%，风险15%

目标：

最大化总预期收益
最小化总投资风险

约束：
总投资额 = 100万元
每种资产投资比例 ≥ 0
股票投资 ≤ 总投资的60%'''

import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

def portfolio_optimization_weighted():
    """
    权重法解决多目标规划
    将多目标转化为单目标：加权求和
    """

    def objective(weights, alpha):
        """
        目标函数：alpha * 收益 - (1-alpha) * 风险
        alpha: 收益的权重 (0 ≤ alpha ≤ 1)
        """
        x1, x2, x3 = weights

        # 预期收益（最大化）
        expected_return = 0.15 * x1 + 0.08 * x2 + 0.06 * x3

        # 风险（最小化）
        risk = 0.25 * x1 + 0.10 * x2 + 0.15 * x3

        # 加权目标：最大化这个值
        return -(alpha * expected_return - (1 - alpha) * risk)

    # 约束条件
    constraints = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},  # 总投资比例=1
        {'type': 'ineq', 'fun': lambda x: 0.6 - x[0]}  # 股票≤60%
    ]

    # 变量边界
    bounds = [(0, 1), (0, 1), (0, 1)]

    # 初始猜测
    x0 = np.array([0.3, 0.4, 0.3])

    print("投资组合优化 - 权重法")
    print("=" * 60)
    print("权重α | 股票   | 债券   | 黄金   | 预期收益 | 风险   | 综合得分")
    print("-" * 60)

    pareto_front = []

    # 测试不同的权重组合
    for alpha in np.linspace(0, 1, 11):
        result = minimize(
            objective, x0, args=(alpha,),
            method='SLSQP', bounds=bounds, constraints=constraints
        )

        if result.success:
            x_opt = result.x
            return_opt = 0.15 * x_opt[0] + 0.08 * x_opt[1] + 0.06 * x_opt[2]
            risk_opt = 0.25 * x_opt[0] + 0.10 * x_opt[1] + 0.15 * x_opt[2]
            score = -result.fun

            pareto_front.append((return_opt, risk_opt, x_opt))

            print(f"{alpha:5.1f} | {x_opt[0]:5.3f} | {x_opt[1]:5.3f} | {x_opt[2]:5.3f} | "
                  f"{return_opt:7.3f} | {risk_opt:5.3f} | {score:8.3f}")

    return pareto_front


def portfolio_optimization_epsilon():
    """
    ε-约束法解决多目标规划
    将一个目标作为约束，优化另一个目标
    """

    def objective(weights):
        """最小化风险"""
        x1, x2, x3 = weights
        return 0.25 * x1 + 0.10 * x2 + 0.15 * x3

    # 基础约束
    constraints_base = [
        {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
        {'type': 'ineq', 'fun': lambda x: 0.6 - x[0]}
    ]

    bounds = [(0, 1), (0, 1), (0, 1)]
    x0 = np.array([0.3, 0.4, 0.3])

    print("\n投资组合优化 - ε约束法")
    print("=" * 70)
    print("最小收益要求 | 股票   | 债券   | 黄金   | 实际收益 | 风险   ")
    print("-" * 70)

    pareto_front_epsilon = []

    # 不同的最小收益要求
    for min_return in np.linspace(0.06, 0.12, 13):
        # 添加收益约束
        constraints = constraints_base + [
            {'type': 'ineq', 'fun': lambda x: 0.15 * x[0] + 0.08 * x[1] + 0.06 * x[2] - min_return}
        ]

        result = minimize(
            objective, x0,
            method='SLSQP', bounds=bounds, constraints=constraints
        )

        if result.success:
            x_opt = result.x
            return_opt = 0.15 * x_opt[0] + 0.08 * x_opt[1] + 0.06 * x_opt[2]
            risk_opt = result.fun

            pareto_front_epsilon.append((return_opt, risk_opt, x_opt))

            print(f"{min_return:11.3f} | {x_opt[0]:5.3f} | {x_opt[1]:5.3f} | {x_opt[2]:5.3f} | "
                  f"{return_opt:8.3f} | {risk_opt:6.3f}")

    return pareto_front_epsilon


def portfolio_sensitivity_analysis():
    """
    投资组合优化敏感性分析
    分析预期收益率变化对最优配置的影响
    """

    def portfolio_optimization(stock_return, bond_return, gold_return):
        """投资组合优化函数"""

        def objective(weights):
            x1, x2, x3 = weights
            expected_return = stock_return * x1 + bond_return * x2 + gold_return * x3
            risk = 0.25 * x1 + 0.10 * x2 + 0.15 * x3
            # 最大化收益风险比
            return -expected_return / (risk + 1e-6)

        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'ineq', 'fun': lambda x: 0.6 - x[0]}
        ]
        bounds = [(0, 1), (0, 1), (0, 1)]
        x0 = np.array([0.3, 0.4, 0.3])

        result = minimize(objective, x0, method='SLSQP',
                          bounds=bounds, constraints=constraints)

        if result.success:
            return result.x
        else:
            return None

    # 基础参数
    base_stock_return = 0.15
    base_bond_return = 0.08
    base_gold_return = 0.06

    print("投资组合敏感性分析")
    print("=" * 60)

    # 1. 股票收益率敏感性分析
    print("\n1. 股票收益率变化的影响:")
    print("股票收益率 | 股票配置 | 债券配置 | 黄金配置 | 预期收益 | 风险")
    print("-" * 65)

    stock_returns = np.linspace(0.10, 0.20, 11)
    stock_sensitivity = []

    for stock_ret in stock_returns:
        weights = portfolio_optimization(stock_ret, base_bond_return, base_gold_return)
        if weights is not None:
            x1, x2, x3 = weights
            expected_return = stock_ret * x1 + base_bond_return * x2 + base_gold_return * x3
            risk = 0.25 * x1 + 0.10 * x2 + 0.15 * x3
            stock_sensitivity.append((stock_ret, x1, x2, x3, expected_return, risk))

            print(f"{stock_ret:10.3f} | {x1:8.3f} | {x2:8.3f} | {x3:8.3f} | "
                  f"{expected_return:9.3f} | {risk:5.3f}")

    # 2. 债券收益率敏感性分析
    print("\n2. 债券收益率变化的影响:")
    print("债券收益率 | 股票配置 | 债券配置 | 黄金配置 | 预期收益 | 风险")
    print("-" * 65)

    bond_returns = np.linspace(0.05, 0.11, 11)
    bond_sensitivity = []

    for bond_ret in bond_returns:
        weights = portfolio_optimization(base_stock_return, bond_ret, base_gold_return)
        if weights is not None:
            x1, x2, x3 = weights
            expected_return = base_stock_return * x1 + bond_ret * x2 + base_gold_return * x3
            risk = 0.25 * x1 + 0.10 * x2 + 0.15 * x3
            bond_sensitivity.append((bond_ret, x1, x2, x3, expected_return, risk))

            print(f"{bond_ret:10.3f} | {x1:8.3f} | {x2:8.3f} | {x3:8.3f} | "
                  f"{expected_return:9.3f} | {risk:5.3f}")

    return stock_sensitivity, bond_sensitivity


# 运行敏感性分析
stock_sens, bond_sens = portfolio_sensitivity_analysis()

# 运行ε约束法
pareto_epsilon = portfolio_optimization_epsilon()

# 运行权重法
pareto_solutions = portfolio_optimization_weighted()