from leap.data_sources.tdms import TDMSLoader
import matplotlib.pyplot as plt
import numpy as np

# ✅ Update this to your actual data path
PATH_TO_DATA = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40513B.20250724\03 - 20250725_CtrlExp_6K_300mBias"

# Load data container
loader = TDMSLoader(PATH_TO_DATA)
container = loader.to_container(sweep_channel="Insertion")

# Metadata and channel check
print("✅ Metadata:", container.metadata)
print("✅ Available Channels:", container.channels())

# Choose relevant columns
x_col = "Delay"
z_col = "Ch3_y"
y_param = container.metadata.get("sweep_param", "Insertion")  # fallback

# Drop missing values
df = container.data[[x_col, z_col, y_param]].dropna()
print("✅ Data shape after dropping NaNs:", df.shape)

# Group by sweep parameter
grouped = df.groupby(y_param)

# Initialize
x_vals = None
z_matrix = []
y_vals = []

total_groups = 0
skipped_groups = 0

for val, group in grouped:
    total_groups += 1
    if x_vals is None:
        x_vals = group[x_col].values
    elif not np.array_equal(x_vals, group[x_col].values):
        print(f"⚠️ Skipping sweep value = {val:.4f}, points = {len(group)}, due to Delay mismatch")
        skipped_groups += 1
        continue

    z_matrix.append(group[z_col].values)
    y_vals.append(val)

print(f"\n✅ Total groups checked: {total_groups}")
print(f"❗ Groups skipped due to Delay mismatch: {skipped_groups}")

# Plot if enough data
if len(z_matrix) < 2 or len(x_vals) < 2:
    print("❌ Not enough consistent data to plot intensity map.")
else:
    z_matrix = np.array(z_matrix)
    y_vals = np.array(y_vals)

    extent = [x_vals[0], x_vals[-1], y_vals[0], y_vals[-1]]

    plt.figure(figsize=(10, 6))
    plt.imshow(z_matrix, aspect='auto', cmap='plasma', origin='lower', extent=extent)
    plt.colorbar(label=z_col)
    plt.xlabel(x_col)
    plt.ylabel(y_param)
    plt.title(f"Intensity Plot: {z_col} vs {x_col} and {y_param}")
    plt.tight_layout()
    plt.show()
