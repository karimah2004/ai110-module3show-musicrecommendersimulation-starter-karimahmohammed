# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

THE VIBEFINDER PRO generates ranked song recommendations from a fixed catalog of 18 tracks based on a user's stated genre, mood, and energy preferences. It assumes the user can articulate their preferences upfront — it does not learn from listening history or implicit feedback. This is a classroom simulation built to explore how scoring logic, feature weighting, and edge cases shape the behavior of a recommender system.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Mental Map:

Input: user_prefs dict (genre, mood, energy) defined in main.py
Process: load_songs() reads every row from songs.csv → recommend_songs() loops over all songs, calls a scoring function per song, collects (song, score, explanation) tuples → sorts by score descending → slices top k
Output: Ranked list of top-k (song, score, explanation) tuples printed to the terminal

![Terminal output showing top recommendations](image%203.jpg)

flowchart TD
A([User Preferences\ngenre · mood · energy]) --> D
B([data/songs.csv]) --> C[load_songs\nparse each CSV row\ninto a song dict]
C --> D[recommend_songs\nuser_prefs · songs · k]

    D --> E{For each song\nin the catalog}

    E --> F[score_song\nGenre match?\nMood match?\nEnergy delta?]
    F --> G[(song, score, explanation)]
    G --> E

    E -->|All songs scored| H[Sort all scored songs\nby score descending]
    H --> I[Slice top-k results]
    I --> J([Output\nTop K Recommendations\ntitle · score · explanation])

Diagram review — does it accurately trace a single song?

A row in songs.csv enters via load_songs as a dict.
Inside recommend_songs, the loop passes that dict to score_song alongside user_prefs.
score_song computes a numeric score (genre/mood match + energy closeness) and builds an explanation string.
The resulting (song, score, explanation) tuple is collected.
After all songs are processed, the full list is sorted and trimmed to top-k.
main.py prints each tuple — that single song now appears at its earned rank.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

![Standard Profiles — results and key insights](image%202.jpg)

![Adversarial and Edge-Case Profiles — bugs exposed](image%201.jpg)

### Diversity Penalty Results

After implementing greedy re-ranking with an artist penalty (−0.5) and genre penalty (−0.3), the same profiles were re-run. Repeat artists and genres are now penalized in later slots and the penalty is shown explicitly in each explanation.

**Standard profiles with diversity penalty:**

![High-Energy Pop with diversity penalty](use%201.jpg)

![Chill Lofi with diversity penalty](use%202.jpg)

![Deep Intense Rock with diversity penalty](use%203.jpg)

**Edge-case profiles with diversity penalty:**

![Edge case — Conflicting energy and mood with diversity penalty](use%204.jpg)

![Edge case — Nonexistent genre (k-pop) with diversity penalty](use%205.jpg)

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this

---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:

- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:

- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:

- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"
```
