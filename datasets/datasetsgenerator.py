import pandas as pd
import random
import uuid

# 1. Generate catalog.csv (400 products) 
categories = ['apparel', 'leather', 'basketry', 'jewellery', 'home-decor']
materials = ['Sisal', 'Leather', 'Cotton', 'Beads', 'Wood', 'Banana Leaf']
districts = ['Kigali', 'Nyamirambo', 'Musanze', 'Huye', 'Rubavu']

catalog_data = []
for i in range(400):
    cat = random.choice(categories)
    catalog_data.append({
        'sku': str(uuid.uuid4())[:8],
        'title': f"Handmade {cat} Item {i}",
        'description': f"Authentic Rwandan {cat} made from {random.choice(materials)}.",
        'category': cat,
        'material': random.choice(materials),
        'origin_district': random.choice(districts),
        'price_rwf': random.randint(5000, 50000),
        'artisan_id': f"ART-{random.randint(100, 200)}"
    })

df_catalog = pd.DataFrame(catalog_data)
df_catalog.to_csv('catalog.csv', index=False)

# 2. Generate queries.csv (120 queries) [cite: 13, 15]
# Includes English, French, code-switched, and misspellings [cite: 18]
queries = [
    "leather boots", "chaussures en cuir", "cadeau en cuir pour femme", 
    "handmade basket", "panier agaseke", "imigongo art", "lether bots", # misspelling
    "boucles d'oreilles", "local jewelry", "vêtement rwanda", "made in rwanda clothes"
]

query_data = []
for i in range(120):
    q = random.choice(queries)
    query_data.append({
        'query_id': i,
        'query_text': q,
        'global_best_match': f"GLOBAL-{random.randint(1000, 9999)}" # Baseline match [cite: 15]
    })

df_queries = pd.DataFrame(query_data)
df_queries.to_csv('queries.csv', index=False)

# 3. Generate click_log.csv (5,000 events) [cite: 14, 15]
# Position-bias: higher ranks (1, 2) get more clicks 
click_data = []
skus = df_catalog['sku'].tolist()
for _ in range(5000):
    click_data.append({
        'query_id': random.randint(0, 119),
        'sku': random.choice(skus),
        'position': random.choices([1, 2, 3, 4, 5], weights=[50, 25, 15, 7, 3])[0],
        'timestamp': '2026-03-22'
    })

df_clicks = pd.DataFrame(click_data)
df_clicks.to_csv('click_log.csv', index=False)

print("Datasets catalog.csv, queries.csv, and click_log.csv generated successfully.")