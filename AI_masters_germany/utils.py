import nltk


def stopwords_removal(text):
    """
    Remove german and english stopwords from text.

    :param text: A string from which stopwords should be removed.
    :return: Text without stopwords.
    """

    nltk.download('stopwords', quiet=True)

    german_stop_words = set(nltk.corpus.stopwords.words('german'))
    english_stop_words = set(nltk.corpus.stopwords.words('english'))
    stop_words = german_stop_words.union(english_stop_words)

    filtered_words = []
    for word in text.split():
        test_word = word.lower()
        test_word = test_word.replace(',', '')
        test_word = test_word.replace('.', '')
        test_word = test_word.replace(':', '')
        if test_word in stop_words:
            continue
        else:
            filtered_words.append(word)

    filtered_text = ' '.join(filtered_words)

    return filtered_text


def database_preprocessing(df, remove_stopwords=True):
    """
    Database preprocessing function.

    :param df: A pandas dataframe (e.g., result of pandas.read_csv method).
    :param remove_stopwords: if True, remove stopwords from 'Course Description' and 'Goals' columns.
    :return: A preprocessed pandas dataframe.
    """
    # Remove most special characters
    df = df.replace(to_replace=r'[^A-Za-z0-9äÄöÖüÜ.,-: ]', value='', regex=True)

    # 'Mandatory?' is boolean, but database contains different ways of specifying yes/no (e.g., 'PP' and 'WP')
    # Let's fix that!
    df['Mandatory?'] = df['Mandatory?'].fillna('y')  # Default for N.A. values is that the course is mandatory
    # It's important to first fill up the N.A. values and then apply conversion to string + lowering!
    df['Mandatory?'] = df['Mandatory?'].apply(lambda x: str(x).lower())  # Make whole df lowercase (except column names)
    df['Mandatory?'] = df['Mandatory?'].replace('pp', 'y')
    df['Mandatory?'] = df['Mandatory?'].replace('yes', 'y')
    df['Mandatory?'] = df['Mandatory?'].replace('obligatory', 'y')
    df['Mandatory?'] = df['Mandatory?'].replace('wp', 'n')
    df['Mandatory?'] = df['Mandatory?'].replace('elective', 'n')
    df['Mandatory?'] = df['Mandatory?'].replace('no', 'n')
    # todo: fix dataset TU Chemnitz entries
    df['Mandatory?'] = df['Mandatory?'].apply(lambda x: 'n' if x not in ['y', 'n'] else x)

    # Remove entries with missing values. Important that this is done before stopword removal!
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)

    if remove_stopwords:
        df['Course Description'] = df['Course Description'].apply(lambda x: stopwords_removal(x))
        df['Goals'] = df['Goals'].apply(lambda x: stopwords_removal(x))

    return df
