from flask import Flask, request, jsonify
import gspread
import json

app = Flask(__name__)

# Load config
with open('config/config.json', 'r') as f:
    config = json.load(f)

def authorize_client():
    try:
        return gspread.service_account('config/key.json')

    except Exception as e:
        print(f"Error connecting: {e}")
        return None
    

@app.route('/sheets', methods=['POST'])
def create_sheet():
    client = authorize_client()
    if client is None:
        return jsonify({"error": "Error connecting to Google Sheets"}), 500

    data = request.json
    sheet_name = data.get('sheet_name')

    if not sheet_name:
        return jsonify({"error": "Sheet name is required"}), 400

    try:
        new_sheet = client.create(sheet_name)
        new_sheet.share(config['gmail'], 'user', 'writer')
        new_sheet.share(None, 'anyone', 'reader')

        return jsonify({"message": f"Sheet '{sheet_name}' created successfully with worksheet 'Clan Points'!"}), 201
    except Exception as e:
        return jsonify({"error": f"Error adding sheet: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=True)