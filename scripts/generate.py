import json, random, os, math
from pathlib import Path
from datetime import datetime, timedelta

HERE = Path(__file__).parent
DATA_DIR = HERE.parent / "data"

def gen_movies(n=2000):
    random.seed(42)
    genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi", "Romance", "Thriller", "Animation", "Documentary", "Fantasy"]
    genre_popularity = [0.15, 0.13, 0.12, 0.08, 0.10, 0.09, 0.10, 0.08, 0.05, 0.10]
    genre_avg_rating = {"Action": 3.8, "Comedy": 3.6, "Drama": 4.0, "Horror": 3.2, "Sci-Fi": 3.7,
                        "Romance": 3.4, "Thriller": 3.9, "Animation": 4.1, "Documentary": 4.0, "Fantasy": 3.5}
    director_quality = {f"Director_{i}": random.gauss(0, 0.3) for i in range(1, 101)}
    titles = [
        "The Last Frontier", "Midnight Sun", "Crystal Palace", "Shadow Protocol", "Neon Dreams",
        "Iron Will", "Silent Echo", "Crimson Tide", "Quantum Leap", "Golden Hour",
        "Dark Matter", "Silver Lining", "Phantom Thread", "Electric Soul", "Wild Heart",
        "Frozen Kingdom", "Burning Sky", "Lost Horizon", "Eternal Flame", "Hidden Valley",
        "Rising Star", "Deep Blue", "Red Mountain", "Green Valley", "White Storm",
        "Black Diamond", "Purple Rain", "Orange Sunrise", "Yellow Brick", "Pink Panther"
    ]
    review_templates = {
        5: ["Absolutely loved this movie! The acting was superb and the plot kept me engaged throughout.",
            "A masterpiece of cinema. Beautifully shot with an incredible soundtrack.",
            "One of the best films I've seen this year. Highly recommend to everyone.",
            "Brilliant performances and a gripping story. A must-watch.",
            "Incredible visuals and a touching narrative. Left me speechless."],
        4: ["Really enjoyable film. Some minor issues but overall great.",
            "Solid movie with good performances. Worth the watch.",
            "Great story and acting. A few slow parts but excellent overall.",
            "Really liked it. Would definitely recommend to friends.",
            "Strong performances and a compelling story. Very good."],
        3: ["It was okay. Some good moments but nothing special overall.",
            "Decent movie for a weekend watch. Not great, not terrible.",
            "Had its ups and downs. Worth watching if you have nothing else to do.",
            "Average at best. The first half was better than the second.",
            "Mixed feelings about this one. Some scenes were brilliant, others fell flat."],
        2: ["Disappointing. The trailer was better than the actual movie.",
            "Couldn't finish it. Poor acting and a predictable plot.",
            "Overhyped and underdelivered. Expected much more from this cast.",
            "A waste of time. The story made no sense and the pacing was terrible.",
            "Very boring. I fell asleep halfway through."],
        1: ["Terrible movie. One of the worst I've ever seen.",
            "Complete disaster. Bad acting, worse writing, and awful direction.",
            "I want my money back. This was unwatchable.",
            "Absolutely dreadful. Do not waste your time.",
            "The lowest point in cinema history. Avoid at all costs."]
    }
    user_biases = {}
    out = []
    base_time = datetime(2024, 1, 1)
    for i in range(n):
        genre = random.choices(genres, weights=genre_popularity, k=1)[0]
        title = f"{random.choice(titles)} {random.choice(['II', 'III', 'Origins', 'Returns', 'Legacy', 'Unleashed', 'Redefined', ''])}".strip()
        director = f"Director_{random.randint(1,100)}"
        director_effect = director_quality[director]
        genre_avg = genre_avg_rating[genre]
        popularity_boost = random.gauss(0, 0.5)
        user_id = f"user_{random.randint(10000,99999)}"
        if user_id not in user_biases:
            user_biases[user_id] = random.gauss(0, 0.4)
        user_bias = user_biases[user_id]
        raw_rating = genre_avg + director_effect + popularity_boost + user_bias
        rating = max(1, min(5, round(raw_rating)))
        if random.random() < 0.03:
            rating = random.choice([1, 5])
        if rating >= 4:
            sentiment = "positive"
        elif rating <= 2:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        release_year = random.choices([2018, 2019, 2020, 2021, 2022, 2023, 2024],
                                       weights=[5, 8, 10, 12, 15, 25, 25], k=1)[0]
        month = random.choices(range(1, 13),
            weights=[8, 7, 9, 10, 12, 14, 11, 8, 7, 8, 6, 6], k=1)[0]
        review_time = datetime(release_year, month, random.randint(1, 28),
                               random.randint(0, 23), random.randint(0, 59))
        if review_time > datetime(2024, 12, 31):
            review_time = base_time + timedelta(days=random.randint(0, 365))
        helpful_base = random.lognormvariate(2, 1.5) if rating in [1, 5] else random.lognormvariate(1.5, 1)
        helpful = int(min(helpful_base, 2000))
        out.append({
            "id": f"mov_{i:06d}",
            "title": title,
            "genre": genre,
            "rating": rating,
            "review_text": random.choice(review_templates[rating]),
            "user_id": user_id,
            "timestamp": review_time.isoformat(),
            "helpful_votes": helpful,
            "verified_purchase": random.random() < 0.75 if rating >= 4 else random.random() < 0.6,
            "release_year": release_year,
            "director": director,
            "runtime_minutes": random.randint(80, 200),
            "sentiment": sentiment,
            "text_length": len(random.choice(review_templates[rating])),
            "hour_of_day": review_time.hour,
            "day_of_week": review_time.strftime("%A"),
            "is_weekend": review_time.weekday() >= 5,
            "months_since_release": max(0, (datetime(2024, 6, 1) - review_time).days // 30),
        })
    return out

def main():
    data = gen_movies()
    DATA_DIR.mkdir(exist_ok=True)
    out = DATA_DIR / "dataset.json"
    out.write_text(json.dumps(data, indent=2) + "\n")
    print(f"Generated {len(data)} movie rating records")
    print(f"Saved to {out}")

if __name__ == "__main__":
    main()
