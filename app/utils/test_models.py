import aiomysql
import pandas as pd
import asyncio
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()  # Cargar variables del .env

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("❌ ERROR: DATABASE_URL no está en tu .env")

# Parsear la URL de conexión
url = urlparse(DATABASE_URL)


async def export_csv():
    conn = await aiomysql.connect(
        host=url.hostname,
        port=url.port,
        user=url.username,
        password=url.password,
        db=url.path.lstrip("/"),  # remover '/'
        charset="utf8",
        autocommit=True,
    )

    cur = await conn.cursor()
    await cur.execute("SELECT * FROM students;")
    rows = await cur.fetchall()

    col_names = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=col_names)
    df.to_csv("students.csv", index=False)

    await cur.close()
    conn.close()

    print("✔ CSV generado correctamente: students.csv")


asyncio.run(export_csv())
