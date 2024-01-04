import pandas as pd
import numpy as np

class Strategy:

    def __init__(self, df=None, params=None):
        self.df = df

    def eval(self, df=None, params=None):
        df2 = df.copy()
        df2['actions'] = np.random.choice([0,1,2], size=len(df2), p=[0.7, 0.1, 0.2])
        return df2

    def objective_function(self, df=None, params=None):
        result_df = self.eval(df=df.copy())
        return result_df['actions'].sum()

    # def optimize(self, df=None, parms=None):
    def optimize(self, parms: list = [(5, 30), (10, 100)], initial_guess: list = [10, 20], df=None, method: str = "Nelder-Mead"):

        best_return = self.objective_function(df=df)
        return best_return

    def experiment(self, df=None, parms=[(5, 100), (40, 200)],initial_guess=[5, 40]):
        best_return = self.optimize(df=df)
        return best_return
