import pandas as pd

def predict_stockout(items):
    stockout_predictions = []

    try:
        sales_data = pd.read_csv('data/sales.csv')
    except Exception as e:
        print(f"❌ Failed to read sales data: {e}")
        return []

    for item in items:
        try:
            item_id = item.get('id')
            stock = float(item.get('stock', 0))

            # Filter sales data for the item
            item_sales = sales_data[sales_data['item_id'] == item_id]

            # Skip if no sales data
            if item_sales.empty or stock <= 0:
                continue

            # Ensure sales column is numeric
            item_sales['sales'] = pd.to_numeric(item_sales['sales'], errors='coerce').fillna(0)

            # Calculate average daily sales
            daily_sales = item_sales.groupby('date')['sales'].sum().mean()

            if daily_sales > 0:
                days_until_stockout = int(stock / daily_sales)
                stockout_predictions.append({
                    'item': item['name'],
                    'days_until_stockout': days_until_stockout
                })

        except Exception as e:
            print(f"⚠️ Error processing item '{item.get('name')}': {e}")

    return stockout_predictions
