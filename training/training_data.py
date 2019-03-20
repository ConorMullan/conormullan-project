import pandas as pd
import sqlite3


def write_to_file_parent(file):
    with open(file, "a", encoding="utf8") as f:
        for content in df['parent'].values:
            f.write(content + "\n")


def write_to_file_comment(file):
    with open(file, "a", encoding="utf8") as f:
        for content in df['comment'].values:
            f.write(content + "\n")


timeframe = '2015-01'

connection = sqlite3.connect('{}.db'.format(timeframe))
cnx = connection.cursor()
# limit of rows to what we pull into pandas
limit = 5000
# Buffer through the database with last unix time
last_unix = 0
# current length of rows
cur_length = limit
counter = 0
# Is test complete
test_done = False

# Every 5000 it pulls into new files
while cur_length == limit:
    df = pd.read_sql("""SELECT * FROM parent_reply WHERE unix > {} AND parent NOT NULL AND score > 1
                     ORDER BY unix ASC LIMIT {}""".format(last_unix, limit), connection)
    last_unix = df.tail(1)['unix'].values[0]
    cur_length = len(df)
    if not test_done:
        write_to_file_parent("test.from")
        write_to_file_comment("test.to")
        test_done = True

    else:
        write_to_file_parent("train.from")
        write_to_file_comment("train.to")

    counter += 1
    # Every 50,000 rows it prints
    if counter % 10 == 0:
        # every 10 * limit, prints
        print(counter*limit, 'rows done')
