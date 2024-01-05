# TODO: Importar el language acá


class __AppMessage:
    def __init__(self, languaje):
        if languaje == "es":
            self.dataprep = self.dataprep_spanish()
            self.dataviz = self.dataviz_spanish()
            self.autots = self.autots_spanish()
            self.automl = self.automl_spanish()
            self.handlers = self.handlers_spanish()
            self.utils = self.utils_spanish()
            self.worker = self.worker_spanish()
            self.service = self.service_spanish()
        else:
            self.dataprep = self.dataprep_english()
            self.dataviz = self.dataviz_english()
            self.autots = self.autots_english()
            self.automl = self.automl_english()
            self.handlers = self.handlers_english()
            self.utils = self.utils_english()
            self.worker = self.worker_english()
            self.service = self.service_english()

    # ===================================
    # Spanish
    # ===================================
    def dataprep_spanish(self):
        return {
            "nodes": {
                "code": {
                    "no_vtg_codeout": lambda node_key: f"({node_key}): Debes llamar a la función vtg_codeout(Df) con tu DataFrame de salida",
                },
                "column": {
                    "no_columns_selected": lambda node_key: f"({node_key}): No hay columnas seleccionadas",
                    "rename_columns": lambda node_key: f"({node_key}): No fue posible renombrar las columnas",
                    "column_not_in_df": lambda node_key, column: f"({node_key}): La columna '{column}' no existe en el Dataframe",
                },
                "dtype": {
                    "no_columns_selected": lambda node_key: f"({node_key}): No hay columnas seleccionadas",
                    "rename_columns": lambda node_key: f"({node_key}): No fue posible renombrar las columnas",
                    "column_not_in_df": lambda node_key, column: f"({node_key}): La columna '{column}' no existe en el Dataframe",
                    "change_dtype": lambda node_key, column, dtype: f"({node_key}): No fue posible transformar el tipo de dato de la columna '{column}' a '{dtype}'",
                    "unknow_dtype": lambda node_key, column, dtype: f"({node_key}): Tipo de dato '{dtype}' desconocido. Columna '{column}' se mantiene como string",
                },
                "concat": {
                    "column_required": lambda node_key, port: f"({node_key}): Debes mantener al menos un campo en la entrada '{port}'",
                },
                "corss_join": {
                    "column_required": lambda node_key, port: f"({node_key}): Debes mantener al menos un campo en la entrada '{port}'",
                },
                "cumsum": {
                    "aggregation_required": lambda node_key: f"({node_key}): Debes seleccionar al menos un método de agregación",
                },
                "database_write": {
                    "source_required": lambda node_key: f"({node_key}): Debes seleccionar un recurso de conexión",
                },
                "database": {
                    "source_required": lambda node_key: f"({node_key}): Debes seleccionar un recurso de conexión",
                },
                "datetime_extract": {},
                "datetime_formatter": {
                    "pattern_quotes": lambda node_key: f"({node_key}): El patrón personalizado debe venir entre comillas",
                    "pattern_required": lambda node_key: f"({node_key}): Debes seleccionar al menos un formato",
                },
                "describe": {},
                "df_maker": {},
                "email": {
                    "config_required": lambda node_key, fields: f"({node_key}): Debes completar todos los campos en la configuración. Campos faltantes {fields}",
                    "failed_send": lambda node_key: f"({node_key}): No fue posible realizar el envío de email",
                    "size_max": lambda node_key: f"({node_key}): No es posible enviar el correo ya que el tamaño de los archivos adjuntos supera el límite máximo",
                },
                "excel": {
                    "failed_generate": lambda node_key: f"({node_key}): No fue posible generar el archivo excel",
                },
                "filter": {
                    "rules": lambda node_key: f"({node_key}): No se ha creado ninguna una regla",
                    "unknow_rule": lambda node_key, rule: f"({node_key}): No se reconoce la regla '{rule}'",
                    "failed_condition": lambda node_key: f"({node_key}): No fue posible procesar la condición",
                    "unknow_column": lambda node_key, field: f"({node_key}): No existe la columna '{field}' en el Dataframe de entrada",
                    "unknow_operator": lambda node_key, operator: f"({node_key}): Operador '{operator}' no reconocido ",
                },
                "input_data": {
                    "unknow_format": lambda node_key, format: f"({node_key}): Formato '{format}' no reconocido",
                    "end_start_spaces": lambda node_key: f"({node_key}): Archivo fuente contiene espacios al inicio o final del nombre de una o más columnas. Se ha corregido para la lectura",
                },
                "inter_row": {
                    "fillna": lambda node_key: f"({node_key}): Si seleccionas la función 'fillna', debes especificar el valor para los nulos",
                },
                "merge": {
                    "input_port": lambda node_key: f"({node_key}): Puerto entrada iL o iR no conectado",
                    "input_port_il": lambda node_key, col: f"({node_key}): La columna '{col}' no está en las columnas del Dataframe iL",
                    "input_port_iR": lambda node_key, col: f"({node_key}): La columna '{col}' no está en las columnas del Dataframe iR",
                },
                "pivot": {
                    "incompleted_fields": lambda node_key, missing: f"({node_key}): Faltan campos de la configuración. Campos faltantes: {missing}",
                },
                "switch": {
                    "default_value": lambda node_key: f"({node_key}): Falta el valor por defecto",
                },
                #
                "database_utilities": {
                    "source_required": lambda node_key: f"({node_key}): Debes seleccionar un recurso de conexión",
                    "check_missing_source": lambda node_key: f"({node_key}): El recurso de conexión no se encuentra",
                    "check_fields_to_connection": lambda node_key, field: f"({node_key}): Falta la columna '{field}' para establecer la conexión",
                    "check_empty_fields": lambda node_key, field: f"({node_key}): La columna '{field}' se encuentra vacía",
                    "check_optional_fields": lambda node_key, field: f"({node_key}): Faltan campos para establecer conexión",
                },
                "deploy_enabled": lambda node_key: f"({node_key}): El deploy_mode está habilitado en el flujo, pero deploy_path no existe en la configuración del nodo",
                "exception": lambda node_key, error: f"({node_key}) Error: " + error,
                "missing_column": lambda node_key: f"({node_key}): Debes seleccionar al menos una columna",
            },
            "builder": {
                "reset_cache": lambda flow_name: f"Caché reseteada para el flujo '{flow_name}'",
                "nodes_in_cache": lambda q_nodes: f"'{q_nodes}' Nodos en caché",
                "not_send": lambda node_key: f"Se omite envío para nodo '{node_key}'",
                "skip_writing": lambda node_key: f"Se omite escritura de archivo para nodo '{node_key}'",
                "parent_without_entry": lambda node_key: f"Se omite nodo '{node_key}' sin entrada padre",
                "save_cache": lambda q_nodes: f"Se almacenaron '{q_nodes}' nodos en caché",
                "processed_flow": lambda seconds: f"Flujo procesado en '{seconds}' segundos",
                "exec_flow": "El flujo aún no se ha ejecutado",
                "max_rows": lambda node_key, max_rows: f"({node_key}): Se ha exedido el máximo de filas permitido ({f'{max_rows:_}'.replace('_','.')})",
            },
        }

    def dataviz_spanish(self):
        return {
            "data_source_reader": {
                "not_memory_flow": lambda node_key, flow_name: f"La fuente de datos del nodo '{node_key}' en el flujo '{flow_name}' No está en memoria. Por favor Corre el flujo en el módulo Dataprep",
                "no_such_file": lambda file_path: f"No se encuentra el archivo '{file_path}'",
                "unspecified_extension": f"El archivo debe tener alguna extensión",
                "invalid_extension": lambda extensions: f"Las extensiones permitidas son: '{extensions}'",
            },
            "data_frame_operator": {
                "specified_operation": "Not specified operation in the metric",
                "invalid_operation": lambda operation, operation_dict: f"La operación '{operation}' es inválida'. Peraciones permitidas: '{operation_dict}'",
                "field_numeric": lambda operation, field_name: f"La operación '{operation}' requiere que el campo '{field_name}' sea númerico",
            },
        }

    def autots_spanish(self):
        return {
            "autots": {
                "not_train": "Aún no se ha realizado el entrenamiento",
                "not_path": lambda pickle: f"{pickle}: Ruta no existe",
            },
            "train": {},
            "exception": lambda error: f"Error: " + error,
        }

    def automl_spanish(self):
        return {
            "automl": {
                "not_train": "Aún no se ha realizado el entrenamiento",
                "not_path": lambda pickle: f"{pickle}: Ruta no existe",
            },
            "exception": lambda error: f"Error: " + error,
        }

    def handlers_spanish(self):
        return {
            "cache_handler": {
                "node_cache_saved": lambda node_key: f"({node_key}) Almacenado en cache",
                "node_ram_saved": lambda node_key: f"({node_key}) Almacenado en RAM",
            },
            "exception": lambda error: f"Error: " + error,
        }

    def utils_spanish(self):
        return {
            "utilities": {
                "var_not_in_df": lambda prop: f"La columna '{prop}' no está en el Df",
            },
            "exception": lambda error: f"Error: " + error,
        }

    def worker_spanish(self):
        return {
            "listener": {
                "automl": {
                    "get_interaction": {
                        "missing_property": lambda prop: f"Falta la propiedad '{prop}'",
                    },
                    "load_source": {
                        "not_path": f"Falta la ruta del archivo",
                    },
                    "load_voutput": {
                        "not_flow_cache": f"Flujo no cargado en caché",
                    },
                    "set_cache": {
                        "not_flow_cache": f"Flujo no cargado en caché",
                        "not_source": f"No existe fuente de datos",
                    },
                },
                "autots": {
                    "get_interaction": {
                        "missing_property": lambda prop: f"Falta la propiedad '{prop}'",
                    },
                    "load_source": {
                        "not_path": f"Falta la ruta del archivo",
                    },
                    "load_voutput": {
                        "not_flow_cache": f"Flujo no cargado en caché",
                    },
                    "set_cache": {
                        "not_flow_cache": f"Flujo no cargado en caché",
                        "not_source": f"No existe fuente de datos",
                        "processing_error": lambda error: f"Error al intentar procesar: " + error,
                    },
                    "start_training": {
                        "var_not_in_data": lambda prop: f"La variable '{prop}' no está en la data",
                    },
                },
                "dataprep": {
                    "node_output": {
                        "var_not_in_data": lambda prop: f"La variable '{prop}' no está en la data",
                    },
                },
            },
            "exception": lambda error: f"Error: " + error,
        }

    def service_spanish(self):
        return {
            "socket_listeners": {
                "dataprep": {
                    "database_connections": {
                        "get_databases": {
                            "get_database_error": lambda db, error: f"Error al obtener las Bases de Datos desde '{db}'\nError: {error}",
                        },
                        "get_projects": {
                            "get_project_error": lambda db, error: f"Error al obtener los Proyectos desde '{db}'\nError: {error}",
                        },
                        "get_tables": {
                            "get_table_error": lambda db, error: f"Error al obtener las Tablas desde '{db}'\nError: {error}",
                        },
                        "get_warehouses": {
                            "get_warehouse_error": lambda db, error: f"Error al obtener los Almacenes desde '{db}'\nError: {error}",
                        },
                        "unknow_source": "El recurso no coincide con ninguno de la lista",
                    }
                }
            },
            "exception": lambda error: f"Error: " + error,
        }

    # ===================================
    # English
    # ===================================
    def dataprep_english(self):
        return {
            "nodes": {
                "code": {
                    "no_vtg_codeout": lambda node_key: f"({node_key}): You must call the vtg_codeout(Df) function with your output DataFrame",
                },
                #
                "exception": lambda node_key, error: f"({node_key}) Error: " + error,
            },
        }

    def dataviz_english(self):
        return {}

    def autots_english(self):
        return {}

    def automl_english(self):
        return {}

    def utils_english(self):
        return {}

    def worker_english(self):
        return {}

    def service_english(self):
        return {}


app_message = __AppMessage("es")
