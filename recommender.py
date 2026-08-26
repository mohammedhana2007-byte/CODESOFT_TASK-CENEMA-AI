import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class MovieRecommender:

    def __init__(self, data_path="data/movies.csv"):

        self.movies = pd.read_csv(data_path)

        # Required columns
        columns = [
            "genres",
            "overview",
            "cast",
            "director",
            "poster"
        ]

        # Create missing columns safely
        for column in columns:

            if column not in self.movies.columns:
                self.movies[column] = ""

            self.movies[column] = (
                self.movies[column]
                .fillna("")
                .astype(str)
            )

        # Make sure title exists
        if "title" not in self.movies.columns:
            raise ValueError(
                "movies.csv must contain a 'title' column."
            )

        self.movies["title"] = (
            self.movies["title"]
            .fillna("")
            .astype(str)
        )

        # Combine information used by AI
        self.movies["features"] = (
            self.movies["genres"] + " "
            + self.movies["overview"] + " "
            + self.movies["cast"] + " "
            + self.movies["director"]
        )

        # Convert movie information into vectors
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_features=10000
        )

        self.feature_matrix = (
            self.vectorizer.fit_transform(
                self.movies["features"]
            )
        )

        # Calculate similarity between movies
        self.similarity_matrix = cosine_similarity(
            self.feature_matrix
        )


    def recommend(
        self,
        movie_title,
        number_of_recommendations=10
    ):

        movie_title = movie_title.strip().lower()

        matches = self.movies[
            self.movies["title"]
            .str.lower()
            == movie_title
        ]

        if matches.empty:
            return []

        movie_index = matches.index[0]

        similarity_scores = list(
            enumerate(
                self.similarity_matrix[movie_index]
            )
        )

        similarity_scores.sort(
            key=lambda x: x[1],
            reverse=True
        )

        recommendations = []

        for index, score in similarity_scores[
            1:number_of_recommendations + 1
        ]:

            movie = self.movies.iloc[index]

            recommendations.append({

                "title": movie["title"],

                "genres": movie["genres"],

                "overview": movie["overview"],

                "rating": movie.get(
                    "rating",
                    "N/A"
                ),

                "poster": movie.get(
                    "poster",
                    ""
                ),

                "similarity": round(
                    score * 100,
                    2
                )
            })

        return recommendations