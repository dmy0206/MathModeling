'''给定物品的重量 weights 和价值 values，背包容量 capacity，求能装入的最大价值。

问题分析
状态定义：dp[i][w] 表示前i个物品在容量w下的最大价值

状态转移：

不选第i个物品：dp[i][w] = dp[i-1][w]

选第i个物品：dp[i][w] = dp[i-1][w-weights[i-1]] + values[i-1]

基础情况：dp[0][w] = 0'''
def knapsack(weights,values,capacity):
    n=len(weights)
    dp=[[0]*(capacity+1)for _ in range(n+1)]

    #动态规划求解过程：确定每个dp[i-1][j-1]递推
    for i in range(n+1):
        for j in range(capacity+1):
            if j<weights[i-1]:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = max(dp[i-1][j],dp[i-1][j-weights[i-1]]+values[i-1])
    return dp[n][capacity]



'''给定不同面额的硬币 coins 和总金额 amount，计算凑成总金额所需的最少硬币数。

问题分析
状态定义：dp[i] 表示凑成金额 i 所需的最少硬币数

状态转移：dp[i] = min(dp[i - coin] + 1) for coin in coins

基础情况：dp[0] = 0'''

def coin_change(coins,amount):
    dp=[float('inf')for _ in range(amount+1)]
    dp[0]=0

    #遍历所有金额
    for i in range(1,amount+1):
        for coin in coins:
            if i>=coin:
                dp[i]=min(dp[i],dp[i-coin]+1)

    return dp[amount] if dp[amount]!=float('inf')else -1


#测试部分
if __name__=="__main__":
    weights=[2,3,4,5]
    values=[3,4,5,6]
    capacity=5
    max_value=knapsack(weights,values,capacity)
    print(f"最大可装入价值为:{max_value}")
    coins = [1, 2, 5]
    amount = 11
    result = coin_change(coins, amount)
    print(f"凑成金额 {amount} 需要的最少硬币数: {result}")  # 3 (5+5+1)