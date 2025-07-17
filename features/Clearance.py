import json
from walmart_api import get_store_clearance_data

def calculate_discount(original_price, sale_price):
    try:
        return round((original_price - sale_price) / original_price * 100)
    except ZeroDivisionError:
        return 0

def categorize_by_price(item):
    if item['sale_price'] <= 10:
        return "$10 or less"
    elif item['sale_price'] <= 20:
        return "$20 or less"
    elif item['sale_price'] <= 40:
        return "$40 or less"
    else:
        return "$60 or less"

def format_markdown_group(items_by_discount):
    messages = []
    for discount_group in ['60+', '50', '40']:
        items = items_by_discount.get(discount_group, [])
        if items:
            emoji = "🔥" if discount_group == "60+" else ""
            header = f"\n🔻 {discount_group}% OFF DEALS {emoji} 🔻"
            lines = [header]
            buckets = {}

            for item in items:
                bucket = categorize_by_price(item)
                if bucket not in buckets:
                    buckets[bucket] = []
                line = f"• {item['name']} - Now ${item['sale_price']} (Was ${item['original_price']})"
                buckets[bucket].append(line)

            for bucket_label in ["$10 or less", "$20 or less", "$40 or less", "$60 or less"]:
                if bucket_label in buckets:
                    lines.append(f"\n💲 {bucket_label}:")
                    lines.extend(buckets[bucket_label])

            messages.append("\n".join(lines))
    return messages

def get_grouped_markdowns(zip_code, store_ids):
    all_items = []
    for store_id in store_ids:
        items = get_store_clearance_data(store_id)
        for item in items:
            discount = calculate_discount(item['original_price'], item['sale_price'])
            if discount >= 40:
                item['discount'] = discount
                item['store_id'] = store_id
                all_items.append(item)

    grouped = {'60+': [], '50': [], '40': []}
    for item in all_items:
        if item['discount'] >= 60:
            grouped['60+'].append(item)
        elif item['discount'] >= 50:
            grouped['50'].append(item)
        elif item['discount'] >= 40:
            grouped['40'].append(item)

    return format_markdown_group(grouped)
