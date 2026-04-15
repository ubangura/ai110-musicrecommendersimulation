import csv
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_acousticness: float
    target_danceability: float


class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"


def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    with open(csv_path, newline="") as file:
        reader = csv.DictReader(file)
        return [
            {
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            }
            for row in reader
        ]


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Return (total_score, reasons) by awarding points for mood, genre, and numeric feature proximity."""
    score = 0.0
    reasons: List[str] = []

    if song["mood"] == user_prefs.get("mood"):
        score += 2.0
        reasons.append(f"mood match: {song['mood']} (+2.0)")

    if song["genre"] == user_prefs.get("genre"):
        score += 1.5
        reasons.append(f"genre match: {song['genre']} (+1.5)")

    for feature in ("energy", "valence", "danceability", "acousticness"):
        if feature not in user_prefs:
            continue
        points = max(0.0, 1.0 - abs(song[feature] - user_prefs[feature]))
        if points > 0:
            score += points
            reasons.append(f"{feature} close to target (+{points:.2f})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation) tuples."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda row: row[1], reverse=True)
    return [
        (song, score, "; ".join(reasons))
        for song, score, reasons in scored[:k]
    ]
