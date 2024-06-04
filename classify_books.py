import sys
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words = stopwords.words('portuguese')

# Função para classificar os livros em gêneros
def classify_books(books):
    # Combine o título, descrição e categorias para cada livro
    documents = [f"{book['title']} {book.get('description', '')} {' '.join(book.get('categories', []))}" for book in books]
    
    # Transformar os textos em vetores TF-IDF
    vectorizer = TfidfVectorizer(stop_words=stop_words)
    X = vectorizer.fit_transform(documents)
    
    # Usar KMeans para agrupar os livros
    num_clusters = 5  # Número de gêneros
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(X)
    
    # Atribuir o gênero a cada livro
    genres = kmeans.labels_
    
    return genres

if __name__ == "__main__":
    # Ler dados dos livros da entrada padrão (stdin)
    books = json.loads(sys.stdin.read())
    
    # Classificar os livros
    genres = classify_books(books)
    
    # Imprimir os gêneros classificados
    print(json.dumps({'genres': genres.tolist()}))
