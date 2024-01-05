from importlib import import_module
import json
import os
from ..backtesting_custom import GenericBacktesting

class ModelSelector: 
    
    def __init__(self, 
                model_name: str= "macd", 
                model_folder: str="strategies",
                type_model: str="basic",
                configuration=None,
                path_model :str ="",
                symbol :str = "",
                df=None,
                interval=None, 
                mlflow=None
            ):
        
        self.mlflow = mlflow
        self.model_name = model_name
        self.model_folder = model_folder
        self.type_model = type_model
        self.configuration = configuration
        self.df = df
        self.path_model = path_model
        self.symbol = symbol
        self.interval = interval
        
        self.strategy_id=f"{self.model_name}_{symbol.lower()}_{interval}"


    def select(self):
        best_return = None
        # BASIC MODEL
        if self.type_model == "basic":
            
            Strategy = self.basic_models()
            
            # EXECUTE OPTIMIZATION IF NOT EXIST INSIDE OF THE FOLDER
            if os.path.isfile(f"{self.path_model}/params.json") == False:      
                strategy = Strategy(
                    strategy_name=self.model_name
                )
                
                method, best_return, best_parameters = strategy.experiment(
                    df=self.df
                )

                params = {
                    "type": self.type_model,
                    "method": method,
                    "best_return": best_return,
                    "best_parameters": list(best_parameters),
                    "params": list(best_parameters), 
                    "strategy": self.model_name
                }

                self.mlflow.set_tag("strategy", self.model_name)
                self.mlflow.set_tag("method", method)
                self.mlflow.log_param("optimized_params", json.dumps(params))
                self.mlflow.log_metric('best_return', best_return)
                
                df_actions = strategy.eval(df=self.df, params=best_parameters)
                
                back_testing = GenericBacktesting(
                    df=df_actions,
                    skip=True,
                    initial_money=2000.0,
                    commission=0.02,
                    plot_result=False,
                    path_save_result=self.path_model,
                    print_stacks=False
                )

                return_data, stats_json = back_testing.calculate_bk()

                for key, value in stats_json.items():
                    key_s = key.replace(" ",'').replace('[%]','').replace('.','').replace('&','').replace('[$]','').replace('(','').replace(')','').replace('#','')
                    if '_' not in key_s:
                        try:
                            self.mlflow.log_metric(key_s, value)
                        except Exception:
                            pass

                image_folder = self.path_model + "/images"

                if not os.path.exists(image_folder):
                    os.mkdir(image_folder)

                strategy.plot(df=df_actions, save_figure=True, show_graph=False, params=best_parameters, title=f"Strategy: {self.model_name} Return: {return_data}")
                

            else: 
                # Read params.json
                # MLfow
                params = {}
                # params = json.loads(open(f"{self.path_model}/params.json", "r").read())["best_parameters"]
                
            return Strategy, params, best_return
        
        
        
    def basic_models(self):
        
        libray_trading = f"pyttrading.strategies.{self.model_name}"

        model_module = import_module(libray_trading)
        
        strategy = getattr(model_module, "Strategy")
        
        return strategy
    
    
    def execute(self, df):
        
        _strategy, params, best_return = self.select()
        strategy = _strategy()
        df_action = strategy.eval(df=df, params=params.get('params'))
        
        return best_return, df_action
        
    
    
    
    
     
    
    
    