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
    book_ids = []
    for book in books:
        categories.append(", ".join(book['categories']))  # Concatena as categorias em uma string
        book_ids.append(str(book['_id']))
    return categories, book_ids

def transform_data(categories):
    # Transforma as categorias dos livros em vetores TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(categories)
    return X

def cluster_books(X, book_ids, categories, num_clusters):
    # Aplica o algoritmo K-Means para agrupar os livros
    model = KMeans(n_clusters=num_clusters, random_state=42)
    model.fit(X)

    labels = model.labels_
    clusters = {i: {'ids': [], 'categories': []} for i in range(num_clusters)}
    
    for idx, label in enumerate(labels):
        clusters[label]['ids'].append(book_ids[idx])
        clusters[label]['categories'].append(categories[idx])
    
    return clusters

def get_representative_category(categories):
    # Obtém a categoria mais representativa de uma lista de categorias
    from collections import Counter
    most_common = Counter(categories).most_common(1)
    if most_common:
        return most_common[0][0]
    return "Unknown"

def main():
    # Carrega os livros do argumento da linha de comando
    books = json.loads(sys.argv[1])
    
    # Seleção
    selected_books = selection(books)
    
    # Pré-processamento
    categories, book_ids = preprocess_books(selected_books)
    
    # Transformação
    X = transform_data(categories)
    
    # Determina o número de clusters com base nos gêneros únicos
    unique_genres = set(categories)
    num_clusters = len(unique_genres)
    
    # Mineração
    clusters = cluster_books(X, book_ids, categories, num_clusters)
    
    # Remover duplicatas dentro dos clusters
    for cluster_id, cluster_data in clusters.items():
        cluster_data['ids'] = list(set(cluster_data['ids']))
        cluster_data['categories'] = list(set(cluster_data['categories']))
    
    # Adicionar nome da categoria na frente do número do cluster
    labeled_clusters = {}
    for cluster_id, cluster_data in clusters.items():
        representative_category = get_representative_category(cluster_data['categories'])
        labeled_cluster_name = f"{representative_category} Cluster {cluster_id}"
        labeled_clusters[labeled_cluster_name] = cluster_data['ids']
    
    # Apresentação do conhecimento
    print(json.dumps(labeled_clusters))

if __name__ == "__main__":
    main()
