🥗 VegRec — Vegetarian Recipe Recommender
VegRec is an intelligent web-based application that helps users discover delicious vegetarian recipes based on the ingredients they already have at home. By leveraging Natural Language Processing (NLP), inverted indexing, and clustering techniques, the system matches user-provided ingredients to the most suitable recipes from a curated vegetarian dataset.

📌 Project Highlights
🧂 Ingredient-Based Recipe Matching
Users input available ingredients, and the system returns recipes that can be prepared with them.
🧠 NLP & Text Preprocessing
Ingredients are stemmed and vectorized using CountVectorizer and PorterStemmer for normalized matching.
🔍 Inverted Index Search
Fast lookup of recipes containing user-provided ingredients via inverted indexing.
🌐 Cluster-Based Fallback
When no exact match is found, cosine similarity and Agglomerative Clustering are used to find the closest recipe suggestions.
📊 Dynamic Streamlit Interface
Interactive and intuitive UI where users can input ingredients and browse suggested recipes with detailed instructions.

🧾 Dataset Overview
The system uses a structured dataset of pure vegetarian recipes with the following key columns:
• Recipe Name
• Ingredients

• Complete Recipe Process



🛠️ Technologies Used
PurposeLibraries / ToolsData ManipulationPandas, NumPyNLPNLTK (PorterStemmer), Regex, CountVectorizerML & SimilarityScikit-learn (Clustering), SciPy (Cosine)Web FrameworkStreamlitDataCustom vegetarian recipe dataset (CSV)
🔧 Workflow Summary
1. Data Preprocessing
• Remove punctuation, tokenize and stem ingredients
• Normalize ingredient formats

2. Feature Extraction
• Use CountVectorizer to vectorize preprocessed ingredient text
• Build inverted index for fast ingredient-to-recipe lookup

3. Recipe Recommendation
• Exact/Partial Match: Based on overlap of stemmed ingredients
• Fallback Matching: Cosine similarity using vectorized ingredients and clustering

4. Clustering
• Recipes are grouped using AgglomerativeClustering to improve fallback recommendations

🚀 Getting Started
1. Clone the repository:
Bash--
git clone https://github.com/your-username/VegRec.git
cd VegRec

2. Install dependencies:
Bash--
pip install -r requirements.txt

3. Run the app:
Bash--
streamlit run app.py


📈 Example Use Case
Input: tomato, onion, potato
 Output: Recipes like Aloo Tamatar Ki Sabzi, Tomato Curry, etc., with matching scores or similarity distances.

🌱 Future Enhancements
• Integrate transformer-based NLP models (e.g., BERT, DistilBERT)
• Add support for image-based ingredient recognition
• Personalize recommendations using user preferences
• Include nutrition facts and cooking time

• Enable user-added custom recipes


🤝 Contributions
Contributions and ideas are welcome! Feel free to fork the repo, create issues, or submit pull requests.

