from flask import Flask, jsonify
import os
import psycopg2

app = Flask(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://pinguser:pingpass@postgres:5432/pingdb"
)

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS counter (
                    id SERIAL PRIMARY KEY,
                    value INTEGER NOT NULL DEFAULT 0
                );
            """)
            conn.commit()
            cur.execute("SELECT COUNT(*) FROM counter;")
            if cur.fetchone()[0] == 0:
                cur.execute("INSERT INTO counter (value) VALUES (0);")
                conn.commit()

@app.route("/")  
def health():
    return "OK", 200

@app.route("/pingpong")
def pingpong():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE counter SET value = value + 1 RETURNING value;"
            )
            new_count = cur.fetchone()[0]
            conn.commit()
    return jsonify({"pong_count": new_count})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
