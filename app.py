from flask import Flask, request, jsonify
from userSheetService import UserSheetsService
app = Flask(__name__)

# Initialize the Google Sheets service
sheets_service = UserSheetsService('config/config.json', 'config/key.json')

@app.route('/sheets', methods=['POST'])
def create_sheet():
    data = request.json
    sheet_name = data.get('sheet_name')
    response, status_code = sheets_service.create_sheet(sheet_name)
    return jsonify(response), status_code

@app.route('/sheets/<name>', methods=['DELETE'])
def delete_sheet(name):
    response, status_code = sheets_service.delete_sheet(name)
    return jsonify(response), status_code

@app.route('/sheets/<username>', methods=['GET'])
def get_sheet_by_username(username):
    response, status_code = sheets_service.get_sheet_by_username(username)
    return jsonify(response), status_code

if __name__ == "__main__":
    app.run(debug=True)
