
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class DataContainer:
    data: pd.DataFrame
    metadata: dict = field(default_factory=dict)

    def channels(self):
        return [col for col in self.data.columns if col not in ['param', 'time']]

    def groupby_param(self):
        if "sweep_param" in self.metadata:
            return self.data.groupby(self.metadata["sweep_param"])
        else:
            raise ValueError("This is not a sweep/folder-based dataset.")
