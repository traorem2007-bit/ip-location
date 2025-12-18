from flask import Flask, request
import requests
import os

app = Flask(__name__)

def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0]
    return request.remote_addr

@app.route("/")
def home():
    ip = get_client_ip()

    data = requests.get(f"http://ip-api.com/json/{ip}").json()

    return {
        "ip": ip,
        "country": data.get("country"),
        "city": data.get("city"),
        "region": data.get("regionName"),
        "isp": data.get("isp"),
        "asn": data.get("as")
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


