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

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>IP Location</title>
        <style>
            body {{
                background: #0f172a;
                color: #e5e7eb;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}
            .card {{
                background: #020617;
                padding: 30px;
                border-radius: 12px;
                width: 360px;
                box-shadow: 0 0 20px rgba(0,0,0,0.6);
            }}
            h1 {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .row {{
                margin: 8px 0;
            }}
            .label {{
                color: #94a3b8;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🌍 IP Location</h1>
            <div class="row"><span class="label">IP:</span> {ip}</div>
            <div class="row"><span class="label">Country:</span> {data.get("country")}</div>
            <div class="row"><span class="label">Region:</span> {data.get("regionName")}</div>
            <div class="row"><span class="label">City:</span> {data.get("city")}</div>
            <div class="row"><span class="label">ISP:</span> {data.get("isp")}</div>
            <div class="row"><span class="label">ASN:</span> {data.get("as")}</div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



