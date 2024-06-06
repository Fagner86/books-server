import sys
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def detect_sequence(read_books, unread_books):
    sequence_recommendations = []
    read_titles = [book['title'].lower() for book in read_books]

    for unread_book in unread_books:
        lower_title = unread_book['title'].lower()
        for read_title in read_titles:
            if read_title in lower_title and lower_title != read_title:
                if unread_book['author'] in [book['author'] for book in read_books]:
                    sequence_recommendations.append(unread_book['title'])

    return sequence_recommendations

def generate_recommendations(read_books, unread_books, num_recommendations=5):
    try:
        # Detectar sequências primeiro
        sequence_recommendations = detect_sequence(read_books, unread_books)
        remaining_recommendations_needed = num_recommendations - len(sequence_recommendations)

        # Se já temos recomendações suficientes com sequências, retorná-las
        if remaining_recommendations_needed <= 0:
            return sequence_recommendations[:num_recommendations]

        # Combine as listas de livros lidos e todos os livros disponíveis
        all_books = read_books + unread_books

        # Crie uma lista de descrições combinadas de título, autor e gênero
        descriptions = [
            f"{book['title']} {book['author']} {book['genre']}" for book in all_books
        ]

        # Crie um vetor TF-IDF para as descrições
        vectorizer = TfidfVectorizer().fit_transform(descriptions)
        vectors = vectorizer.toarray()

        # Calcule a similaridade de cosseno entre os livros lidos e todos os livros não lidos
        cosine_sim = cosine_similarity(vectors[:len(read_books)], vectors[len(read_books):])

        # Obtenha a soma das similaridades para todos os livros lidos em relação a cada livro não lido
        summed_similarities = cosine_sim.sum(axis=0)

        # Encontre os índices dos livros mais similares
        similar_indices = summed_similarities.argsort()[::-1]

        # Obtenha os títulos dos livros recomendados
        recommended_titles = [unread_books[i]['title'] for i in similar_indices if unread_books[i]['title'] not in sequence_recommendations]
        combined_recommendations = sequence_recommendations + recommended_titles

        return combined_recommendations[:num_recommendations]
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    try:
        read_books = json.loads(sys.argv[1])
        unread_books = json.loads(sys.argv[2])
        
        recommendations = generate_recommendations(read_books, unread_books)
        print(json.dumps(recommendations))  # Usa json.dumps para garantir que a saída seja JSON válido
    except Exception as e:
        print(json.dumps({"error": str(e)}))  # Usa json.dumps para garantir que a saída seja JSON válido
        sys.exit(1)
