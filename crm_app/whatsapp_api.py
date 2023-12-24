import requests


def send_whatsapp_message(mobile_number, message):
    url = "https://api.bulkwhatsapp.net/wapp/api/send"

    payload_data = {
        "apikey": "1edc3df293324143a960137e2c7584aa",
        "mobile": mobile_number,
        "msg": message,
        # Add other payload parameters as needed
    }

    response = requests.post(url, data=payload_data)

    return response