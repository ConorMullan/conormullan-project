"""Preparation and validation of data into two training files and two testing files for NMT.
This file was executed and tested within SublimeText3, and have been copy and pasted over to Pycharm Folders"""

import pandas as pd
import sqlite3
# Approx 3100000 paired rows
# Preparation of training data


# Function for reuse of code for writing to .from file
def write_to_file_parent(file):
    with open(file, "a", encoding="utf8") as f:
        for content in df['parent'].values:
            f.write(content + "\n")


# Function for reuse of code for writing to .to file
def write_to_file_comment(file):
    with open(file, "a", encoding="utf8") as f:
        for content in df['comment'].values:
            f.write(content + "\n")


timeframe = '2015-01'
# Connection to SQLite database
connection = sqlite3.connect('{}.db'.format(timeframe))
# limit of rows to what we pull into pandas data frame
limit = 5000
# Buffer through the database with last unix time
last_unix = 0
# current length of rows starts the same as limit
current_length = limit
counter = 0
test_done = False

# Every 5000 it pulls into new files
while current_length == limit:
    # 5000 SQL queries are pulled into a data frame after the previous time value (unix)
    df = pd.read_sql("""SELECT * FROM parent_reply WHERE unix > {} AND parent NOT NULL AND score > 1
                     ORDER BY unix ASC LIMIT {}""".format(last_unix, limit), connection)
    # Last unix is set to the time value for the 5000th query
    last_unix = df.tail(1)['unix'].values[0]
    current_length = len(df)
    # Sends 5000 lines to test.from and test.to each, then moves on to train.from and train.to
    if not test_done:
        write_to_file_parent("test.from")
        write_to_file_comment("test.to")
        test_done = True

    else:
        write_to_file_parent("train.from")
        write_to_file_comment("train.to")

    counter += 1

    # Every 50000 rows it prints
    if counter % 10 == 0:
        print(counter*limit, 'rows done')
