import pandas as pd
import nltk
import time as t
from sentiment_analysis import *


def word_cloud_filter(file_path, url,text='url', path='scrapped/', latest_tolerence=60, minimum_row=10):
    df = pd.read_csv(rf'{file_path}')
    df_raw = pd.concat([df,pd.DataFrame({})],ignore_index=True)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    stopwords = nltk.corpus.stopwords.words("english")
    word_index = 0
    df_cloud = pd.DataFrame({'word': {}})

    # remove punchuation, filter time column
    df_raw = df_raw.dropna()
    for row_index in range(df_raw.shape[0]):
        comment = df_raw['comment'].iloc[row_index]
        # if type(comment) == type(1) or type(comment) == type(1.0):
        #     df.drop(labels=[row_index], axis=0)
        time_raw = df_raw['time'].iloc[row_index]
        time = time_raw.split()[-3:]
        if time[0] in months:
            time_str = f'{time[1].strip(",")}-{months.index(time[0])}-{time[2]}'
        else:
            time_str = f'{time[0].strip(",")}-{months.index(time[1])}-{time[2]}'
        comment_str = ''
        for letter in comment:
            if letter.isalpha() or letter == ' ':
                comment_str += letter
        for word in comment_str.split():
            if word.lower() not in stopwords:
                df_cloud.loc[word_index, 'word'] = word.lower()
                word_index += 1
        df_raw.loc[row_index, 'time'] = time_str
        df_raw.loc[row_index, 'comment'] = comment_str
        if time[0] in months:
            df_raw.loc[row_index, 'time_mag'] = int(time[1].strip(',')) + int(months.index(time[0])) * 30 + int(time[2]) * 355
        else:
            df_raw.loc[row_index, 'time_mag'] = int(time[0].strip(',')) + int(months.index(time[1])) * 30 + int(time[2]) * 355


    if url:
        df_cloud.to_csv(f'{path}url_{int(t.time())}.csv')
    else:
        df_cloud.to_csv(f'{path}{text}_{int(t.time())}.csv')
    return df_cloud


def cloud_sentiment_filter(file_path, url,text='url', path='scrapped/', latest_tolerence=60, minimum_row=10):
    df = pd.read_csv(rf'{file_path}')
    df_raw2 = pd.concat([df, pd.DataFrame({})], ignore_index=True)
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']
    df_sentiment_count = pd.DataFrame({'word': {}, 'frequency': {}, 'positive_count': {}})
    stopwords = nltk.corpus.stopwords.words("english")
    word_index_count = 0

    # remove punchuation, filter time column
    df_raw2 = df_raw2.dropna()
    for row_index in range(df_raw2.shape[0]):
        comment = df_raw2['comment'].iloc[row_index]
        time_raw = df_raw2['time'].iloc[row_index]
        time = time_raw.split()[-3:]
        if time[0] in months:
            time_str = f'{time[1].strip(",")}-{months.index(time[0])}-{time[2]}'
        else:
            time_str = f'{time[0].strip(",")}-{months.index(time[1])}-{time[2]}'
        comment_str = ''
        for letter in comment:
            if letter.isalpha() or letter == ' ':
                comment_str += letter
        df_raw2.loc[row_index, 'time'] = time_str
        df_raw2.loc[row_index, 'comment'] = comment_str
        if time[0] in months:
            df_raw2.loc[row_index, 'time_mag'] = int(time[1].strip(',')) + int(months.index(time[0])) * 30 + int(
                time[2]) * 355
        else:
            df_raw2.loc[row_index, 'time_mag'] = int(time[0].strip(',')) + int(months.index(time[1])) * 30 + int(time[2]) * 355

    # removing old reviews.
    df_raw2['time_mag'] = df_raw2['time_mag'].sort_values(ignore_index=True)
    initial_time_mag = df_raw2['time_mag'].iloc[0]
    row_latest = df_raw2.shape[0]
    for row_index in range(df_raw2.shape[0]):
        time_mag = df_raw2['time_mag'].iloc[row_index]
        if (time_mag - initial_time_mag > latest_tolerence) and row_index > minimum_row:
            row_latest = row_index
            break

    df_raw2 = df_raw2.iloc[:row_latest]

    # getting sentiment count.
    for row_index in range(df_raw2.shape[0]):
        try:
            comment = df_raw2.loc[row_index, 'comment']
        except:
            continue
        sentiment = predict_sentiment(comment)
        for word in comment.split():
            positive_count = 0
            if word.lower() in stopwords:
                continue
            if sentiment == 'positive':
                positive_count = 1
            if word.lower() not in list(df_sentiment_count['word']):
                temp_df = pd.DataFrame({'word': {word_index_count: word.lower()}, 'frequency': {word_index_count: 1},
                                        'positive_count': {word_index_count: positive_count}})
                df_sentiment_count = pd.concat([df_sentiment_count, temp_df], ignore_index=True)
                word_index_count += 1
                continue
            word_index = df_sentiment_count.index[df_sentiment_count['word'] == word.lower()][0]
            df_sentiment_count.loc[word_index, 'frequency'] += 1
            df_sentiment_count.loc[word_index, 'positive_count'] += positive_count


    if url:
        df_sentiment_count.to_csv(f'{path}url_{int(t.time())}.csv')
    else:
        df_sentiment_count.to_csv(f'{path}{text}_{int(t.time())}.csv')
    return df_sentiment_count
