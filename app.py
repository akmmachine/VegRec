import streamlit as st
import pandas as pd
import string
import re
from recipe_backend import preprocess_ingredients, stemmer
from recipe_backend import CountVectorizer, AgglomerativeClustering, cosine

# Load the vegetarian recipe dataset
@st.cache_data
def load_data():
    return pd.read_csv("pure_vegetarian_recipes_dataset.csv")

# Build model using backend logic
@st.cache_resource
def build_model(df):
    df['Processed_Ingredients'] = df['Ingredients'].apply(preprocess_ingredients)
    df['Processed_Text'] = df['Processed_Ingredients'].apply(lambda x: ' '.join(x))

    vectorizer = CountVectorizer()
    ingredient_vectors = vectorizer.fit_transform(df['Processed_Text'])

    inverted_index = {}
    for idx, ingredients in enumerate(df['Processed_Ingredients']):
        for ing in ingredients:
            inverted_index.setdefault(ing, []).append(idx)

    clustering_model = AgglomerativeClustering(n_clusters=5)
    df['Cluster'] = clustering_model.fit_predict(ingredient_vectors.toarray())

    return df, vectorizer, ingredient_vectors, inverted_index

# Recommend recipes using ingredient match and fallback similarity
def recommend_recipe(user_ingredients, df, vectorizer, ingredient_vectors, inverted_index, top_n=5):
    user_processed = []
    for ing in user_ingredients:
        ing = ing.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = re.findall(r'\b\w+\b', ing)
        stemmed = ' '.join(stemmer.stem(token) for token in tokens)
        user_processed.append(stemmed)

    candidate_ids = set()
    for ing in user_processed:
        candidate_ids.update(inverted_index.get(ing, []))

    matches = []
    for idx in candidate_ids:
        recipe_ings = set(df.loc[idx, 'Processed_Ingredients'])
        overlap = len(set(user_processed) & recipe_ings)
        if overlap > 0:
            matches.append((idx, overlap))

    if matches:
        matches.sort(key=lambda x: x[1], reverse=True)
        return [{
            "Match Type": "Exact/Partial Match",
            "Recipe Name": df.loc[idx, 'Recipe Name'],
            "Ingredients": df.loc[idx, 'Ingredients'],
            "Complete Recipe Process": df.loc[idx, 'Complete Recipe Process'],
            "Score": score
        } for idx, score in matches[:top_n]]

    # Fallback: cosine similarity
    user_vector = vectorizer.transform([' '.join(user_processed)]).toarray()[0]
    distances = [
        (idx, cosine(user_vector, ingredient_vectors[idx].toarray()[0]))
        for idx in range(len(df))
    ]
    distances.sort(key=lambda x: x[1])
    return [{
        "Match Type": "Cluster-based Closest Match",
        "Recipe Name": df.loc[idx, 'Recipe Name'],
        "Ingredients": df.loc[idx, 'Ingredients'],
        "Complete Recipe Process": df.loc[idx, 'Complete Recipe Process'],
        "Distance": dist
    } for idx, dist in distances[:top_n]]

# Streamlit UI
st.title("🥗 Vegetarian Recipe Recommender")
st.write("Type the ingredients you have, and we'll suggest delicious recipes!")

user_input = st.text_area("🧂 Ingredients (comma-separated)", "potato, tomato, onion")
top_n = st.slider("🔢 Number of recipes to show", min_value=1, max_value=10, value=5)

if user_input:
    user_ingredients = [x.strip() for x in user_input.split(',')]
    df = load_data()
    df, vectorizer, ingredient_vectors, inverted_index = build_model(df)
    results = recommend_recipe(user_ingredients, df, vectorizer, ingredient_vectors, inverted_index, top_n=top_n)

    st.subheader("🍽️ Recommended Recipes")
    for i, result in enumerate(results):
        with st.expander(f"🍲 Recipe {i+1}: {result['Recipe Name']}"):
            st.markdown(f"**🔍 Match Type**: {result['Match Type']}")
            st.markdown(f"**📝 Ingredients**: {result['Ingredients']}")
            if "Score" in result:
                st.markdown(f"**✅ Match Score**: {result['Score']}")
            elif "Distance" in result:
                st.markdown(f"**📏 Similarity Distance**: {result['Distance']:.2f}")
            st.markdown("**📖 Recipe Instructions:**")
            st.markdown(result["Complete Recipe Process"])
