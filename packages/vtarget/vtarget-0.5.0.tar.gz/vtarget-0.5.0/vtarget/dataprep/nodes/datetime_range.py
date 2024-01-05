import json

import pandas as pd

from vtarget.language.app_message import app_message
from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler


class DatetimeRange:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df: pd.DataFrame = pd.DataFrame()
        script.append("\n# DATETIME RANGE")

        start_date = settings["start_date"] if "start_date" in settings else None
        end_date = settings["end_date"] if "end_date" in settings else None
        frequency = settings["frequency"] if "frequency" in settings else None
        
        if not start_date:
            # TODO: Agregar a diccionario de idioma
            msg = "Start Date is required" #app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        if not end_date:
            # TODO: Agregar a diccionario de idioma
            msg = "End Date is required" #app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        if not frequency:
            # TODO: Agregar a diccionario de idioma
            msg = "Frequency is required" #app_message.dataprep["nodes"]["missing_column"](node_key)
            return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")
        
        if start_date and end_date and frequency:
            try:
                
                df["date_range"] = pd.date_range(start=start_date, end=end_date, freq=frequency)
                script.append(f"df['date_range'] = pd.date_range(start='{start_date}', end='{end_date}', freq={frequency}")

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

