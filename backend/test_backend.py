import unittest
import os
import json
import uuid
from fastapi.testclient import TestClient
from backend.main import app
from backend.database import DATABASE_PATH, init_db, get_db_connection
from backend.hindsight_memory import process_and_retain_meeting

class TestMemoMeetBackend(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Remove existing database file to ensure fresh start
        if os.path.exists(DATABASE_PATH):
            try:
                os.remove(DATABASE_PATH)
            except Exception as e:
                print("Failed to remove test db:", e)
        # Initialize db before tests
        init_db()
        from backend.main import seed_initial_data
        seed_initial_data()
        cls.client = TestClient(app)

    def test_database_connection(self):
        conn = get_db_connection()
        self.assertIsNotNone(conn)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        self.assertIn("customers", tables)
        self.assertIn("meetings", tables)
        self.assertIn("transcripts", tables)
        self.assertIn("memory_nodes", tables)
        self.assertIn("contradictions", tables)
        self.assertIn("risks", tables)
        conn.close()

    def test_api_list_customers(self):
        response = self.client.get("/api/customers")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]["id"], "acme-corp")

    def test_api_list_meetings(self):
        response = self.client.get("/api/meetings")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)
        # Check that meeting details include customer names
        self.assertIn("customer_name", data[0])

    def test_api_get_meeting_details(self):
        # We know acme-m1 was seeded
        response = self.client.get("/api/meetings/acme-m1")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], "acme-m1")
        self.assertEqual(data["customer_id"], "acme-corp")
        self.assertGreater(len(data["transcript"]), 0)
        self.assertGreater(len(data["decisions"]), 0)
        self.assertGreater(len(data["requirements"]), 0)

    def test_hindsight_memory_ingestion_and_reflection(self):
        # Ingest a new meeting that contradicts earlier decisions to verify flow
        meeting_id = "test-m3"
        title = "Acme Corp: Mobile Decision Shift"
        customer_id = "acme-corp"
        meeting_date = "2026-06-05"
        duration_seconds = 1200
        transcript_lines = [
            {"speaker": "Sarah Jenkins (VP Product)", "text": "We need to cancel the web project and focus 100% on native mobile development immediately."},
            {"speaker": "John Doe (CTO)", "text": "Wait, we decided in January to focus on web stability first and delay mobile. This is a complete contradiction."}
        ]
        
        # Ingest
        insights = process_and_retain_meeting(
            meeting_id=meeting_id,
            title=title,
            customer_id=customer_id,
            meeting_date=meeting_date,
            duration_seconds=duration_seconds,
            transcript_lines=transcript_lines
        )
        
        self.assertIsNotNone(insights)
        self.assertIn("iq_score", insights)
        
        # Verify it got saved
        conn = get_db_connection()
        meeting_row = conn.execute("SELECT * FROM meetings WHERE id = ?", (meeting_id,)).fetchone()
        self.assertIsNotNone(meeting_row)
        
        # Verify transcripts saved
        t_count = conn.execute("SELECT COUNT(*) FROM transcripts WHERE meeting_id = ?", (meeting_id,)).fetchone()[0]
        self.assertEqual(t_count, 2)
        
        # Verify new memory nodes created
        n_count = conn.execute("SELECT COUNT(*) FROM memory_nodes WHERE meeting_id = ?", (meeting_id,)).fetchone()[0]
        self.assertGreater(n_count, 0)
        
        # Verify a new contradiction was detected because of the mobile app conflict
        contra_count = conn.execute(
            "SELECT COUNT(*) FROM contradictions WHERE customer_id = ? AND resolved = 0",
            (customer_id,)
        ).fetchone()[0]
        self.assertGreater(contra_count, 0)
        
        conn.close()

    def test_api_truth_verification(self):
        # Query for Stripe integration evidence
        payload = {
            "query": "Stripe billing support",
            "customer_id": "acme-corp"
        }
        response = self.client.post("/api/truth-verification", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("direct_answer", data)
        self.assertGreater(len(data["evidence_cards"]), 0)
        self.assertIn("Stripe", data["evidence_cards"][0]["text_excerpt"])
        self.assertGreater(data["evidence_cards"][0]["confidence_level"], 0.5)

    def test_api_predictions(self):
        response = self.client.get("/api/predictions?customer_id=acme-corp")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]["customer_id"], "acme-corp")

    def test_api_chat(self):
        payload = {
            "query": "What decisions were made regarding the database?",
            "customer_id": "acme-corp",
            "history": []
        }
        response = self.client.post("/api/chat", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("answer", data)
        self.assertGreater(len(data["referenced_meetings"]), 0)

    def test_api_settings_update(self):
        # Update settings
        payload = {
            "groq_api_key": "gsk_testkey_12345",
            "system_prompt": "Test Custom Chief of Staff System Instruction"
        }
        response = self.client.post("/api/settings", json=payload)
        self.assertEqual(response.status_code, 200)
        
        # Fetch setting status
        response = self.client.get("/api/settings")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["groq_api_key_configured"])
        self.assertEqual(data["system_prompt"], "Test Custom Chief of Staff System Instruction")

if __name__ == "__main__":
    unittest.main()
