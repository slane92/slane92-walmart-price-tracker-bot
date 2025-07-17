from tinydb import TinyDB, Query
db = TinyDB("db.json")
User = Query()

async def add_wishlist(update, context):
    upc = context.args[0]
    db.upsert(...)

async def remove_wishlist(update, context):
    ...

async def show_wishlist(update, context):
    ...
