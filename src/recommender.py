from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(
        self,
        user: UserProfile,
        k: int = 5,
        artist_penalty: float = 0.5,
        genre_penalty: float = 0.3,
    ) -> List[Song]:
        """Return the top k songs using greedy re-ranking with a diversity penalty.

        After all songs are scored normally, each slot is filled by picking the
        candidate with the highest *effective* score:

            effective = base_score
                        - artist_penalty * (# already-selected songs by same artist)
                        - genre_penalty  * (# already-selected songs of same genre)

        This prevents the same artist or genre from dominating the top results.
        """
        def base_score(song: Song) -> float:
            score = 0.0
            if song.genre == user.favorite_genre:
                score += 2.0
            if song.mood == user.favorite_mood:
                score += 2.0
            score += 1.0 - abs(song.energy - user.target_energy)
            return score

        remaining = sorted(self.songs, key=base_score, reverse=True)
        selected: List[Song] = []

        while len(selected) < k and remaining:
            selected_artists = [s.artist for s in selected]
            selected_genres = [s.genre for s in selected]

            best_song = max(
                remaining,
                key=lambda s: (
                    base_score(s)
                    - selected_artists.count(s.artist) * artist_penalty
                    - selected_genres.count(s.genre) * genre_penalty
                ),
            )
            remaining.remove(best_song)
            selected.append(best_song)

        return selected

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song was recommended."""
        reasons = []
        if song.genre == user.favorite_genre:
            reasons.append("genre match")
        if song.mood == user.favorite_mood:
            reasons.append("mood match")
        energy_closeness = 1.0 - abs(song.energy - user.target_energy)
        reasons.append(f"energy closeness ({energy_closeness:.2f})")
        return ", ".join(reasons)

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a song against user preferences and return a (score, explanation) tuple."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("genre"):
        score += 2.0
        reasons.append("genre match")

    if song["mood"] == user_prefs.get("mood"):
        score += 2.0
        reasons.append("mood match")

    energy_delta = abs(song["energy"] - user_prefs.get("energy", 0.5))
    energy_score = 1.0 - energy_delta  # closer to 0 delta = higher score
    score += energy_score
    reasons.append(f"energy closeness ({energy_score:.2f})")

    explanation = ", ".join(reasons)
    return score, explanation


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv and return a list of dicts with numeric fields cast to float/int."""
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    artist_penalty: float = 0.5,
    genre_penalty: float = 0.3,
) -> List[Tuple[Dict, float, str]]:
    """Score every song then greedily pick the top k with a diversity penalty.

    Each slot is filled by the candidate with the highest effective score:

        effective = base_score
                    - artist_penalty * (# already-selected songs by same artist)
                    - genre_penalty  * (# already-selected songs of same genre)

    The returned score reflects the effective (post-penalty) value so the
    explanation accurately represents why a song landed at its position.
    """
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)

    selected: List[Tuple[Dict, float, str]] = []
    remaining = list(scored)

    while len(selected) < k and remaining:
        selected_artists = [s[0]["artist"] for s in selected]
        selected_genres = [s[0]["genre"] for s in selected]

        best = max(
            remaining,
            key=lambda item: (
                item[1]
                - selected_artists.count(item[0]["artist"]) * artist_penalty
                - selected_genres.count(item[0]["genre"]) * genre_penalty
            ),
        )
        remaining.remove(best)

        song, base, explanation = best
        artist_count = selected_artists.count(song["artist"])
        genre_count = selected_genres.count(song["genre"])
        penalty = artist_count * artist_penalty + genre_count * genre_penalty

        if penalty > 0:
            explanation += f", diversity penalty (-{penalty:.2f})"

        selected.append((song, base - penalty, explanation))

    return selected
