import pandas as pd
import numpy as np

# Load the data
data = pd.read_csv('query_data.csv')

# Ensure the column exists and is correctly referenced
if 'dcount_cloud_RoleInstance' in data.columns:
    # Flatten the counts if the column is in list-like form
    try:
        flattened_counts = np.concatenate(data['dcount_cloud_RoleInstance'].apply(lambda x: eval(x)).values)
    except TypeError:
        flattened_counts = data['dcount_cloud_RoleInstance'].values

    # Convert the flattened counts to a DataFrame
    flattened_counts_df = pd.DataFrame(flattened_counts, columns=['Count'])

    # Filter out periods where the count is less than or equal to 1
    active_periods = flattened_counts_df[flattened_counts_df['Count'] > 2]

    # Calculate the average number of servers/pods during the active periods
    average_pods_during_active_periods = active_periods['Count'].mean()

    print("Average number of active servers/pods during active periods:", average_pods_during_active_periods)
else:
    print("The column 'dcount_cloud_RoleInstance' was not found in the data.")



import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data
data = pd.read_csv('query_data.csv')

# Convert the timestamp column to datetime if it's not already
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Set the timestamp as the index
data.set_index('timestamp', inplace=True)

# Filter the data based on cloud_RoleName and operation_Name
filtered_data = data[(data['cloud_RoleName'] == 'healthcareorchestration') & 
                     (data['operation_Name'] == 'http_app_func')]

# Create a time series for unique counts of cloud_RoleInstance over time
time_series = filtered_data['cloud_RoleInstance'].resample('30S').nunique()

# Plot the time series
plt.figure(figsize=(12, 6))
plt.plot(time_series, label='Unique cloud_RoleInstance Counts', color='orange')

# Adding title and labels
plt.title('Unique Counts of cloud_RoleInstance Over Time (Last 18 Hours)')
plt.xlabel('Time')
plt.ylabel('Count')

# Adding a legend
plt.legend()

# Display the plot
plt.show()
