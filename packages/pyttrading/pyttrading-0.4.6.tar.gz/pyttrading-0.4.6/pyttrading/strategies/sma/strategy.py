from ...backtesting_custom.generic_backtesting import GenericBacktesting
from ...utils.pre_processing import remove_noise_trading
from scipy.optimize import minimize
from ta.trend import SMAIndicator

class Strategy: 
    def __init__(self, df=None):
        pass         

    def eval(self, df=None, params=[10, 30]):
        
        if len(params) != 2:
            print(f"Print error")
            return False
        
        fast_ma_period, slow_ma_period = params
        
        print(f"fast_ma_period: {fast_ma_period} slow_ma_period: {slow_ma_period}")
        # Calcular el rango de ruptura (breakout range)
        df['fast_ma'] = SMAIndicator(df['close'], int(fast_ma_period), True).sma_indicator()
        df['slow_ma']  = SMAIndicator(df['close'], int(slow_ma_period), True).sma_indicator()
        df['actions'] = 0  # Inicializar todas las acciones como "mantener"
        df.loc[df['fast_ma'] > df['slow_ma'], 'actions'] = 1  # Señal de compra
        df.loc[df['fast_ma'] < df['slow_ma'], 'actions'] = 2  # Señal de venta
        # Eliminar señales consecutivas repetidas
        df['actions'] = df['actions'].mask(df['actions'].eq(df['actions'].shift()))
        # Reemplazar NaN por 0
        df['actions'] = df['actions'].fillna(0)
        
        df['actions'] = remove_noise_trading(actions=df['actions'])
        
        
        return df
    
    def objective_function(self, params=[10,30], df=None):
        # Apply the strategy with the current parameters
        
        result_df = self.eval(df=df.copy(), params=params)
        
        back_testing = GenericBacktesting(
            df=result_df,
            skip=True,
            initial_money=2000.0,
            commission=0.02,
            plot_result=False,
            path_save_result=".",
            print_stacks=False
        )
        return_data, _ = back_testing.calculate_bk()
        # Minimize the negative return to maximize the return
        return -return_data
    
    def optimize(self, parms: list = [(5, 30), (10, 100)], initial_guess: list = [10, 20], df=None, method: str = "Nelder-Mead"):
        
        threshold_bounds = parms
        
        result = minimize(self.objective_function, initial_guess, bounds=threshold_bounds, args=(df), method=method)
        
        best_breakout_threshold = result
        
        best_return = -result.fun

        return best_return, best_breakout_threshold
    
    
    def experiment(self, df=None, parms=[(5, 100), (40, 200)],initial_guess=[5, 40]):
        
        methods_list = [
            'Nelder-Mead',
            'Powell',
            'CG',
            # 'BFGS',
            'L-BFGS-B',
            # 'TNC',
            'COBYLA',
            # 'SLSQP',
            'trust-constr',
            # 'dogleg',
            # 'trust-ncg',
            # 'trust-exact',
            # 'trust-krylov'
        ]
        
        results_methods = {}
        results_method_list = []
        result_method_name = []
        
        for method in methods_list:
            print(f"Method: {method}")
    
            best_return, best_sma_threshold = self.optimize(
                parms=parms, 
                initial_guess=initial_guess,
                df=df, 
                method=method
            )
    
            results_method_list.append(best_return)
            result_method_name.append(method)
    
            results_methods[method] = best_return, best_sma_threshold.x
            

        # get the max value of results_method_list
        optimize = results_method_list.index(max(results_method_list))
        method = result_method_name[optimize]
        best_return, best_sma_threshold = results_methods[method]
        
        return method, best_return, best_sma_threshold