## Ingest data from the generated .csv, remove the start and end of the video while the task was not started and until the record endded
## Save the cleaned data

import pandas as pd
import matplotlib.pyplot as plt

task_df = pd.read_csv('tracked_positions.csv')

task_df.plot(kind='scatter', x='Center_X', y='Center_Y', s=1)
plt.show()