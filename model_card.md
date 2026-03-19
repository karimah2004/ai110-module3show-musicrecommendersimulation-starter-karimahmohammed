# Model Card: Music Recommender Simulation

## 1. Model Name

Give your model a short, descriptive name.
Example: **VibeFinder 1.0**

THE VIBEFINDER PRO

---

## 2. Intended Use

Describe what your recommender is designed to do and who it is for.

Prompts:

- What kind of recommendations does it generate
- What assumptions does it make about the user
- Is this for real users or classroom exploration

THE VIBEFINDER PRO generates ranked song recommendations from a fixed catalog of 18 tracks based on a user's stated genre, mood, and energy preferences. It assumes the user can articulate their preferences upfront — it does not learn from listening history or implicit feedback. This is a classroom simulation built to explore how scoring logic, feature weighting, and edge cases shape the behavior of a recommender system.

---

## 3. How the Model Works

Explain your scoring approach in simple language.

Prompts:

- What features of each song are used (genre, energy, mood, etc.)
- What user preferences are considered
- How does the model turn those into a score
- What changes did you make from the starter logic

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

THE VIBEFINDER PRO scores each song out of 5 using three questions. First, does the song's genre match your favorite genre? If yes, it earns 2 points. Second, does the song's mood match your preferred mood? Another 2 points if yes. Third, how close is the song's energy level (a 0–1 scale) to your target energy? The closer it is, the closer to 1 bonus point it earns. Songs are then ranked from highest to lowest score and the top results are returned.

---

## 4. Data

Describe the dataset the model uses.

Prompts:

- How many songs are in the catalog
- What genres or moods are represented
- Did you add or remove data
- Are there parts of musical taste missing in the dataset

The catalog contains 18 songs stored in `data/songs.csv`. Genres covered include pop, lofi, rock, ambient, jazz, hip-hop, folk, electronic, classical, metal, synthwave, r&b, country, indie pop, and bossa nova. Moods include happy, chill, intense, focused, relaxed, moody, nostalgic, confident, melancholic, energetic, romantic, sad, and angry. No songs were added or removed from the starter dataset.

Notable gaps: most genres have only one song, so a genre match has almost no competition. Non-Western popular genres (K-pop, Afrobeats, Latin pop) are absent entirely. Attributes like acousticness, valence, danceability, and tempo are stored in the data but not used by the scoring function.

---

## 5. Strengths

Where does your system seem to work well

Prompts:

- User types for which it gives reasonable results
- Any patterns you think your scoring captures correctly
- Cases where the recommendations matched your intuition

VibeFinder works best for users whose tastes map cleanly onto the catalog. The Chill Lofi profile produced a perfect 5.0 score for "Library Rain" — the ranking matched intuition exactly. Well-matched profiles consistently place the most fitting song at the top with a large score gap over the runner-up, making the recommendation unambiguous. Every result also comes with a plain-language explanation (genre match, mood match, energy closeness), so it is always clear why a song was suggested.

---

## 6. Limitations and Bias

Where the system struggles or behaves unfairly.

Prompts:

- Features it does not consider
- Genres or moods that are underrepresented
- Cases where the system overfits to one preference
- Ways the scoring might unintentionally favor some users

The scorer ignores acousticness, valence, danceability, and tempo entirely — and critically, the `likes_acoustic` field on the user profile is never read, so acoustic preferences are silently discarded. Genre and mood together account for 80% of the maximum score, meaning categorical labels dominate over the continuous energy fit. A song with the right genre and mood but completely wrong energy will outscore a song with perfect energy and only one label match.

---

## 7. Evaluation

How you checked whether the recommender behaved as expected.

Prompts:

- Which user profiles you tested
- What you looked for in the recommendations
- What surprised you
- Any simple tests or comparisons you ran

No need for numeric metrics unless you created some.

Eight profiles were tested — three standard (High-Energy Pop, Chill Lofi, Deep Intense Rock) and five adversarial edge cases. Standard profiles all surfaced the expected top song with wide score margins. Edge cases revealed meaningful weaknesses.

The most surprising result: the "conflicting preferences" profile (`classical/sad` + energy=0.9) recommended "Solitude" (energy=0.22) as #1 with a score of 4.32. The +4.0 genre+mood bonus completely overrode the large energy mismatch — a song the user would likely find too quiet still won decisively.

---

## 8. Future Work

Ideas for how you would improve the model next.

Prompts:

- Additional features or preferences
- Better ways to explain recommendations
- Improving diversity among the top results
- Handling more complex user tastes

- **Use the ignored features.** Acousticness, valence, danceability, and tempo are already in the dataset. Adding a small weight for acousticness would make `likes_acoustic` meaningful.
- **Softer genre/mood matching.** Similar genres and moods could earn partial credit (e.g., "indie pop" is 50% similar to "pop"), reducing cliff-edge scoring.
- **Rebalance weights.** Let users express how much they care about each dimension, so a user who prioritizes energy over genre label gets recommendations that reflect that.
- **Diversity constraint.** Ensure the top-5 results span multiple genres so one style doesn't dominate the list.
- **Conflict detection.** When a profile contains contradictory signals (high energy + inherently low-energy mood), flag the tension instead of resolving it silently.

---

## 9. Personal Reflection

A few sentences about your experience.

Prompts:

- What you learned about recommender systems
- Something unexpected or interesting you discovered
- How this changed the way you think about music recommendation apps

Building VibeFinder made clear how much a recommender's behavior is shaped by decisions that look small on paper, like assigning genre a weight of 2 instead of 1. A scoring function can look reasonable for the common case while behaving in unexpected ways at the edges. Discovering that the +4.0 categorical bonus can completely override a large energy mismatch changed how I think about apps like Spotify. When a recommendation feels off, it often means my actual preference fell into an edge case the scoring logic wasn't built to handle.
