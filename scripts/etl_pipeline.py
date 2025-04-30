import pandas as pd
import numpy as np
import sqlite3 as sql

# define the path to the raw data file

file_path = 'raw_data/JC-202501-citibike-tripdata.csv'

# chunk 

chunk_size = 1000000
df_chunks = pd.read_csv(file_path, chunksize=chunk_size)

# Initialize an empty list to store the processed chunks
cleaned_chunks = []

# Process each chunk

for chunk in df_chunks:
    print("Chunk info: ")
    print(chunk.info())
    print("Chunk shape: ", chunk.shape)
    print("Chunk head: ")
    print(chunk.head())
    print(chunk.isnull().sum())

    # We have missing values in the columns 'end station id' , 'end station name' , ' end station latitude' , 'end station longitude' , 'birth year'

    # We will drop the rows with missing values in these columns

    chunk = chunk.dropna(subset=['end station id', 'end station name', 'end station latitude', 'end station longitude', 'birth year'])
    
    # we will transform start time and end time to datetime format
    chunk['starttime'] = pd.to_datetime(chunk['starttime'])
    chunk['stoptime'] = pd.to_datetime(chunk['stoptime'])
    chunk['end station name'] = chunk['end station name'].astype(str)
    chunk['start station name'] = chunk['start station name'].astype(str)

    cleaned_chunks.append(chunk)

#Combine the cleaned chunks into a single DataFrame
# We will use ignore_index=True to reset the index of the combined DataFrame
df = pd.concat(cleaned_chunks, ignore_index=True)

# Check the shape of the combined DataFrame
print("Combined DataFrame shape: ", df.shape)
print("Combined DataFrame info: ")
print(df.info())
print(df.isnull().sum())

# Save cleaned data to CSV for reference
df.to_csv('output/cleaned_data.csv', index=False)



## More data Cleaning

df['trip_duration_min'] = (df['stoptime'] - df['starttime']).dt.total_seconds() / 60.0  # in minutes

# Remove trips with negative or unrealistic durations (>24 hours)
df = df[(df['trip_duration_min'] > 0) & (df['trip_duration_min'] < 1440)]

# Remove trips with negative or unrealistic distances

