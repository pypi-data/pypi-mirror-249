import pandas as pd
import numpy as np

class Strategy:

    def __init__(self, df=None, params=None):
        self.df = df

    def eval(self, df=None, params=None):
        df = df.copy()
        df['actions'] = np.random.choice([0,1,2], size=len(df), p=[0.7, 0.1, 0.2])
        return df

    def objective_function(self, df=None, params=None):
        result_df = self.eval(df=df.copy())
        return result_df['actions'].sum()

    def optimize(self, df=None, parms=None):
        best_return = self.objective_function(df=df)
        return best_return

    def experiment(self, df=None, parms=None):
        best_return = self.optimize(df=df)
        return best_return
