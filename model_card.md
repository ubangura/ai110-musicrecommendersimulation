# Model Card: Music Recommender Simulation

## 1. Model Name

**MoodFirst 1.0**

---

## 2. Intended Use

A classroom simulation demonstrating how content-based recommender systems work. Useful for understanding feature selection, scoring design, and the tradeoffs between categorical and numeric signals.

**Not intended for:** Real users, production music services, or any context where recommendations affect what people actually listen to. The catalog is too small and too narrow to reflect genuine musical diversity or individual taste.

---

## 3. How the Model Works

Each song is scored by comparing it to the user's preferences across six attributes:

- **Mood match** — worth the most points (+2.0) because mood most directly reflects what a listener wants in the moment
- **Genre match** — second highest (+1.5) as a broad style signal
- **Energy, valence, danceability, acousticness** — each worth up to +1.0 based on how close the song's value is to the user's target. A perfect match scores +1.0; a larger gap scores less; a gap of 1.0 or more scores nothing.

The song with the highest total score is recommended first. Every result comes with a plain-language explanation listing exactly which attributes contributed points.

---

## 4. Data

- **18 songs** across 15 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, hip-hop, r&b, folk, edm, metal, blues, soul
- **7 attributes** per song: mood, energy, tempo, valence, danceability, acousticness, plus genre as a categorical label
- **6 attributes** used for scoring (tempo excluded due to correlation with energy and danceability)
---

## 5. Limitations and Bias

**Mood and genre dominate.** A song that matches both earns +3.5 before any numeric scoring begins. A song with perfect numeric alignment but no categorical match tops out at +4.0 — meaning the gap is small. In a sparse catalog, this makes it easy for the one blues song to rank #1 for any blues-preferring user regardless of whether its audio features actually match.

**The system cannot express a mood range.** A user who likes both `happy` and `chill` depending on context must pick one. The other mood will never score a bonus.

---

## 6. Evaluation

Six user profiles were run against the full catalog and the top 5 results were reviewed for each:

- **High-Energy Pop, Chill Lofi, Deep Intense Rock** — verified that expected songs clustered at the top and that the scoring reasons matched intuition
- **Conflicting Energy + Sad Mood** — tested whether high energy would override an emotional mood preference (it did not — categorical bonuses won)
- **Genre Not in Catalog** — tested graceful degradation when no genre match exists (the system fell back to numeric proximity without errors)
- **Perfectly Neutral Profile** — tested behavior when all numeric preferences are equal (categorical matches became the sole differentiator)

---

## 7. Ideas for Improvement

1. **Add a mood range.** Allow users to specify multiple acceptable moods rather than a single value, so the system can serve users with varied listening contexts.
2. **Expand the catalog and balance genres.** A meaningful genre bonus requires more than one or two songs per genre — otherwise the bonus reflects catalog gaps rather than actual preference alignment.
