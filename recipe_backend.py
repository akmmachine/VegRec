import pandas as pd
import string
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import AgglomerativeClustering
from nltk.stem import PorterStemmer
from scipy.spatial.distance import cosine

df = pd.read_csv('pure_vegetarian_recipes_dataset.csv')

stemmer=PorterStemmer()

def preprocess_ingredients(ingredient_str):
    ingredient_str = ingredient_str.lower()
    ingredient_str = ingredient_str.translate(str.maketrans('','',string.punctuation))

    ingredients = [ing.strip() for ing in ingredient_str.split(',')]
    stemmed_ingredients = []
    for ing in ingredients:
        tokens = re.findall(r'\b\w+\b', ing)
        stemmed = ' '.join(stemmer.stem(token) for token in tokens)
        stemmed_ingredients.append(stemmed)

    return stemmed_ingredients

df['Processed_Ingredients'] = df['Ingredients'].apply(preprocess_ingredients)

df['Processed_Text'] = df['Processed_Ingredients'].apply(lambda x: ' '.join(x))

df.head()

vectorizer = CountVectorizer()
ingredient_vectors = vectorizer.fit_transform(df['Processed_Text'])
feature_names = vectorizer.get_feature_names_out()

# Show feature names
print("Ingredient Vocabulary:", vectorizer.get_feature_names_out())

# Save vectorized matrix for future use (like clustering or searching)
print("Vectorized Matrix Shape:", ingredient_vectors.shape)

inverted_index={}
for idx,ingredients in enumerate(df['Processed_Ingredients']):
    for ingredient in ingredients:
        if ingredient not in inverted_index:
            inverted_index[ingredient] = []
        inverted_index[ingredient].append(idx)


clustering_model = AgglomerativeClustering(n_clusters=5)
df['Cluster'] = clustering_model.fit_predict(ingredient_vectors.toarray())

def recommend_recipe(user_ingredients):
    # Preprocess user ingredients
    user_processed = []
    for ing in user_ingredients:
        ing = ing.lower().translate(str.maketrans('', '', string.punctuation))
        tokens = re.findall(r'\b\w+\b', ing)
        stemmed = ' '.join(stemmer.stem(token) for token in tokens)
        user_processed.append(stemmed)

    # Find candidate recipes from inverted index
    candidate_ids = set()
    for ing in user_processed:
        if ing in inverted_index:
            candidate_ids.update(inverted_index[ing])

    # Score candidates by overlap
    best_match = None
    best_score = -1

    for idx in candidate_ids:
        recipe_ings = set(df.loc[idx, 'Processed_Ingredients'])
        overlap = len(set(user_processed) & recipe_ings)
        if overlap > best_score:
            best_score = overlap
            best_match = idx

    # If a good match is found, return it
    if best_match is not None and best_score > 0:
        return {
            "Match Type": "Exact/Partial Match",
            "Recipe Name": df.loc[best_match, 'Recipe Name'],
            "Ingredients": df.loc[best_match, 'Ingredients'],
            "Complete Recipe Process": df.loc[best_match, 'Complete Recipe Process']
        }

    # === Fallback: Use Clustering ===
    user_vector = vectorizer.transform([' '.join(user_processed)]).toarray()[0]
    min_distance = float('inf')
    closest_idx = None

    for idx in range(len(df)):
        recipe_vector = ingredient_vectors[idx].toarray()[0]
        dist = cosine(user_vector, recipe_vector)
        if dist < min_distance:
            min_distance = dist
            closest_idx = idx

    return {
        "Match Type": "Cluster-based Recommendation",
        "Recipe Name": df.loc[closest_idx, 'Recipe Name'],
        "Ingredients": df.loc[closest_idx, 'Ingredients'],
        "Complete Recipe Process": df.loc[closest_idx, 'Complete Recipe Process']
    }


user_ingredients = ["tomato", "onion"]
result = recommend_recipe(user_ingredients)

print("\n✅ Recommended Recipe:")
for key, val in result.items():
    print(f"{key}: {val}")

user_ingredients = ["cheese", "egg", "pasta","cabbag"]

result = recommend_recipe(user_ingredients)
print("\n✅ Recommended Recipe:")
for key, val in result.items():
    print(f"{key}: {val}")