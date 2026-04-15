"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


PROFILES = [
    (
        "High-Energy Pop",
        {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.90,
            "valence": 0.87,
            "danceability": 0.85,
            "acousticness": 0.10,
        },
    ),
    (
        "Chill Lofi",
        {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.38,
            "valence": 0.58,
            "danceability": 0.55,
            "acousticness": 0.80,
        },
    ),
    (
        "Deep Intense Rock",
        {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.92,
            "valence": 0.40,
            "danceability": 0.60,
            "acousticness": 0.08,
        },
    ),
    # --- Adversarial / edge-case profiles ---
    (
        "Edge Case: Conflicting Energy + Sad Mood",
        {
            "genre": "blues",
            "mood": "sad",
            "energy": 0.90,   # high energy conflicts with sad mood
            "valence": 0.20,
            "danceability": 0.50,
            "acousticness": 0.50,
        },
    ),
    (
        "Edge Case: Genre Not in Catalog",
        {
            "genre": "country",   # no country songs in catalog
            "mood": "nostalgic",
            "energy": 0.55,
            "valence": 0.65,
            "danceability": 0.55,
            "acousticness": 0.70,
        },
    ),
    (
        "Edge Case: Perfectly Neutral Profile",
        {
            "genre": "ambient",
            "mood": "focused",
            "energy": 0.50,   # all numeric features at midpoint
            "valence": 0.50,
            "danceability": 0.50,
            "acousticness": 0.50,
        },
    ),
]


def print_recommendations(label: str, recommendations: list) -> None:
    print("\n" + "=" * 55)
    print(f"  {label}")
    print("=" * 55)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']} — {song['artist']}")
        print(f"       Score : {score:.2f}")
        print("       Why   :")
        for reason in explanation.split("; "):
            print(f"               • {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for label, user_prefs in PROFILES:
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(label, recommendations)


if __name__ == "__main__":
    main()
