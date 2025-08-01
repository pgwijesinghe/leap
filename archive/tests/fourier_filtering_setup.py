import numpy as np
import matplotlib.pyplot as plt
import nptdms

file_path = r"G:\.shortcut-targets-by-id\0B8-gGFa6hkR4XzJJMDlqZXVKRk0\ansom\Data\THz 1\SA40653C.20250526\32 - 20250709_CtrlExp_50K_100mBias\SA40653C.20250526.000225.tdms"
with nptdms.TdmsFile(file_path) as tdms_file:
    group = tdms_file["Data.000000"]
    delay_ps = group["Delay"].data
    pc = group["Ch3_y"].data

# Convert delay to seconds for FFT
delay_s = delay_ps * 1e-12
dt = np.mean(np.diff(delay_s)) # sampling interval in seconds
N = len(pc)

# frequency axis (in THz) ---
pc_fft = np.fft.fft(pc)
freq_Hz = np.fft.fftfreq(N, d=dt)
freq_THz = freq_Hz / 1e12

mask = (
    ((0 <= np.abs(freq_THz)) & (np.abs(freq_THz) <= 10))
    # ((350 <= np.abs(freq_THz)) & (np.abs(freq_THz) <= 450)) |
    # ((700 <= np.abs(freq_THz)) & (np.abs(freq_THz) <= 900))
)

filtered_fft = pc_fft * mask

filtered_signal = np.fft.ifft(filtered_fft)

# time-domain signals
plt.figure(figsize=(10, 6))
plt.plot(delay_ps, pc-np.mean(pc), label='Original', color='blue', linewidth=1)
plt.plot(delay_ps, filtered_signal.real-np.mean(filtered_signal.real), label='Filtered (Real)', color='red', linewidth=2)
plt.xlabel("Delay (ps)")
plt.ylabel("Signal Amplitude")
plt.title("Time-Domain Signal (Filtered vs Original)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# frequency spectrum
plt.figure(figsize=(10, 5))
plt.plot(freq_THz, np.abs(pc_fft), label='Original Spectrum', alpha=0.5)
plt.plot(freq_THz, np.abs(filtered_fft), label='Filtered Spectrum', alpha=0.8)
plt.xlim(-1000, 1000)
plt.xlabel("Frequency (THz)")
plt.ylabel("Magnitude")
plt.title("Frequency-Domain Spectrum")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
