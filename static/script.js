const movieInput = document.getElementById("movieInput");
const recommendButton = document.getElementById("recommendButton");

const loading = document.getElementById("loading");
const errorMessage = document.getElementById("errorMessage");
const results = document.getElementById("results");
const welcome = document.getElementById("welcome");
const movieGrid = document.getElementById("movieGrid");
const resultCount = document.getElementById("resultCount");


async function getRecommendations() {

    const movieTitle = movieInput.value.trim();

    if (!movieTitle) {
        showError("Please enter a movie name.");
        return;
    }

    recommendButton.disabled = true;
    recommendButton.textContent = "Finding...";

    loading.classList.remove("hidden");
    errorMessage.classList.add("hidden");

    try {

        const response = await fetch("/api/recommend", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                movie: movieTitle
            })
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(
                data.error || "Recommendation failed."
            );
        }

        displayRecommendations(
            data.recommendations
        );

    } catch (error) {

        console.error("Recommendation error:", error);

        showError(error.message);

    } finally {

        loading.classList.add("hidden");

        recommendButton.disabled = false;

        recommendButton.textContent =
            "✨ Recommend";
    }
}


function displayRecommendations(movies) {

    movieGrid.innerHTML = "";

    welcome.classList.add("hidden");

    results.classList.remove("hidden");

    resultCount.textContent =
        `${movies.length} AI matches`;


    movies.forEach(movie => {

        const card = document.createElement("article");

        card.className = "movie-card";


        const poster = movie.poster || "";


        card.innerHTML = `

            <div class="poster-container">

                ${
                    poster
                    ?
                    `
                    <img
                        src="${poster}"
                        alt="${movie.title}"
                        class="movie-poster"
                        onerror="this.style.display='none';"
                    >
                    `
                    :
                    `
                    <div class="movie-placeholder">
                        🎬
                    </div>
                    `
                }

            </div>


            <div class="movie-content">

                <h3>
                    ${movie.title}
                </h3>


                <p class="movie-genres">
                    ${movie.genres || "Movie"}
                </p>


                <p class="movie-overview">
                    ${movie.overview || ""}
                </p>


                <div class="movie-footer">

                    <span>
                        ⭐ ${movie.rating || "N/A"}
                    </span>

                    <span>
                        ${movie.similarity || 0}% match
                    </span>

                </div>

            </div>
        `;


        movieGrid.appendChild(card);

    });


    results.scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


function showError(message) {

    errorMessage.textContent = message;

    errorMessage.classList.remove("hidden");

    results.classList.add("hidden");

    loading.classList.add("hidden");
}


/* Recommend button */

recommendButton.addEventListener(
    "click",
    getRecommendations
);


/* Enter key */

movieInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            getRecommendations();

        }

    }
);