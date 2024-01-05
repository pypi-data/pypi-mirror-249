import json

import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
# from vtarget.language.app_message import app_message

class Sample:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        df_A: pd.DataFrame = pd.DataFrame()
        df_B: pd.DataFrame = pd.DataFrame()
        
        script.append("\n# SAMPLE")

        random_pct: float = settings["random_pct"] if "random_pct" in settings else None
        first_pct: float = settings["first_pct"] if "first_pct" in settings else None
        last_pct: float = settings["last_pct"] if "last_pct" in settings else None
        random_n: float = settings["random_n"] if "random_n" in settings else None
        first_n: float = settings["first_n"] if "first_n" in settings else None
        last_n: float = settings["last_n"] if "last_n" in settings else None        
        
        if random_pct:
            df_A = df.sample(int(len(df) * random_pct / 100))
        elif random_n:
            df_A = df.sample(int(random_n))
        elif first_pct:
            df_A = df[:(int(len(df) * first_pct / 100))]
        elif last_pct:
            df_A = df[-(int(len(df) * last_pct / 100)):]
        elif first_n:
            df_A = df[:int(first_n)]
        elif last_n:
            df_A = df[-int(last_n):]
        else:
            # TODO: Pancho, agregar mensaje al dicc de idioma
            msg = "Debes ingresar una muestra válida"
            # msg = app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        
        # Obtengo el complemento (la parte negada de la condición)
        df_B = df[~df.index.isin(df_A.index)]
        
        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"A": df_A, "B": df_B},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"A": df_A, "B": df_B}
