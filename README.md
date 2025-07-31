🥗 VegRec — Vegetarian Recipe Recommender
-
VegRec is an intelligent web-based application that helps users discover delicious vegetarian recipes based on the ingredients they already have at home. By leveraging Natural Language Processing (NLP), inverted indexing, and clustering techniques, the system matches user-provided ingredients to the most suitable recipes from a curated vegetarian dataset.

---------------------------------------------------------------------------------------------------

📌 Project Highlights
-
🧂 Ingredient-Based Recipe Matching
Users input available ingredients, and the system returns recipes that can be prepared with them.

🧠 NLP & Text Preprocessing
Ingredients are stemmed and vectorized using CountVectorizer and PorterStemmer for normalized matching.

🔍 Inverted Index Search
Fast lookup of recipes containing user-provided ingredients via inverted indexing.

🌐 Cluster-Based Fallback
When no exact match is found, cosine similarity and Agglomerative Clustering are used to suggest similar recipes.

📊 Dynamic Streamlit Interface
Interactive and intuitive UI where users can input ingredients and browse detailed recipe recommendations.

---------------------------------------------------------------------------------

🧾 Dataset Overview
-
The system uses a structured dataset of pure vegetarian recipes with the following key columns:

1.Recipe Name

2.Ingredients

3.Complete Recipe Process

---------------------------------------------------------------------------------

🛠️ Technologies Used
-
| Purpose           | Libraries / Tools                                        |
| ----------------- | -------------------------------------------------------- |
| Data Manipulation | `pandas`, `numpy`                                        |
| NLP Preprocessing | `nltk`, `regex`, `CountVectorizer`                       |
| Machine Learning  | `scikit-learn` (clustering), `scipy` (cosine similarity) |
| Web Framework     | `streamlit`                                              |
| Dataset           | Custom vegetarian recipes (`.csv`)                       |

----------------------------------------------------------------------------------

🔧 Workflow Summary
-
📌 Data Preprocessing

Remove punctuation
Tokenize and stem ingredients
Normalize ingredient formats

📌 Feature Extraction

Use CountVectorizer to vectorize preprocessed ingredient text
Build inverted index for fast ingredient-to-recipe mapping

📌 Recipe Recommendation

Exact/Partial Match: Based on overlap of stemmed ingredients
Fallback Matching: Uses cosine similarity and clustering for close matches

📌 Clustering
Recipes are grouped using AgglomerativeClustering to support similarity-based fallback suggestions

--------------------------------------------------------------------------------

🚀 Getting Started
-
1. Clone the repository
git clone https://github.com/your-username/VegRec.git
cd VegRec

2. Install dependencies
bash
pip install -r requirements.txt

3. Run the application
bash
streamlit run app.py

---------------------------------------------------------------------------------

📈 Example Use Case
-
Input:tomato, onion, potato

Output:Recipes like Aloo Tamatar Ki Sabzi, Tomato Curry, etc., with exact match scores or similarity distances.

---------------------------------------------------------------------------------

🌱 Future Enhancements
-
1.Integrate transformer-based NLP models (e.g., BERT, DistilBERT)

2.Add support for image-based ingredient recognition

3.Personalize recommendations based on user preferences
4.Display nutrition facts and cooking time
5.Enable users to add custom recipes via the UI

---------------------------------------------------------------------------------

🤝 Contributions
-
Contributions, ideas, and suggestions are welcome!
Feel free to fork the repo, open issues, or submit a pull request.
