import sys
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def generate_recommendations(read_titles, all_titles):
    # Combine as listas de títulos lidos e todos os títulos disponíveis
    titles = read_titles + all_titles
    
    # Crie um vetor TF-IDF para os títulos
    vectorizer = TfidfVectorizer().fit_transform(titles)
    vectors = vectorizer.toarray()
    
    # Calcule a similaridade de cosseno entre os títulos lidos e todos os títulos
    cosine_sim = cosine_similarity(vectors[:len(read_titles)], vectors[len(read_titles):])
    
    # Obtenha a soma das similaridades para todos os livros lidos em relação a cada livro não lido
    summed_similarities = cosine_sim.sum(axis=0)
    
    # Encontre os índices dos 5 livros mais similares
    similar_indices = summed_similarities.argsort()[-5:][::-1]
    
    # Obtenha os títulos dos livros recomendados
    recommended_titles = [all_titles[i] for i in similar_indices]
    
    return recommended_titles

if __name__ == "__main__":
    read_titles = json.loads(sys.argv[1])
    all_titles = json.loads(sys.argv[2])
    
    recommendations = generate_recommendations(read_titles, all_titles)
    print(json.dumps(recommendations))
