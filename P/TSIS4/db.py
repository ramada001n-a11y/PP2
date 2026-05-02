import psycopg2



def get_connection():
    return psycopg2.connect(dbname="postgres", user="postgres", password="0710", host="localhost")

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_score(username, score, level):
    if not username:
        username = "Anonymous"
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING;", (username,))
    cur.execute("SELECT id FROM players WHERE username = %s;", (username,))
    player_id = cur.fetchone()[0]
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s);", (player_id, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_top_10():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT p.username, MAX(g.score), MAX(g.level_reached)
        FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        GROUP BY p.username
        ORDER BY MAX(g.score) DESC LIMIT 10;
    """)
    
    res = cur.fetchall()
    cur.close()
    conn.close()
    return res

def get_personal_best(username):
    if not username: return 0
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(g.score) FROM game_sessions g
        JOIN players p ON g.player_id = p.id
        WHERE p.username = %s;
    """, (username,))
    res = cur.fetchone()[0]
    cur.close()
    conn.close()
    return res if res else 0