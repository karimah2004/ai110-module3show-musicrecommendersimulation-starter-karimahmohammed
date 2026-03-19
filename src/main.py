"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from tabulate import tabulate
from recommender import load_songs, recommend_songs


def print_recommendations(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    recommendations = recommend_songs(user_prefs, songs, k=k)

    prefs_str = "  ".join(f"{k}: {v}" for k, v in user_prefs.items())
    header = f"  {label}  |  {prefs_str}"
    print(f"\n{'─' * len(header)}")
    print(header)
    print(f"{'─' * len(header)}")

    rows = []
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        rows.append([
            rank,
            song["title"],
            song["artist"],
            song["genre"],
            f"{score:.2f}",
            explanation,
        ])

    print(tabulate(
        rows,
        headers=["#", "Title", "Artist", "Genre", "Score", "Reasons"],
        tablefmt="rounded_outline",
        colalign=("center", "left", "left", "left", "center", "left"),
    ))
    print()


# --- Standard profiles ---

HIGH_ENERGY_POP = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.9,
}

CHILL_LOFI = {
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.35,
}

DEEP_INTENSE_ROCK = {
    "genre": "rock",
    "mood": "intense",
    "energy": 0.95,
}

# --- Adversarial / edge-case profiles ---

# Edge case 1: Conflicting signals — wants high energy but a "sad" mood.
# Sad songs in the dataset (Solitude: energy=0.22) are low-energy.
# The scorer treats genre/mood and energy independently, so it will
# try to satisfy both and likely compromise by recommending mid-energy
# songs that match neither target well.
CONFLICTING_ENERGY_AND_MOOD = {
    "genre": "classical",
    "mood": "sad",
    "energy": 0.9,
}

# Edge case 2: Genre that doesn't exist in the dataset.
# No song will ever earn the +2.0 genre bonus, so every song starts
# from the same baseline. The winner is decided entirely by mood+energy,
# which may surface unexpected genres at the top.
NONEXISTENT_GENRE = {
    "genre": "k-pop",
    "mood": "happy",
    "energy": 0.8,
}

# Edge case 3: likes_acoustic=True is stored in UserProfile but the
# score_song function never reads it — acoustic preference is silently
# ignored. This tests whether the scorer leaks/respects all stated prefs.
# Here we set a genre/mood/energy that match non-acoustic songs, so an
# acoustic lover should get recommendations they'd actually dislike.
ACOUSTIC_LOVER_IGNORED = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.8,
    # Note: no "likes_acoustic" key — score_song doesn't look for it anyway.
    # Add one if you extend the scorer: "likes_acoustic": True
}

# Edge case 4: Boundary energy value of 0.0.
# energy_score = 1.0 - abs(song.energy - 0.0) = 1.0 - song.energy
# Highest-energy songs (metal, electronic, ~0.97) earn close to 0.0 on
# the energy component. Lowest-energy songs (classical, ~0.22) earn ~0.78.
# Tests whether the scorer handles the full [0, 1] boundary correctly.
SILENCE_SEEKER = {
    "genre": "classical",
    "mood": "sad",
    "energy": 0.0,
}

# Edge case 5: Perfectly average preferences (energy=0.5, no genre/mood match).
# Because no song is exactly genre="neutral" or mood="neutral", all songs
# earn 0 points for genre and mood. The ranking is driven purely by how
# close each song's energy is to 0.5, which can produce ties or near-ties
# that expose any unstable sort behavior.
AVERAGE_EVERYTHING = {
    "genre": "neutral",
    "mood": "neutral",
    "energy": 0.5,
}


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    profiles = [
        ("High-Energy Pop",              HIGH_ENERGY_POP),
        ("Chill Lofi",                   CHILL_LOFI),
        ("Deep Intense Rock",            DEEP_INTENSE_ROCK),
        ("[EDGE] Conflicting energy+mood (high energy + sad)", CONFLICTING_ENERGY_AND_MOOD),
        ("[EDGE] Nonexistent genre (k-pop)",                   NONEXISTENT_GENRE),
        ("[EDGE] Acoustic lover (pref silently ignored)",      ACOUSTIC_LOVER_IGNORED),
        ("[EDGE] Silence seeker (energy=0.0)",                 SILENCE_SEEKER),
        ("[EDGE] Average everything (no genre/mood hits)",     AVERAGE_EVERYTHING),
    ]

    for label, prefs in profiles:
        print_recommendations(label, prefs, songs)


if __name__ == "__main__":
    main()
