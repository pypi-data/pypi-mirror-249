import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

def time_series(df:pd.DataFrame):
    dts = pd.to_datetime(df['Date'])
    dates = df['Date'].to_list()
    df['Date'] = dts
    df = df.set_index('Date')
    cols = df.columns.tolist()

    high = 0
    high_index = 0
    low = 0
    low_index = 0
    recent = 0

    for col in cols:
        if '(focal)' in col:
            plt.plot(df.index, df[col], color='#FDB934', linewidth=3)
            high = df[col].max()
            low = df[col].min()
            recent = df[col].iloc[-1]
            for i in range(len(df[col].tolist())):
                if df[col][i] == low:
                    low_index = i
                if df[col][i] == high:
                    high_index = i
        else:
            plt.plot(df.index, df[col], color='#414042', linewidth=1)

    for d in range(len(dates)):
        if 'Jan' in dates[d]:
            dates[d] = 'Q1'
        if 'Apr' in dates[d]:
            dates[d] = 'Q2'
        if 'Jul' in dates[d]:
            dates[d] = 'Q3'
        if 'Oct' in dates[d]:
            dates[d] = 'Q4'

    years = []
    for d in dts:
        if d.year not in years:
            years.append(d.year)

    plt.gca().annotate(high, xy=(dts.iloc[high_index], high), color='green',
                       bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))
    plt.gca().annotate(low, xy=(dts.iloc[low_index], low), color='red',
                       bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))
    plt.gca().annotate(recent, xy=(dts.iloc[-1], recent),
                       bbox=dict(facecolor='white', edgecolor='black', boxstyle='circle'))
    plt.gca().plot(x_compat=True)
    plt.gca().set_xticklabels(dates)
    return plt.gcf()
