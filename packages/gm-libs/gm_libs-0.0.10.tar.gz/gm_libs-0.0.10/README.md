# 掘金量化的简化函数包（第三方）

个人自用包，出问题了欢迎提 Issue。

## 功能列表

### A 股

#### 获取信息

1. 获取所有指数（股票市场、当前有效）: get_all_index
2. 获取所有股票（股票市场、当前有效）: get_all_security
3. ~~获取龙虎榜股票列表: get_dragon_tiger_list~~

#### 执行交易

1. 买指定数量的股票: buy_count(stock: str, count: int, price: float)
2. 卖指定数量的股票: sell_count(stock: str, count: int, price: float)
3. 调整仓位（到特定数量）: order_target_count(stock: str, volume: int, price: float)
4. 调整仓位（到特定价值）: order_target_money(stock: str, worth: int, price: float)

#### 记录日志

1. 日志输出且保存: log_all，兼容 gm.log
2. 日志不输出仅保存: log_save，兼容 gm.log
3. 日志输出不保存，gm.print 即可

## 打包

1. 更新 [pyproject.toml](pyproject.toml) 文件
2. 执行 `python -m build`
3. 执行 `python -m twine upload dist/*`
4. 对输入框，输入账号: `__token__` 并回车
5. 最后输入 API token 即可
