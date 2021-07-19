# how to do quantile distribution and normalize the data
numQuantiles = 20
colsQuantiles = [
    "balance",
    "transaction_sum_amount",
    "debit_transaction_amount",
    "credit_transaction_amount",
]


def createQuantiles(dfColumn, numQuantiles):
    return pd.qcut(dfColumn, numQuantiles, labels=False, duplicates="drop")


for string in colsQuantiles:
    df12[string] = createQuantiles(df12[string], numQuantiles)


def minMaxScaler(numArr):
    minx = np.min(numArr)
    maxx = np.max(numArr)
    numArr = (numArr - minx) / (maxx - minx)
    return numArr


for string in colsQuantiles:
    df12[string] = minMaxScaler(df12[string])
