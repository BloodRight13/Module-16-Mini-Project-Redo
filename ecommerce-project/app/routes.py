from flask import request, jsonify
from app.database import get_db_connection
from app.models import Item, CreateItem, UpdateItem
import psycopg2
from typing import List

def init_app(app):
    @app.route('/items', methods=['GET'])
    def get_items():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM items')
        items = cur.fetchall()
        cur.close()
        conn.close()
        item_list: List[Item] = []
        for item in items:
           item_list.append({
                'id': item[0],
                'name': item[1],
                'price': item[2]
            })
        return jsonify(item_list), 200

    @app.route('/items', methods=['POST'])
    def create_item():
        data: CreateItem = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO items (name, price) VALUES (%s, %s)",
                        (data['name'], data['price']))
            conn.commit()
        except psycopg2.Error as e:
          conn.rollback()
          cur.close()
          conn.close()
          return jsonify({"error": str(e)}), 500
        cur.close()
        conn.close()
        return jsonify({"message": "item created successfully"}), 201

    @app.route('/items/<int:item_id>', methods=['GET'])
    def get_item(item_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM items WHERE id = %s", (item_id,))
        item = cur.fetchone()
        cur.close()
        conn.close()
        if item:
            item_data: Item = {
                'id': item[0],
                'name': item[1],
                'price': item[2]
            }
            return jsonify(item_data), 200
        return jsonify({"message": "item not found"}), 404
    @app.route('/items/<int:item_id>', methods=['PUT'])
    def update_item(item_id):
      data: UpdateItem = request.get_json()
      conn = get_db_connection()
      cur = conn.cursor()
      try:
          cur.execute("UPDATE items SET name = %s, price = %s WHERE id = %s",
                      (data['name'], data['price'], item_id))
          conn.commit()
      except psycopg2.Error as e:
        conn.rollback()
        cur.close()
        conn.close()
        return jsonify({"error": str(e)}), 500
      cur.close()
      conn.close()
      return jsonify({"message": "item updated successfully"}), 200


    @app.route('/items/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM items WHERE id = %s", (item_id,))
            conn.commit()
        except psycopg2.Error as e:
          conn.rollback()
          cur.close()
          conn.close()
          return jsonify({"error": str(e)}), 500
        cur.close()
        conn.close()
        return jsonify({"message": "item deleted successfully"}), 204
