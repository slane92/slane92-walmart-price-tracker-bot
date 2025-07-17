from datetime import datetime

def run_clearance_scan(user_id=None):
    # placeholder: fetch items, calculate markdown %, original price, store info
    return [
        {'name': 'Widget', 'orig': 25.00, 'price': 10.00, 'pct': 60, 'store': 'Poway', 'checked': datetime.now()}
    ]

def format_clearance_message(items):
    groups = {'40': [], '50': [], '60': []}
    for i in items:
        tier = '60' if i['pct'] >= 60 else '50' if i['pct'] >= 50 else '40'
        groups[tier].append(i)
    msg = ""
    for tier, list_ in groups.items():
        if not list_: continue
        emoji = "🔥" if tier=='60' else ""
        msg += f"\n{emoji}{tier}%+ off:\n"
        for it in list_:
            msg += f"{it['name']} from ${it['orig']} → ${it['price']} ({it['pct']}%) at {it['store']} 🕒{it['checked'].strftime('%m/%d %H:%M')}\n"
    return msg
