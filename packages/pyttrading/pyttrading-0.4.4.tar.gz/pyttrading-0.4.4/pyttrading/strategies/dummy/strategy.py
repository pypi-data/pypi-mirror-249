import pandas as pd
import numpy as np

class DummyStrategy:

    def __init__(self, df=None):
        self.df = df

    def eval(self, df=None):
        signal_distribution = [0, 1, 2]
        signal_probabilities = [0.7, 0.1, 0.2]
        df['actions'] = np.random.choice(signal_distribution, size=len(df), p=signal_probabilities)
        return df

    def objective_function(self, df=None):
        result_df = self.eval(df=df.copy())
        return result_df['actions'].sum()

    def optimize(self, df=None):
        best_return = self.objective_function(df=df)
        return best_return

    def experiment(self, df=None):
        best_return = self.optimize(df=df)
        return best_return
