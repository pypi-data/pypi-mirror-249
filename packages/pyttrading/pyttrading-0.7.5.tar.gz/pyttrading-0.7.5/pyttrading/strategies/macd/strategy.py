from ...backtesting_custom.generic_backtesting import GenericBacktesting
from ...utils.pre_processing import remove_noise_trading
from scipy.optimize import minimize
from ta.trend import MACD

class Strategy:
    def __init__(self, df=None):
        pass
    
    def eval(self, df=None, params= [26, 12, 9]):
        
        if len(params) != 3:
            print(f"Print error")
            return False
        
        window_slow, window_fast, window_sign = params
        
        window_slow = int(window_slow)
        window_fast = int(window_fast)
        window_sign = int( window_sign)
        
        print(f"window_slow: {window_slow}, window_fast: {window_fast}, window_sign: {window_sign}")
        # Calcular el indicador MACD
        
        try:
            macd = MACD(df['close'], 
                    window_slow=window_slow, 
                    window_fast=window_fast, 
                    window_sign=window_sign,
                    fillna=True
                ) 
        except:
            print(f"Error en el calculo del MACD")
            return False
        
        macd = MACD(df['close'], 
                    window_slow=window_slow, 
                    window_fast=window_fast, 
                    window_sign=window_sign,
                    fillna=True
                )
        
        df['macd_line'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df.loc[(df['macd_line'] > df['macd_signal']) & (df['macd_line'].shift() <= df['macd_signal'].shift()), 'actions'] = 1  # Señal de compra
        df.loc[(df['macd_line'] < df['macd_signal']) & (df['macd_line'].shift() >= df['macd_signal'].shift()), 'actions'] = 2  # Señal de venta
        df['actions'] = df['actions'].mask(df['actions'].eq(df['actions'].shift()))
        df['actions'] = df['actions'].fillna(0)
        df['actions'] = remove_noise_trading(actions=df['actions'])
        
        
        return df
    
    def objective_function(self, params=[26, 12, 9], df=None):
        
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
        
        return -return_data
    
    def optimize(self, params: list = [(6, 100), (4, 100), (4, 100)], initial_guess: list = [6, 4, 4], df=None, method: str = "Nelder-Mead"):
        threshold_bounds = params
        result = minimize(self.objective_function, initial_guess, bounds=threshold_bounds, args=(df,), method=method)
        best_macd_parameters = result.x
        best_return = -result.fun
        return best_return, best_macd_parameters
    
    def experiment(self, df=None, params=[(6, 100), (4, 100), (4, 100)], initial_guess=[6, 4, 4]):
        
        methods_list = [
            'Nelder-Mead',
            'Powell',
            'CG',
            'L-BFGS-B',
            'COBYLA',
            'trust-constr'
        ]
        results_methods = {}
        results_method_list = []
        result_method_name = []
        
        for method in methods_list:
            print(f"Method: {method}")
            best_return, best_macd_parameters = self.optimize(params=params, initial_guess=initial_guess, df=df, method=method)
            results_method_list.append(best_return)
            result_method_name.append(method)
            results_methods[method] = best_return, best_macd_parameters
        
        # Obtener el máximo valor de results_method_list
        optimize = results_method_list.index(max(results_method_list))
        method = result_method_name[optimize]
        best_return, best_macd_parameters = results_methods[method]
        
        return method, best_return, best_macd_parameters
