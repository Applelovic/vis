import numpy as np
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv(
        'covid_us.csv',
        usecols=[
            'date',
            'state',
            'death',
            'deathIncrease',
            'hospitalizedCurrently',
            'hospitalizedIncrease',
            'positive',
            'positiveIncrease',
        ],
        parse_dates=['date']
    )
    state_name = pd.read_csv('state_name.csv').set_index('state')
    popu = pd.read_csv('popu.csv').set_index('State')
    popu = pd.concat((popu, state_name), axis=1)
    popu.set_index('abbr', inplace=True)
    df['popu'] = df['state'].apply(lambda x: popu.loc[x, 'State Population'] if x in popu.index else np.nan)
    df['poli'] = df['state'].apply(lambda x: popu.loc[x, 'poli'] if x in popu.index else np.nan)
    df = df.loc[~pd.isna(df['popu'])]
    df.sort_values(['state', 'date'], inplace=True)
    kan = df.groupby('state').fillna(method='ffill')
    kan = pd.concat((kan, df.loc[:, 'state']), axis=1)
    kan = kan.loc[kan['date'] >= pd.to_datetime('2020-08-01')]
    kan.drop(['popu'], axis=1, inplace=True)
    incr = kan.loc[:, ['date', 'state', 'positiveIncrease', 'deathIncrease', 'hospitalizedIncrease', 'poli']]


