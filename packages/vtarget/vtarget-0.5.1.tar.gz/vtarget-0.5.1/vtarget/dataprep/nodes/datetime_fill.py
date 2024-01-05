import json

import pandas as pd

from vtarget.language.app_message import app_message
from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler

class DatetimeFill:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pin["In"].copy()
        script.append("\n# DATETIME FILL")

        time_column: str = settings["time_column"] if "time_column" in settings else None
        key_columns: list = settings["key_columns"] if "key_columns" in settings else []
        frequency = settings["frequency"] if "frequency" in settings else None
        
        if not time_column:
            # TODO: Agregar a diccionario de idioma
            msg = "Time column is required" #app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        if not key_columns:
            # TODO: Agregar a diccionario de idioma
            msg = "Key columns list is required" #app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        if not frequency:
            # TODO: Agregar a diccionario de idioma
            msg = "Frequency is required" #app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        
        if time_column and key_columns and frequency:
            try:
                df = df.set_index([time_column] + key_columns).unstack(fill_value=0).asfreq(frequency, fill_value=0).stack().sort_index(level=1).reset_index()
                
                # TODO Agregar script
                # script.append(f"")

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

