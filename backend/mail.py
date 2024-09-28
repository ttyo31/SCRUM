from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from flask import Flask, request, jsonify
import requests


app = Flask(__name__)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'scrumjacksim@gmail.com'  # Your email
app.config['MAIL_PASSWORD'] = 'ihatescrum'  # Your email password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/send-email', methods=['POST'])
def send_email():
    url = "https://script.google.com/macros/s/AKfycbxG3EnSYZAFLlS9qhRseObe08CsHT-PviqhzKm99cTDAn4vit3KUgbEKDnt2qGodpS0/exec"
    data = request.get_json()
    recipient = data.get("recipient")
    body = data.get("body")
    payload = {
        'recipient': recipient,
        "message":body
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.exceptions.HTTPError as http_err:
        return jsonify({'error': str(http_err)}), 500
    except Exception as err:
        return jsonify({'error': str(err)}), 500

    # Step 4: Return a response to the client
    return jsonify({'message': 'Email sent and POST request made successfully', 'external_response': response.json()}), 200

if __name__ == '__main__':
    app.run(debug=True,port=5002)