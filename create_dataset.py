import pandas as pd

# Sample data
data = {
    'plot': [
        "A young wizard discovers he has magical powers and attends a school of witchcraft and wizardry.",
        "Two star-crossed lovers from rival families meet and fall in love in Verona.",
        "A team of superheroes must save the world from an alien invasion.",
        "A detective investigates a series of murders linked to a serial killer.",
        "An animated film about toys that come to life when humans aren't around."
    ],
    'genres': [
        "Fantasy,Adventure",
        "Romance,Drama",
        "Action,Science Fiction",
        "Thriller,Crime",
        "Animation,Comedy,Family"
    ]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('movie_dataset.csv', index=False)
print("movie_dataset.csv has been created successfully.")

