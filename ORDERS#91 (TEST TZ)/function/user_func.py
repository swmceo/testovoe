import aiosqlite

async def create_connection():
    connection = await aiosqlite.connect("database/database.db")
    return connection

async def add_user(connection, user_id: int, username: str,):
    async with connection.cursor() as cursor:
        await cursor.execute("""
                            INSERT or IGNORE INTO users (user_id, username)
                            VALUES (?, ?)""",
                            (user_id, username))
        await connection.commit()

async def add_wallet(connection, wallet: str, user_id: int, balance: int,):
    async with connection.cursor() as cursor:
        await cursor.execute("""
                            INSERT or IGNORE INTO wallets (address, user_id, balance)
                            VALUES (?, ?, ?)""",
                            (wallet, user_id, balance))
        await connection.commit()

######################################

async def delete_wallets(connection, id, address):
    async with connection.cursor() as cursor:
        request = f"DELETE FROM wallets WHERE user_id = {id} AND address = '{address}'"
        await cursor.execute(request)
        await connection.commit()
        return await cursor.fetchall()
    
async def get_all_wallets_user(connection, id):
    async with connection.cursor() as cursor:
        request = f"SELECT * FROM wallets WHERE user_id = {id}"
        await cursor.execute(request)
        return await cursor.fetchall()
    
async def get_wallet(connection, address, id):
    async with connection.cursor() as cursor:
        request = f"SELECT user_id FROM wallets WHERE address='{address}' AND user_id = {id}"
        await cursor.execute(request)
        return await cursor.fetchone()

async def get_user(connection, id):
    async with connection.cursor() as cursor:
        request = f"SELECT user_id FROM users WHERE user_id={id}"
        await cursor.execute(request)
        return await cursor.fetchone()