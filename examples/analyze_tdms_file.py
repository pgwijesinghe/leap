from leap.data_sources.tdms import TDMSLoader
import matplotlib.pyplot as plt
import numpy as np

PATH_TO_DATA = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40513B.20250724\06 - 20250729_IVvsBG\goingNeg"

GROUP_NAME = "Data.000000"
CHANNELS = {
    "Data.000000": ["AO1", "AI3", "BG"]
}

# Initialize and load data
loader = TDMSLoader(PATH_TO_DATA)
container = loader.to_container(group=GROUP_NAME, channels=CHANNELS.get(GROUP_NAME, None), sweep_channel='BG')
# container = loader.to_container(sweep_channel='BG')

df = container.data

# Access metadata and channels
print("Metadata:", container.metadata)
print("Available Channels:", container.channels())
print("Data Preview:")
print(df.head())
print(df.tail())

# Optional: groupby parameter (if loading from folder)
if "sweep_param" in container.metadata:
    grouped = container.groupby_param()
    print(f"\nGrouped by '{container.metadata['sweep_param']}' — Number of groups:", len(grouped))

# --------------------------------------
# Intensity Plot
# --------------------------------------

from leap.plotting.intensity_plot import plot_intensity

plot_intensity(container, x_col="AO1", z_col="AI3", sweep_direction="forward")
