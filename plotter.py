import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np


def normal_cloud(df):
    text_str = ''
    for row_index in range(df.shape[0]):
        text_str += ' ' + df['word'].iloc[row_index]
    word_cloud = WordCloud(width=500, height=500, collocations=False, background_color='white').generate(text_str)

    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig('plot/word_cloud.png')
    return 'plot/word_cloud.png'


def sentiment_cloud(df):
    def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
        try:
            word_index = df.index[df['word'] == word.lower()][0]
            negative_count = df.loc[word_index, 'frequency'] - df.loc[word_index, 'positive_count']
            positive_count = df.loc[word_index, 'positive_count']
        except:
            return f'#11{np.random.randint(50,100)}11'
        if positive_count > negative_count:
            return f'#11{np.random.randint(50,100)}11'
        else:
            return f'#{np.random.randint(50,100)}1111'

    text_str = ''
    for row_index in range(df.shape[0]):
        text_str += ' ' + df['word'].iloc[row_index]
    word_cloud = WordCloud(width=500, height=500, collocations=False, background_color='white').generate(text_str)
    word_cloud.recolor(color_func=grey_color_func)

    plt.imshow(word_cloud)
    plt.axis("off")
    plt.savefig('plot/sentiment_cloud.png')
    return 'plot/sentiment_cloud.png'

