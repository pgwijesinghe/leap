import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from LevyTDMS import LevyTDMS
import numpy as np
import matplotlib.pyplot as plt

# Load TDMS file
files = LevyTDMS(
    r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1"
    r"\SA40653C.20250526\32 - 20250709_CtrlExp_50K_100mBias"
)

# Extract data once at the start
data = files.extract_channels(
    channels={'Data.000000': ['Delay', 'Ch3_PS_y', 'Ch3_PS_x', 'Ch3_y', 'Insertion']}
)

if data is None:
    raise ValueError("extract_channels returned None. Check channel names or file format.")

# Tkinter App
class FilterGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("THz Filter GUI")
        self.geometry("400x250")

        # --- Labels ---
        tk.Label(self, text="Low Frequency (THz)").pack(pady=(10, 0))
        self.low_scale = tk.Scale(self, from_=0.0, to=20.0, resolution=0.5, orient=tk.HORIZONTAL)
        self.low_scale.set(2.0)
        self.low_scale.pack()

        tk.Label(self, text="High Frequency (THz)").pack(pady=(10, 0))
        self.high_scale = tk.Scale(self, from_=0.5, to=30.0, resolution=0.5, orient=tk.HORIZONTAL)
        self.high_scale.set(10.0)
        self.high_scale.pack()

        # --- Buttons ---
        tk.Button(self, text="Apply Filter and Plot", command=self.apply_filter).pack(pady=20)

    def apply_filter(self):
        f_low = self.low_scale.get()
        f_high = self.high_scale.get()

        if f_low >= f_high:
            messagebox.showwarning("Invalid Range", "Low frequency must be less than high frequency.")
            return

        try:
            filtered_data = files.apply_frequency_filter(
                data,
                signal_key='Ch3_y',
                delay_key='Delay',
                bands_THz=[(f_low, f_high)]
            )

            if not filtered_data:
                messagebox.showerror("Error", "Filtered data is empty or invalid.")
                return

            files.plot_heatmap_1(
                extracted_data=filtered_data,
                sig_channel='Ch3_y_filtered',
                x_channel='Delay',
                y_channel='Insertion',
                title=f'TD vs GDD (Filtered {f_low}-{f_high} THz)',
                xlabel='Delay [ps]',
                ylabel='Insertion [mm]'
            )
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")

# Run the GUI
if __name__ == "__main__":
    app = FilterGUI()
    app.mainloop()
