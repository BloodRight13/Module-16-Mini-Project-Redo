import unittest
import json
from app import create_app
from app.database import get_db_connection
import os

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        # Setup the database (create tables if not there)
        with self.app.app_context():
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    price DECIMAL(10, 2) NOT NULL
                );
            """)
            conn.commit()
            cur.close()
            conn.close()


    def tearDown(self):
        # Clean up database after each test
       with self.app.app_context():
         conn = get_db_connection()
         cur = conn.cursor()
         cur.execute("DELETE FROM items")
         conn.commit()
         cur.close()
         conn.close()


    def test_get_items(self):
        response = self.client.get('/items')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_create_item(self):
        item_data = {'name': 'Test Item', 'price': 10.99}
        response = self.client.post('/items', json=item_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, "application/json")
        #Check if the item is on the DB
        with self.app.app_context():
          conn = get_db_connection()
          cur = conn.cursor()
          cur.execute("SELECT * FROM items")
          items = cur.fetchall()
          self.assertEqual(len(items), 1)
          cur.close()
          conn.close()

    def test_get_item(self):
        # Insert a record for testing
        with self.app.app_context():
           conn = get_db_connection()
           cur = conn.cursor()
           cur.execute("INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id", ('Test Item', 10.99))
           item_id = cur.fetchone()[0]
           conn.commit()
           cur.close()
           conn.close()
        response = self.client.get(f'/items/{item_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['name'], 'Test Item')
        self.assertEqual(data['price'], 10.99)

    def test_get_item_not_found(self):
        response = self.client.get('/items/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.content_type, "application/json")

    def test_update_item(self):
        # Insert a record for testing
        with self.app.app_context():
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id", ('Test Item', 10.99))
            item_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
        updated_item_data = {'name': 'Updated Item', 'price': 12.99}
        response = self.client.put(f'/items/{item_id}', json=updated_item_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        #Check if the item is updated on the DB
        with self.app.app_context():
          conn = get_db_connection()
          cur = conn.cursor()
          cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
          item = cur.fetchone()
          self.assertEqual(item[1], 'Updated Item')
          self.assertEqual(item[2], 12.99)
          cur.close()
          conn.close()

    def test_delete_item(self):
        # Insert a record for testing
        with self.app.app_context():
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id", ('Test Item', 10.99))
            item_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
        response = self.client.delete(f'/items/{item_id}')
        self.assertEqual(response.status_code, 204)
        #Check if the item is on the DB
        with self.app.app_context():
          conn = get_db_connection()
          cur = conn.cursor()
          cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
          item = cur.fetchone()
          self.assertIsNone(item)
          cur.close()
          conn.close()

if __name__ == '__main__':
    unittest.main()