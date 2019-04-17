"""Data insertion and cleansing of a raw data file into SQLite DB
This file was executed and tested within SublimeText3, and have been copy and pasted over to Pycharm Folders"""


import sqlite3
import json
# import zstandard as zstd
from datetime import datetime



timeframe = '2015-01'
sql_transaction =[]

connection = sqlite3.connect('{}.db'.format(timeframe))
cnx = connection.cursor()


# Creates a table to store data if not already created
def create_table():
    cnx.execute("""CREATE TABLE IF NOT EXISTS parent_reply
    (parent_id TEXT PRIMARY KEY, comment_id TEXT UNIQUE, parent TEXT,
    comment TEXT, subreddit TEXT, unix INT, score INT)""")


# Replaces functions that could disrupt text and standardises quotation marks
def format_data(data):
    data = data.replace("\n", " newlinechar ").replace("\r", " newlinechar ").replace('"', "'")
    return data


# Checks if data can conform to rules and returns a Boolean response
def acceptable(data):
    if len(data.split(' ')) > 50 or len(data) < 1:
        return False 
    elif len(data) > 1000:
        return False
    elif data == '[deleted]' or data == '[removed]':
        return False
    else:
        return True


# Returns a sql query where the comment_Id is the parent_id
def find_parent(pid):
    try:
        sql = "SELECT comment FROM parent_reply WHERE comment_id = '{}' LIMIT 1".format(pid)
        cnx.execute(sql)
        result = cnx.fetchone()
        if result is not None:
            return result[0]
        else:
            return False
    except Exception as e:
        print('Finding_parent error:', str(e))


# Finds the existing score of the entered Id
def find_existing_score(pid):
    try:
        sql = "SELECT score FROM parent_reply WHERE parent_id = '{}' LIMIT 1".format(pid)
        cnx.execute(sql)
        result = cnx.fetchone()
        if result is not None:
            return result[0]
        else:
            return False
    except Exception as e:
        print('Finding_existing_score error:', str(e))


# Overrides older comment with newer comment that has a parent
def sql_insert_replace_comment(pid, cid, parent, comment, subreddit, time, score):
    try:
        sql = """UPDATE parent_reply SET parent_id = ?, comment_id = ?, parent = ?, comment = ?,
         subreddit = ?, unix = ?, score = ? WHERE parent_id =?;""".format(pid, cid, parent, comment,
                                                                          subreddit, int(time), score, pid)
        transaction_builder(sql)

    except Exception as e:
        print('Replace comment error:', str(e))


# Inserts comment that has a parent comment value
def sql_insert_has_parent_comment(pid, cid, parent, comment, subreddit, time, score):
    try:
        sql = """INSERT INTO parent_reply(parent_id, comment_id, parent, comment, subreddit, unix, score)
         VALUES("{}", "{}","{}", "{}","{}", "{}", "{}");""".format(
            pid, cid, parent, comment, subreddit, int(time), score)
        transaction_builder(sql)

    except Exception as e:
        print('Insert parent comment error:', str(e))


# Inserts comment with no higher comments i.e. parent comment
def sql_insert_no_parent_comment(pid, cid, comment, subreddit, time, score):
    try:
        sql = """INSERT INTO parent_reply(parent_id, comment_id, comment, subreddit, unix, score)
         VALUES("{}", "{}","{}", "{}","{}", "{}");""".format(pid, cid, comment, subreddit, int(time), score)
        transaction_builder(sql)

    except Exception as e:
        print('Insert_no_parent_comment error:', str(e))


# Appends sql statements and executes all of them when length is higher than 1000
def transaction_builder(sql):
    global sql_transaction
    sql_transaction.append(sql)
    if len(sql_transaction) > 1000:
        cnx.execute('BEGIN TRANSACTION')
        for s in sql_transaction:
            try:
                cnx.execute(s)
            except Exception as e:
                print('Execution of sum transaction failed:', str(e))
        connection.commit()
        sql_transaction = []


if __name__ == "__main__":
    create_table()
    row_counter = 0
    paired_rows = 0
    with open("C:/Users/User/Documents/Ulster/reddit_data/{}/RC_{}".format(timeframe.split('-')[0], timeframe),
              buffering=1000) as f:
        for row in f:
            # print(row) 
            row_counter += 1
            row = json.loads(row)
            parent_id = row['parent_id'].split('_')[1]
            comment_id = row['id']
            body = format_data(row['body'])
            created_utc = row['created_utc']
            score = row['score']
            subreddit = row['subreddit']

            parent_data = find_parent(parent_id)

            if acceptable(body):
                if score >= 2:
                    existing_comment_score = find_existing_score(parent_id)
                    if existing_comment_score:
                        if score > existing_comment_score:
                            # Parent data is the parent comment, body is the reply
                            sql_insert_replace_comment(parent_id, comment_id, parent_data, body, subreddit,
                                                       created_utc, score)
                    else:
                        if parent_data:
                            sql_insert_has_parent_comment(parent_id, comment_id, parent_data, body, subreddit,
                                                          created_utc, score)
                            paired_rows += 1
                        else:
                            # top level comment, so no parent_data but top comment has its parent Id
                            sql_insert_no_parent_comment(parent_id, comment_id, body, subreddit, created_utc, score)

            if row_counter % 100000 == 0:
                print("The total number of rows read: {},\n Paired rows:{},\n Time:{}".format(row_counter, paired_rows,
                                                                                              datetime.now))
