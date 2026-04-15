from src.recommender import Recommender, Song, UserProfile, score_song


def make_pop_song(**overrides) -> Song:
    defaults = dict(
        id=1,
        title="Test Pop Track",
        artist="Test Artist",
        genre="pop",
        mood="happy",
        energy=0.8,
        tempo_bpm=120,
        valence=0.9,
        danceability=0.8,
        acousticness=0.2,
    )
    return Song(**{**defaults, **overrides})


def make_lofi_song(**overrides) -> Song:
    defaults = dict(
        id=2,
        title="Chill Lofi Loop",
        artist="Test Artist",
        genre="lofi",
        mood="chill",
        energy=0.4,
        tempo_bpm=80,
        valence=0.6,
        danceability=0.5,
        acousticness=0.9,
    )
    return Song(**{**defaults, **overrides})


def make_pop_user() -> dict:
    return {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.9,
        "danceability": 0.8,
        "acousticness": 0.2,
    }


# --- score_song ---

def test_score_song_when_mood_matches():
    song = make_pop_song()
    score, reasons = score_song({"mood": "happy"}, song.__dict__)
    assert score == 2.0
    assert any("mood match" in r for r in reasons)


def test_score_song_when_genre_matches():
    song = make_pop_song()
    score, reasons = score_song({"genre": "pop"}, song.__dict__)
    assert score == 1.5
    assert any("genre match" in r for r in reasons)


def test_score_song_when_no_match():
    song = make_pop_song()
    score, reasons = score_song({"genre": "jazz", "mood": "sad"}, song.__dict__)
    assert score == 0.0
    assert reasons == []


def test_score_song_when_energy_matches_exactly():
    song = make_pop_song(energy=0.8)
    score, reasons = score_song({"energy": 0.8}, song.__dict__)
    assert score == 1.0
    assert any("energy" in r for r in reasons)


def test_score_song_when_feature_not_in_prefs():
    song = make_pop_song()
    score, _ = score_song({}, song.__dict__)
    assert score == 0.0


# --- recommend (OOP) ---

def test_recommend_returns_songs_sorted_by_score():
    subject = Recommender([make_pop_song(), make_lofi_song()])
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_valence=0.9,
        target_acousticness=0.2,
        target_danceability=0.8,
    )
    results = subject.recommend(user, k=2)
    assert len(results) == 2
    assert results[0].genre == "pop"


def test_recommend_returns_at_most_k_songs():
    subject = Recommender([make_pop_song(), make_lofi_song()])
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_valence=0.9,
        target_acousticness=0.2,
        target_danceability=0.8,
    )
    assert len(subject.recommend(user, k=1)) == 1


def test_explain_recommendation_returns_non_empty_string():
    subject = Recommender([make_pop_song()])
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_valence=0.9,
        target_acousticness=0.2,
        target_danceability=0.8,
    )
    explanation = subject.explain_recommendation(user, subject.songs[0])
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
