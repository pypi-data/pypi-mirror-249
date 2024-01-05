import json

import numpy as np
import pandas as pd

from vtarget.handlers.bug_handler import bug_handler
from vtarget.handlers.cache_handler import cache_handler
from vtarget.handlers.script_handler import script_handler
from vtarget.language.app_message import app_message


class Groupby:
    def exec(self, flow_id: str, node_key: str, pin: dict[str, pd.DataFrame], settings: dict):
        script = []

        df = pin["In"].copy()  # pyright: ignore
        script.append("\n# GROUPBY")

        def percentile(n):  # pyright: ignore
            def percentile_(x):
                return np.percentile(x, n)

            percentile_.__name__ = "q%s" % n
            return percentile_

        def count_distinct(x):  # pyright: ignore
            return x.nunique()

        def count_null(x):  # pyright: ignore
            return x.isnull().sum()

        def mode(x):  # pyright: ignore
            return x.value_counts().idxmax()

        def count_blank(x):  # pyright: ignore
            return sum(x == "")

        def count_not_blank(x):  # pyright: ignore
            return sum(x == "")

        # https://www.analyticsvidhya.com/blog/2020/03/groupby-pandas-aggregating-data-python/
        group_by_cols = settings["group_by"] if "group_by" in settings and settings["group_by"] else []
        aggs = settings["agg"] if "agg" in settings and settings["agg"] else []
        agg_cols = {}
        pctl_replaces2 = []
        rename_cols = {}

        for agg_method in aggs:
            action = agg_method["action"] if "action" in agg_method else None
            column = agg_method["column"] if "column" in agg_method else None
            
            if action and column:
                if action == "percentile":
                    pctl_value = agg_method["pctl_value"] if "pctl_value" else None
                    
                    if pctl_value:
                        fn_name = "quantile_{}".format(pctl_value)
                        action = fn_name
                        pctl_replaces2.append((fn_name, pctl_value))

                # Luego agrupo las funciones de agregación
                if column not in agg_cols:
                    agg_cols[column] = [action]
                else:
                    # Valido que no se agreguen agregaciones repetidas
                    if action not in agg_cols[column]:
                        agg_cols[column].append(action)

                # Creo el nombre compuesto entre la columna y la fn de agg para renombrar la columna
                current_name = column + "_" + action
                # rename_cols[current_name] = column # por defecto renombra sin "action" prop como sufijo
                
                # Si viene una columna de agregación con un renombre desde la vista
                if "rename" in agg_method and agg_method["rename"]:
                    rename_cols[current_name] = agg_method["rename"]
                else:
                    if "suffix" in agg_method and bool(agg_method["suffix"]) == False:
                        rename_cols[current_name] = column
            else:
                msg = "some of the properties of aggregate method have not been provided"
                return bug_handler.default_on_error(flow_id, node_key, msg, console_level="error")

        agg_str = str(agg_cols)
        for pr in pctl_replaces2:
            agg_str = agg_str.replace("'{}'".format(pr[0]), "percentile({})".format(pr[1]))
        if "count_distinct" in agg_str:
            agg_str = agg_str.replace("'count_distinct'", "count_distinct")
        if "count_null" in agg_str:
            agg_str = agg_str.replace("'count_null'", "count_null")
        if "mode" in agg_str:
            agg_str = agg_str.replace("'mode'", "mode")

        grouped = pd.DataFrame()
        try:
            if group_by_cols:
                grouped = eval("df.groupby(group_by_cols).agg({}).reset_index()".format(agg_str))
                # Dado que las columnas vienen en un multiIndex, con esto reseteo el indice
                grouped.columns = ["_".join(x) if str(x[1]) else str(x[0]) for x in grouped.columns]
                script.append("grouped = df.groupby({}).agg({}).reset_index()".format(group_by_cols, agg_str))
            else:
                grouped = eval("df.groupby(lambda _ : 1).agg({}).reset_index()".format(agg_str))
                grouped.columns = ["_".join(x) if str(x[1]) else str(x[0]) for x in grouped.columns]
                grouped.drop(columns=["index"], axis=1, inplace=True)
                script.append("grouped = df.groupby(lambda _ : 1).agg({}).reset_index()".format(agg_str))
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(e.args)})")

        try:
            grouped.rename(columns=rename_cols, inplace=True)
        except Exception as e:
            msg = app_message.dataprep["nodes"]["exception"](node_key, str(e))
            return bug_handler.default_on_error(flow_id, node_key, msg, f"{e.__class__.__name__}({', '.join(e.args)})")

        cache_handler.update_node(
            flow_id,
            node_key,
            {
                "pout": {"Out": grouped},
                "config": json.dumps(settings, sort_keys=True),
                "script": script,
            },
        )

        script_handler.script += script
        return {"Out": grouped}
