import matplotlib.pyplot as plt
import numpy as np


def plot_intensity(container, x_col="Delay", z_col="Ch3_y", sweep_param=None,
                   sweep_direction="both", show=True, save_path=None):
    """
    Plots an intensity map from a TDMSContainer, with option to use only
    forward, backward, or both directions of each sweep.

    Args:
        container: TDMSContainer with .data (DataFrame) and .metadata.
        x_col (str): Column for x-axis (e.g., "Delay").
        z_col (str): Column for color axis (e.g., signal like "Ch3_y").
        sweep_param (str or None): Sweep variable. If None, inferred from metadata.
        sweep_direction (str): 'forward', 'backward', or 'both' (default).
        show (bool): Show plot in window.
        save_path (str or None): Path to save the plot (if desired).
    """
    df = container.data.copy()

    if sweep_param is None:
        sweep_param = container.metadata.get("sweep_param")
        if sweep_param is None:
            raise ValueError("Sweep parameter not found in metadata or provided.")

    df = df[[x_col, z_col, sweep_param]].dropna()
    grouped = df.groupby(sweep_param)

    x_template = None
    z_matrix, y_vals = [], []

    for val, group in grouped:
        x = group[x_col].values
        z = group[z_col].values

        # Detect turning point
        diffs = np.diff(x)
        turn_idx = np.argmax(diffs < 0) + 1 if np.any(diffs < 0) else len(x)

        if sweep_direction == "forward":
            x_seg, z_seg = x[:turn_idx], z[:turn_idx]
        elif sweep_direction == "backward":
            x_seg, z_seg = x[turn_idx:], z[turn_idx:]
        else:  # both
            x_seg, z_seg = x, z

        if x_template is None:
            x_template = x_seg
        elif not np.array_equal(x_template, x_seg):
            continue  # Skip misaligned sweep

        z_matrix.append(z_seg)
        y_vals.append(val)

    if len(z_matrix) < 2:
        raise ValueError("Not enough aligned sweeps to plot.")

    x_vals = x_template
    y_vals = np.array(y_vals)
    z_matrix = np.array(z_matrix)

    # extent = [x_vals[0], x_vals[-1], y_vals[0], y_vals[-1]]
    extent = [np.min(x_vals), np.max(x_vals), np.min(y_vals), np.max(y_vals)]
    
    plt.figure(figsize=(10, 6))
    plt.imshow(z_matrix, aspect='auto', cmap='plasma', origin='lower', extent=extent)
    plt.colorbar(label=z_col)
    plt.xlabel(x_col)
    plt.ylabel(sweep_param)
    plt.title(f"Intensity Plot ({sweep_direction.capitalize()} Sweep)")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)

    if show:
        plt.show()
    else:
        plt.close()
