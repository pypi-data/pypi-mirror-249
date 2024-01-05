import json

import pandas as pd

from vtarget.language.app_message import app_message
from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class Rolling:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# ROLLING")

        column: str = settings["column"] if "column" in settings else None
        window: int = settings["window"] if "window" in settings else 1
        operation = settings["operation"] if "operation" in settings else None
        
        if not column:
            # TODO: Agregar a diccionario de idioma
            msg = "Column is required" #app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        if not operation:
            # TODO: Agregar a diccionario de idioma
            msg = "Operation is required" #app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        
        if column and operation:
            try:
                
                obj = df[column].rolling(window=window, min_periods=0, closed="right")
                
                if operation == "sum":
                    df["rolling"] = obj.sum()
                elif operation == "mean":
                    df["rolling"] = obj.mean()
                elif operation == "median":
                    df["rolling"] = obj.median()
                elif operation == "min":
                    df["rolling"] = obj.min()
                elif operation == "max":
                    df["rolling"] = obj.max()
                
                # TODO Agregar script
                # script.append(f'df["{new_column_name}"] = df[column_to_convert].dt.{to_extract}')

            except Exception as e:
                msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
                return bug_handler.default_on_error(flow_id, node_key, msg, str(e))

            cache_handler.update_node(
                flow_id,
                node_key,
                {
                    "pout": {"Out": df},
                    "config": json.dumps(settings, sort_keys=True),
                    "script": script,
                },
            )
            script_handler.script += script
            return {"Out": df}
        else:
            # TODO: Agregar a diccionario de idioma
            msg = "some of the properties have not been provided" #app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

