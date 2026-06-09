import pandas as pd
import matplotlib.pyplot as plt
import Server




df = pd.read_csv(, header=10, skipinitialspace=True)


df.plot(x="Elapsed Time")


plt.tight_layout()
plt.savefig("chart.png")   # saves to disk
plt.show()