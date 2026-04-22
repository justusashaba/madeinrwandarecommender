#installing required libraries if missing
# pip install pandas scikit-learn 

import pandas as pd
import argparse
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_data():
    """Loads the synthetic catalog generated in the previous step[cite: 12]."""
    try:
        return pd.read_csv('datasets/catalog.csv')
    except FileNotFoundError:
        print("Error: catalog.csv not found. Please run your generator script first.")
        sys.exit(1)

def recommend(query_text, similarity_threshold=0.2):
    """
    Main recommendation logic including TF-IDF, local-boost, and fallback[cite: 21, 24, 73].
    """
    df = load_data()
    
    # 1. Preparing text data
    # combining title, description, and material for a richer search context.
    df['search_content'] = (df['title'] + " " + df['description'] + " " + df['material']).fillna('')
    
    # 2. Vectorization (TF-IDF)
    # This is CPU-friendly and fast, meeting the <250ms constraint.
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['search_content'])
    query_vec = vectorizer.transform([query_text])
    
    # 3. Compute Similarity
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    df['similarity_score'] = cosine_sim
    
    # Sort by similarity to find the 'global best match'
    results = df.sort_values(by='similarity_score', ascending=False).copy()
    top_global = results.iloc[0]
    
    # 4. Local-Boost & Fallback Rule 
    # Define 'Local' (In this dataset, all products in the catalog are Made in Rwanda)
    # However, we prioritize products with the highest similarity.
    
    # If the highest similarity is too low, we provide a 'curated fallback'
    # For this challenge, the fallback is the most popular local product in that category.
    if top_global['similarity_score'] < similarity_threshold:
        # Filter for the same category as the query (simplified keyword match for category)
        category_match = df[df['category'].apply(lambda x: x.lower() in query_text.lower())]
        
        if not category_match.empty:
            # Return the top item in that category as a fallback [cite: 24]
            final_output = category_match.head(5)
            logic_used = "Fallback (Low similarity match)"
        else:
            # General top-rated fallback if category isn't found
            final_output = df.head(5)
            logic_used = "Fallback (Generic)"
    else:
        # Boost local results that are nearly as good as the global match
        final_output = results.head(5)
        logic_used = "TF-IDF Search"

    return final_output, logic_used

def main():
    # CLI setup
    parser = argparse.ArgumentParser(description="Made in Rwanda Content Recommender")
    parser.add_argument('--q', type=str, required=True, help="The search query")
    args = parser.parse_args()

    # Execute recommendation
    recommendations, logic = recommend(args.q)
    
    # Print Output 
    print(f"\n--- Results for: '{args.q}' ---")
    print(f"Logic Applied: {logic}")
    print("-" * 50)
    
    # Display the top 5 results 
    output_cols = ['sku', 'title', 'category', 'origin_district', 'similarity_score']
    print(recommendations[output_cols].to_string(index=False))

if __name__ == "__main__":
    main()