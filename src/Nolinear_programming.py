import numpy as np
from scipy.optimize import minimize

def total_profit(production):
    """
    计算总利润函数
    参数: production = [x, y] 产品A和B的产量
    返回: 总利润（负值，因为minimize是求最小化）
    """
    x, y = production
    profit_A = 50*x - 0.1*x**2  # 产品A的利润
    profit_B = 60*y - 0.2*y**2  # 产品B的利润
    total = profit_A + profit_B
    return -total  # 负号是因为我们要最大化利润

def resource_constraint(production):
    """
    资源约束: 2x + 3y ≤ 120
    转换为: 120 - (2x + 3y) ≥ 0
    """
    x, y = production
    return 120 - (2*x + 3*y)

def min_production_constraint(production):
    """
    最低产量约束: x + y ≥ 30
    转换为: (x + y) - 30 ≥ 0
    """
    x, y = production
    return (x + y) - 30

# 初始猜测值
x0 = np.array([20, 20])  # 假设初始各生产20个单位

# 约束条件定义
constraints = [
    # 资源约束（不等式约束 ≥0）
    {'type': 'ineq', 'fun': resource_constraint},
    # 最低产量约束（不等式约束 ≥0）
    {'type': 'ineq', 'fun': min_production_constraint}
]

# 变量边界（产品A和B的产量上下限）
bounds = [
    (0, 50),  # 0 ≤ x ≤ 50
    (0, 40)   # 0 ≤ y ≤ 40
]

# 求解优化问题
result = minimize(
    fun=total_profit,      # 目标函数
    x0=x0,                 # 初始猜测
    method='SLSQP',        # 序列二次规划法，适合约束优化
    bounds=bounds,         # 变量边界
    constraints=constraints # 约束条件
)

# 结果解析
print("=" * 50)
print("产品生产优化问题求解结果")
print("=" * 50)

if result.success:
    optimal_x, optimal_y = result.x
    max_profit = -result.fun  # 转换回正值

    print(f"✅ 优化成功!")
    print(f"📊 最优生产方案:")
    print(f"   产品A产量: {optimal_x:.1f} 个单位")
    print(f"   产品B产量: {optimal_y:.1f} 个单位")
    print(f"💰 最大总利润: {max_profit:.2f} 元")

    # 验证约束条件
    print("\n🔍 约束条件验证:")
    print(f"   资源使用: 2×{optimal_x:.1f} + 3×{optimal_y:.1f} = {2 * optimal_x + 3 * optimal_y:.1f} ≤ 120")
    print(f"   产品A上限: {optimal_x:.1f} ≤ 50")
    print(f"   产品B上限: {optimal_y:.1f} ≤ 40")
    print(f"   最低产量: {optimal_x:.1f} + {optimal_y:.1f} = {optimal_x + optimal_y:.1f} ≥ 30")

    # 各产品利润分析
    profit_A = 50 * optimal_x - 0.1 * optimal_x ** 2
    profit_B = 60 * optimal_y - 0.2 * optimal_y ** 2
    print(f"\n📈 利润分析:")
    print(f"   产品A利润: {profit_A:.2f} 元")
    print(f"   产品B利润: {profit_B:.2f} 元")
    print(f"   利润比例: A占 {profit_A / max_profit * 100:.1f}%, B占 {profit_B / max_profit * 100:.1f}%")

else:
    print("❌ 优化失败!")
    print(f"错误信息: {result.message}")

print("=" * 50)