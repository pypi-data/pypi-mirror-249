class Modeling:
    import cloudpickle

    from evalml.automl.automl_search import AutoMLSearch

    __automl: AutoMLSearch

    @staticmethod
    def load(file_path: str):
        """Loads Modeling object at file path.

        Args:
            file_path (str): Location to find file to load

        Returns:
            Modeling object
        """

        from evalml.automl.automl_search import AutoMLSearch

        modeling = Modeling()

        modeling.__automl = AutoMLSearch.load(file_path)

        return modeling

    def save(self, file_path, pickle_type="cloudpickle", pickle_protocol=cloudpickle.DEFAULT_PROTOCOL):
        """Saves Modeling object at file path.

        Args:
            file_path (str): Location to save file.
            pickle_type ({"pickle", "cloudpickle"}): The pickling library to use.
            pickle_protocol (int): The pickle data stream format.

        Raises:
            ValueError: If pickle_type is not "pickle" or "cloudpickle".
        """

        self.__automl.save(file_path, pickle_type, pickle_protocol)
