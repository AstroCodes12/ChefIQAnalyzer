import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt



def analyze(filePath):
    df = pd.read_csv(filePath, header=10, skipinitialspace=True)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12,10))

    ax1.plot(df["Elapsed Time"], df["Ambient Temperature (deg F)"], label="Ambient Temp", color="darkred", linewidth=2)
    ax1.plot(df["Elapsed Time"], df["Internal Temperature (deg F)"],label="Internal Temp", color="dodgerblue", linewidth=2)
    ax1.set_title("Internal vs Ambient")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Temperature (F)")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2.plot(df["Elapsed Time"], df["Tip 1 (deg F)"],label="tip1", color="salmon", linewidth=2)
    ax2.plot(df["Elapsed Time"], df["Tip 2 (deg F)"],label="tip2", color="blue", linewidth=2)
    ax2.plot(df["Elapsed Time"], df["Tip 3 (deg F)"],label="tip3", color="green", linewidth=2)
    ax2.plot(df["Elapsed Time"], df["Tip 4 (deg F)"],label="tip4", color="rebeccapurple", linewidth=2)
    ax2.plot(df["Elapsed Time"], df["Ambient Temperature (deg F)"],label="Ambient Temp", color="darkred", linewidth=4)
    ax2.set_title("Probe Delta Vs Ambient")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Temperature (F)")
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    return fig
