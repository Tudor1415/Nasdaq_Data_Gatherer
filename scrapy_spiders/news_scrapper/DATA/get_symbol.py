import pandas as pd

cov = pd.read_csv('news_coverings.csv', sep='|')
articles = pd.read_csv('training_articles_links2.csv', sep='|')

symbols = []
cov.drop_duplicates(inplace=True)
articles.drop_duplicates(inplace=True)

for i in articles['Coverage_links']:
    symbols.append(cov.loc[cov["links"]==f".{i.split('.com')[1]}"].values[0][2])


articles["symbols"] = symbols
articles.to_csv('training_articles_links3.csv', sep='|')