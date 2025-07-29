import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from nptdms import TdmsFile
from leap.core.container import DataContainer

class TDMSLoader:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.is_folder = os.path.isdir(self.path)

    def to_container(self, group="Data.000000", channels=None, cache_file=None, sweep_channel=None):
        if self.is_folder:
            return self._load_folder(group, channels, cache_file, sweep_channel)
        else:
            return self._load_file(self.path, group, channels)


    def _load_file(self, filepath, group, channels):
        tdms_data = TdmsFile.read(filepath)
        tdms_group = tdms_data[group]
        available_channels = [ch.name for ch in tdms_group.channels()]
        selected_channels = channels or available_channels

        # Step 1: Collect all channel arrays
        raw_data = {}
        max_len = 0

        for ch in selected_channels:
            if ch in available_channels:
                arr = tdms_group[ch][:]
                raw_data[ch] = arr
                max_len = max(max_len, len(arr))

        # Step 2: Pad all to max length using NaN
        padded_data = {}
        for ch, arr in raw_data.items():
            if len(arr) < max_len:
                pad = np.full(max_len - len(arr), np.nan)
                padded_data[ch] = np.concatenate([arr, pad])
            else:
                padded_data[ch] = arr

        df = pd.DataFrame(padded_data)
        return DataContainer(data=df, metadata={"source": filepath, "type": "TDMS"})


    def _load_folder(self, group, channels, cache_file, sweep_channel="SD"):
        files = sorted([f for f in os.listdir(self.path) if f.endswith(".tdms")])
        full_paths = [os.path.join(self.path, f) for f in files]

        results = []
        param_values = []

        for idx, file in enumerate(tqdm(full_paths, desc="Loading TDMS folder")):
            try:
                if sweep_channel:
                    val = self._infer_parameter(file, group, sweep_channel)
                    if val is None:
                        val = idx  # fallback to file index if extraction fails
                else:
                    val = idx  # use file index if no sweep_channel provided

                container = self._load_file(file, group, channels)
                df = container.data.copy()
                df["param"] = val
                results.append(df)
                param_values.append(val)
            except Exception as e:
                print(f"Failed on file {file}: {e}")

        combined = pd.concat(results, ignore_index=True)
        return DataContainer(
            data=combined,
            metadata={
                "source": self.path,
                "type": "TDMS_FOLDER",
                "sweep_param": "param",
                "param_values": param_values,
                "sweep_channel": sweep_channel
            }
        )

    def _infer_parameter(self, filepath, group, sweep_channel):
        try:
            tdms = TdmsFile.read(filepath)
            value = tdms[group][sweep_channel][0]
            return value
        except Exception as e:
            print(f"Could not extract sweep param from {filepath}: {e}")
            return None
