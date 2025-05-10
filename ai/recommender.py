import pandas as pd
from collections import defaultdict

def recommend_products(items):
    transactions = pd.read_csv('data/transactions.csv')

    # Convert all item_ids to strings for consistent comparison
    transactions['item_id'] = transactions['item_id'].astype(str)
    item_pairs = defaultdict(int)

    # Build co-occurrence counts
    for transaction_id, group in transactions.groupby('transaction_id'):
        item_list = sorted(group['item_id'].tolist())
        for i in range(len(item_list)):
            for j in range(i + 1, len(item_list)):
                pair = (item_list[i], item_list[j])
                item_pairs[pair] += 1

    recommendations = []
    for item in items:
        item_id = str(item['id'])  # ensure consistent type
        related = {}

        # Find all pairs that include this item
        for (a, b), count in item_pairs.items():
            if a == item_id:
                related[b] = count
            elif b == item_id:
                related[a] = count

        # Sort related items by count
        sorted_related = sorted(related.items(), key=lambda x: x[1], reverse=True)
        recommended_items = [r[0] for r in sorted_related[:3]]  # Top 3 recommendations

        recommendations.append({
            'item': item['name'],
            'recommended_items': recommended_items
        })
    # Create ID → Name map
    id_to_name = {str(item['id']): item['name'] for item in items}

    return recommendations
