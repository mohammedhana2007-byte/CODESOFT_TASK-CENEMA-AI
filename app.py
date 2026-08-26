from flask import Flask, render_template, request, jsonify
from recommender import MovieRecommender

app = Flask(__name__)

recommender = MovieRecommender()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/recommend", methods=["POST"])
def recommend():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400

        movie_title = data.get("movie", "").strip()

        if not movie_title:
            return jsonify({
                "success": False,
                "error": "Please enter a movie name."
            }), 400

        recommendations = recommender.recommend(
            movie_title,
            number_of_recommendations=6
        )

        return jsonify({
            "success": True,
            "movie": movie_title,
            "recommendations": recommendations
        })

    except Exception as error:

        print("ERROR:", error)

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )