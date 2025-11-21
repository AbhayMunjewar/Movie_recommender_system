# import pickle
# import streamlit as st
# import requests
#
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
#     data = requests.get(url).json()
#
#     poster_path = data.get("poster_path")  # SAFE access
#
#     if poster_path:
#         return "https://image.tmdb.org/t/p/w500/" + poster_path
#     else:
#         # fallback image if poster not found
#         return "https://via.placeholder.com/500"
#
#
# def recommend(movie):
#     index = movies[movies['title'] == movie].index[0]
#     distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#
#     recommended_movie_names = []
#     recommended_movie_posters = []
#
#     for i in distances[1:6]:
#         movie_id = movies.iloc[i[0]].id
#         recommended_movie_posters.append(fetch_poster(movie_id))  # FIXED
#         recommended_movie_names.append(movies.iloc[i[0]].title)
#
#     return recommended_movie_names, recommended_movie_posters
#
#
# st.header('Movie Recommender System')
# movies = pickle.load(open('movies.pkl', 'rb'))
# similarity = pickle.load(open('similarity.pkl', 'rb'))
#
# movie_list = movies['title'].values
# selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)
#
# if st.button('Show Recommendation'):
#     recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
#
#     col1, col2, col3, col4, col5 = st.columns(5)  # UPDATED
#
#     with col1:
#         st.text(recommended_movie_names[0])
#         st.image(recommended_movie_posters[0])
#
#     with col2:
#         st.text(recommended_movie_names[1])
#         st.image(recommended_movie_posters[1])
#
#     with col3:
#         st.text(recommended_movie_names[2])
#         st.image(recommended_movie_posters[2])
#
#     with col4:
#         st.text(recommended_movie_names[3])
#         st.image(recommended_movie_posters[3])
#
#     with col5:
#         st.text(recommended_movie_names[4])
#         st.image(recommended_movie_posters[4])


import pickle
import streamlit as st
import requests
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="CineMatch - Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling and fixing the Popper.js warning
st.markdown("""
<style>
    /* Hide Popper.js warnings */
    .popper-div,
    [data-popper-placement],
    .stSelectbox [data-popper-placement] {
        display: none !important;
    }

    /* Fix for dropdown positioning */
    .stSelectbox > div > div {
        position: relative !important;
        transform: none !important;
    }

    /* Ensure proper z-index for all elements */
    .stSelectbox > div > div > div {
        z-index: 9999 !important;
        position: relative !important;
    }

    /* Main header styles */
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        padding: 1rem;
    }

    .sub-header {
        font-size: 1.5rem;
        color: #4a4a4a;
        text-align: center;
        margin-bottom: 3rem;
        font-weight: 300;
    }

    .movie-card {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        height: 100%;
        border: 1px solid #e0e0e0;
    }

    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    .movie-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 0.8rem;
        text-align: center;
        height: 3rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .movie-poster {
        border-radius: 12px;
        width: 100%;
        height: 300px;
        object-fit: cover;
        transition: transform 0.3s ease;
    }

    .movie-poster:hover {
        transform: scale(1.03);
    }

    .recommend-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 30px;
        font-size: 1.1rem;
        border-radius: 50px;
        cursor: pointer;
        transition: all 0.3s ease;
        display: block;
        margin: 2rem auto;
        font-weight: 600;
    }

    .recommend-button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }

    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }

    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
    }

    .recommendation-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-top: 2rem;
    }

    .section-title {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Fix for dropdown menu positioning */
    div[data-baseweb="popover"] {
        z-index: 10000 !important;
    }

    /* Hide console errors visually */
    .stApp {
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# JavaScript to suppress console warnings
st.markdown("""
<script>
// Suppress Popper.js warnings
const originalError = console.error;
console.error = function(...args) {
    if (args[0] && typeof args[0] === 'string' && args[0].includes('preventOverflow')) {
        return; // Suppress this specific warning
    }
    originalError.apply(console, args);
};

// Alternative method to prevent dropdown issues
document.addEventListener('DOMContentLoaded', function() {
    // Fix for dropdown positioning
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.addedNodes) {
                mutation.addedNodes.forEach(function(node) {
                    if (node.nodeType === 1 && node.querySelector && node.querySelector('[data-baseweb="popover"]')) {
                        const popover = node.querySelector('[data-baseweb="popover"]');
                        if (popover) {
                            popover.style.position = 'fixed';
                            popover.style.zIndex = '10000';
                        }
                    }
                });
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
</script>
""", unsafe_allow_html=True)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url, timeout=10)
        data.raise_for_status()
        movie_data = data.json()

        poster_path = movie_data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750/667eea/ffffff?text=No+Poster"
    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750/ff6b6b/ffffff?text=Error"


def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    try:
        data = requests.get(url, timeout=10)
        data.raise_for_status()
        return data.json()
    except requests.exceptions.RequestException:
        return None


def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        recommended_movie_names = []
        recommended_movie_posters = []
        recommended_movie_ids = []

        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
            recommended_movie_ids.append(movie_id)

        return recommended_movie_names, recommended_movie_posters, recommended_movie_ids
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return [], [], []


# Header Section
st.markdown('<h1 class="main-header">🎬 CineMatch</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Discover Your Next Favorite Movie</p>', unsafe_allow_html=True)


# Load data
@st.cache_data
def load_data():
    try:
        movies = pickle.load(open('movies.pkl', 'rb'))
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None


movies, similarity = load_data()

if movies is not None and similarity is not None:
    # Sidebar with improved selectbox
    with st.sidebar:
        st.markdown("## 🔍 Find Your Movie")
        st.markdown("---")

        movie_list = movies['title'].values

        # Use a container to isolate the selectbox
        with st.container():
            selected_movie = st.selectbox(
                "Search or select a movie:",
                movie_list,
                index=0,
                help="Type to search or select from dropdown",
                key="movie_selector"  # Unique key
            )

        # Display selected movie info
        if selected_movie:
            try:
                movie_idx = movies[movies['title'] == selected_movie].index[0]
                movie_id = movies.iloc[movie_idx].id
                poster_url = fetch_poster(movie_id)

                st.markdown("### Selected Movie")
                st.image(poster_url, use_container_width=True)  # ✅ FIXED HERE
                st.markdown(f"**{selected_movie}**")
            except:
                pass

        st.markdown("---")
        st.markdown("### 💡 How it works")
        st.markdown("""
        1. Select a movie you enjoy
        2. Click 'Get Recommendations'
        3. Discover similar movies!
        """)

        st.markdown("---")
        st.markdown("### 🎯 Features")
        st.markdown("""
        - AI-powered recommendations
        - Beautiful movie posters
        - Professional interface
        - Fast and accurate
        """)

    # Main content
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button('🎯 Get Recommendations', type='primary', use_container_width=True):
            with st.spinner('Finding the perfect matches for you...'):
                recommended_movie_names, recommended_movie_posters, recommended_movie_ids = recommend(selected_movie)

            if recommended_movie_names:
                st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)
                st.markdown(
                    f'<h2 class="section-title">Because you liked <span style="color: #667eea;">"{selected_movie}"</span></h2>',
                    unsafe_allow_html=True)

                # Display recommendations in columns
                cols = st.columns(5)

                for idx, (name, poster, movie_id) in enumerate(
                        zip(recommended_movie_names, recommended_movie_posters, recommended_movie_ids)):
                    with cols[idx]:
                        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                        st.image(poster, use_container_width=True)  # ✅ FIXED HERE
                        st.markdown(f'<div class="movie-title">{name}</div>', unsafe_allow_html=True)

                        # Add movie details on hover (tooltip alternative)
                        with st.expander("ℹ️ Details"):
                            movie_details = fetch_movie_details(movie_id)
                            if movie_details:
                                st.caption(f"**Rating:** ⭐ {movie_details.get('vote_average', 'N/A')}/10")
                                st.caption(f"**Release:** {movie_details.get('release_date', 'N/A')[:4]}")
                                st.caption(
                                    f"**Overview:** {movie_details.get('overview', 'No description available')[:100]}...")

                        st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

                # Additional stats
                st.success(f"🎉 Found {len(recommended_movie_names)} perfect matches for you!")

            else:
                st.error("Sorry, we couldn't generate recommendations for this movie. Please try another one.")

    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)

    with col2:
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
            <p>Powered by TMDB API • Built with Streamlit</p>
            <p>🎬 Discover your next cinematic adventure!</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.error("""
    ❌ Unable to load the movie database. Please ensure that:
    - `movies.pkl` and `similarity.pkl` files are in the correct directory
    - The files are not corrupted
    - You have the necessary permissions to read the files
    """)