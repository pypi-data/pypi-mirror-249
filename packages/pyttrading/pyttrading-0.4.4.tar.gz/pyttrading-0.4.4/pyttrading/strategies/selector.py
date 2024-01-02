
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

    def adjust_chart_density(self, graph_generator, width, df_actions, height, scale, is_dark):
        pass
        # if width < 700:
        #     # Limitar la cantidad de datos mostrados
        #     df_subset = df_actions.sample(frac=0.5)  # Muestra solo la mitad de los datos
        #     self.graph_generator = GraphGenerator(
        #         df=df_subset, 
        #         df_test=None,
        #         configuration=self.configuration,
        #         width=width, height=height, scale=scale,
        #         is_dark=is_dark == "dark"
        #     )

        #     # Reducir el tamaño de fuente
        #     font_size = 8
        #     graph_generator.fig.update_xaxes(tickfont=dict(size=font_size))
        #     graph_generator.fig.update_yaxes(tickfont=dict(size=font_size))

        #     # Aumentar el espaciado
        #     line_width = 1
        #     graph_generator.candlestick.line = dict(width=line_width)


    def select(self):
        best_return = None
        # BASIC MODEL
        if self.type_model == "basic":
            
            Strategy = self.basic_models()
            
            # EXECUTE OPTIMIZATION IF NOT EXIST INSIDE OF THE FOLDER
            if os.path.isfile(f"{self.path_model}/params.json") == False:      
                strategy = Strategy()
                
                method, best_return, best_sma_threshold = strategy.experiment(
                    df=self.df
                )

                params = {
                    "type": self.type_model,
                    "method": method,
                    "best_return": best_return,
                    "best_sma_threshold": list(best_sma_threshold),
                    "params": list(best_sma_threshold), 
                    "strategy": self.model_name
                }


                self.mlflow.set_tag("strategy", self.model_name)
                self.mlflow.set_tag("method", method)

                self.mlflow.log_param("optimized_params", json.dumps(params))
                
                self.mlflow.log_metric('best_return', best_return)
                
                df_actions = strategy.eval(df=self.df, params=best_sma_threshold)
                
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


                sizes = [
                    {   
                        "width": 400,
                        "height": 300,
                        "scale": 1,
                        "length": 0.3
                    },
                    {   
                        "width": 700,
                        "height": 450,
                        "scale": 1,
                        "length": 0.4
                    },
                    {   
                        "width": 1000,
                        "height": 600,
                        "scale": 1,
                        "length": 1
                    },
                    {   
                        "width": 1200,
                        "height": 700,
                        "scale": 1,
                        "length": 1
                    }
                ]
                is_dark_mode = [
                    "dark", 
                    "light"
                ]

                for is_dark in is_dark_mode:
                    for size in sizes:
                        width = size.get('width')
                        height = size.get('height')
                        scale = size.get('scale')
                        length = size.get('length')

                        image_path = f"{self.path_model}/images/chart_{width}x{height}_{is_dark}.html"
                        print(image_path)

                        # TODO fix the graph
                        # graph_generator = GraphGenerator(
                        #     # df=df_actions, 
                        #     df=df_actions.tail(int(len(df_actions) * length)), 
                        #     df_test=None,
                        #     configuration=self.configuration,
                        #     width=width, height=height, scale =scale,
                        #     is_dark=is_dark == "dark"
                        # )

                        # graph_generator.plot_actions(path=image_path)
                


            else: 
                # Read params.json
                # MLfow
                params = {}
                # params = json.loads(open(f"{self.path_model}/params.json", "r").read())["best_sma_threshold"]
                
            return Strategy, params, best_return
        
        
        
    def basic_models(self, basic_folder: str="basic"):
        
        libray_trading = f"pyttrading.strategies.{self.model_name}"

        model_module = import_module(libray_trading)
        
        strategy = getattr(model_module, "Strategy")
        
        return strategy
    
    
    def execute(self, df):
        
        Strategy, params, best_return = self.select()
        strategy = Strategy()
        df_action = strategy.eval(df=df, params=params.get('params'))
        
        return best_return, df_action
        
    
    
    
    
     
    
    
    