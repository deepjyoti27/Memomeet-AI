import sqlite3
import os

DATABASE_PATH = os.path.join(os.path.dirname(__file__), "memomeet.db")

def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id TEXT PRIMARY KEY,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        company_name TEXT,
        designation TEXT,
        password_hash TEXT NOT NULL,
        verified INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. Workspaces Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workspaces (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        industry TEXT,
        team_size INTEGER,
        use_case TEXT,
        owner_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(owner_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # 3. Workspace Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workspace_users (
        id TEXT PRIMARY KEY,
        workspace_id TEXT,
        user_id TEXT,
        role TEXT, -- 'admin', 'manager', 'viewer'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # 4. Workspace Invites Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS workspace_invites (
        id TEXT PRIMARY KEY,
        workspace_id TEXT,
        email TEXT NOT NULL,
        role TEXT NOT NULL, -- 'admin', 'manager', 'viewer'
        accepted INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE
    );
    """)
    
    # 5. Sessions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        token TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """)
    
    # 6. Customers Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        industry TEXT,
        workspace_id TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 7. Meetings Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS meetings (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        customer_id TEXT,
        workspace_id TEXT,
        meeting_date DATE NOT NULL,
        duration_seconds INTEGER,
        recording_url TEXT,
        iq_score INTEGER CHECK(iq_score BETWEEN 0 AND 100),
        iq_breakdown TEXT, -- JSON structure of sub-scores
        sentiment_score REAL CHECK(sentiment_score BETWEEN -1.0 AND 1.0),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE
    );
    """)
    
    # Check and add workspace_id to customers and meetings if they already exist
    cursor.execute("PRAGMA table_info(customers);")
    columns = [row['name'] for row in cursor.fetchall()]
    if 'workspace_id' not in columns:
        cursor.execute("ALTER TABLE customers ADD COLUMN workspace_id TEXT;")
        
    cursor.execute("PRAGMA table_info(meetings);")
    columns = [row['name'] for row in cursor.fetchall()]
    if 'workspace_id' not in columns:
        cursor.execute("ALTER TABLE meetings ADD COLUMN workspace_id TEXT;")
    
    # 8. Transcripts Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transcripts (
        id TEXT PRIMARY KEY,
        meeting_id TEXT,
        speaker TEXT NOT NULL,
        start_time REAL,
        end_time REAL,
        text TEXT NOT NULL,
        FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
    );
    """)
    
    # 9. Memory Nodes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory_nodes (
        id TEXT PRIMARY KEY,
        meeting_id TEXT,
        customer_id TEXT,
        category TEXT NOT NULL, -- 'decision', 'requirement', 'deadline', 'commitment', 'risk', 'action_item', 'objection'
        content TEXT NOT NULL,
        context_text TEXT,
        speaker TEXT,
        confidence_level REAL,
        status TEXT DEFAULT 'active', -- 'active', 'changed', 'completed', 'superseded'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE,
        FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE
    );
    """)
    
    # 10. Memory Edges Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS memory_edges (
        id TEXT PRIMARY KEY,
        source_id TEXT NOT NULL,
        target_id TEXT NOT NULL,
        relation_type TEXT NOT NULL, -- 'HAS_REQUIREMENT', 'HAS_RISK', 'DECIDED', 'DEADLINE_OF', 'ASSIGNED_TO'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 11. Contradictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contradictions (
        id TEXT PRIMARY KEY,
        customer_id TEXT,
        meeting_id_a TEXT,
        meeting_id_b TEXT,
        node_id_a TEXT,
        node_id_b TEXT,
        statement_a TEXT NOT NULL,
        statement_b TEXT NOT NULL,
        explanation TEXT NOT NULL,
        severity TEXT NOT NULL, -- 'high', 'medium', 'low'
        resolved INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE,
        FOREIGN KEY(meeting_id_a) REFERENCES meetings(id) ON DELETE CASCADE,
        FOREIGN KEY(meeting_id_b) REFERENCES meetings(id) ON DELETE CASCADE,
        FOREIGN KEY(node_id_a) REFERENCES memory_nodes(id) ON DELETE CASCADE,
        FOREIGN KEY(node_id_b) REFERENCES memory_nodes(id) ON DELETE CASCADE
    );
    """)
    
    # 12. Risks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risks (
        id TEXT PRIMARY KEY,
        customer_id TEXT,
        meeting_id TEXT,
        category TEXT NOT NULL, -- 'churn', 'project_delay', 'scope_creep', 'stakeholder_misalignment'
        risk_level TEXT NOT NULL, -- 'high', 'medium', 'low'
        probability REAL, -- 0.0 to 1.0
        impact TEXT NOT NULL,
        evidence TEXT NOT NULL, -- JSON list of reasons
        mitigation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE,
        FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE
    );
    """)

    # 13. Tasks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        workspace_id TEXT NOT NULL,
        customer_id TEXT,
        meeting_id TEXT,
        node_id TEXT,
        content TEXT NOT NULL,
        owner TEXT,
        deadline DATE,
        status TEXT DEFAULT 'open', -- 'open', 'in_progress', 'completed', 'overdue'
        priority TEXT DEFAULT 'medium', -- 'low', 'medium', 'high'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE,
        FOREIGN KEY(customer_id) REFERENCES customers(id) ON DELETE CASCADE,
        FOREIGN KEY(meeting_id) REFERENCES meetings(id) ON DELETE CASCADE,
        FOREIGN KEY(node_id) REFERENCES memory_nodes(id) ON DELETE SET NULL
    );
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at", DATABASE_PATH)
