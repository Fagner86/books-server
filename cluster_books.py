import sys
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

def selection(books):
    # Seleciona apenas os livros com categorias (gêneros)
    return [book for book in books if 'categories' in book and book['categories']]

def preprocess_books(books):
    # Pré-processa os dados dos livros para extração de features
    categories = []
    book_titles = []
    for book in books:
        categories.append(", ".join(book['categories']))  # Concatena as categorias em uma string
        book_titles.append(book['title'])
    return categories, book_titles

def transform_data(categories):
    # Transforma as categorias dos livros em vetores TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(categories)
    return X

def cluster_books(X, book_titles, num_clusters=5):
    # Aplica o algoritmo K-Means para agrupar os livros
    model = KMeans(n_clusters=num_clusters, random_state=42)
    model.fit(X)

    labels = model.labels_
    clusters = {i: [] for i in range(num_clusters)}
    
    for idx, label in enumerate(labels):
        clusters[label].append(book_titles[idx])
    
    return clusters

def evaluate_clusters(clusters):
    # Avalia os clusters gerados
    evaluation = {}
    for cluster_id, books in clusters.items():
        evaluation[cluster_id] = len(books)
    return evaluation

def main():
    # Carrega os livros do argumento da linha de comando
    books = json.loads(sys.argv[1])
    
    # Seleção
    selected_books = selection(books)
    
    # Pré-processamento
    categories, book_titles = preprocess_books(selected_books)
    
    # Transformação
    X = transform_data(categories)
    
    # Mineração
    clusters = cluster_books(X, book_titles)
    
    # Remover duplicatas dentro dos clusters
    for cluster_id, books in clusters.items():
        clusters[cluster_id] = list(set(books))
    
    # Adicionar nome da categoria na frente do número do cluster
    category_set = set(categories)
    labeled_clusters = {}
    for cluster_id, books in clusters.items():
        cluster_category = category_set.pop()  # Remove uma categoria do conjunto
        labeled_cluster_name = f"{cluster_category} Cluster {cluster_id}"
        labeled_clusters[labeled_cluster_name] = books
    
    # Apresentação do conhecimento
    print(json.dumps(labeled_clusters))

if __name__ == "__main__":
    main()
