from pathlib import Path
import json
import os
import numpy as np
import pandas as pd


from .dtype import *


class DataHub(dict):
    """This class contains DataHub results."""

    def __init__(self, *args, **kwargs):
        if 'variable_type' in kwargs:
            
            super().__init__(**kwargs)
            self.variable_type = kwargs["variable_type"]
        else:
            raise ValueError("Unsupported initialization, missing visula type")
        

    def save(self, path = None):
        """
        Save DataHub to the specified path in JSON format.

        Parameters
        ----------
        path: Optional[str], default None
            The path where the DataHub will be saved.
        """
        if path is None:
            path = "DataHub.json"
        else:
            path = os.path.expanduser(path)

        with open(path, "w") as outfile:
            json.dump(self, outfile, cls=DataHubEncoder, indent=4)
        
        print(f"DataHub has been saved to {path}!")