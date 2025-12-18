from flask import Flask, request
import requests
import os

app = Flask(__name__)

def get_client_ip():
    if request.headers.get("X-Forwarded-For"):
        return request.headers.get("X-Forwarded-For").split(",")[0]
    return request.remote_addr

def geo_lookup(ip):
    r = requests.get(f"http://ip-api.com/json/{ip}")
    return r.json()

@app.route("/", methods=["GET"])
def home():
    query_ip = request.args.get("ip")
    ip = query_ip if query_ip else get_client_ip()

    data = geo_lookup(ip)

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
                width: 380px;
                box-shadow: 0 0 20px rgba(0,0,0,0.6);
            }}
            h1 {{
                text-align: center;
                margin-bottom: 15px;
            }}
            input {{
                width: 100%;
                padding: 10px;
                border-radius: 6px;
                border: none;
                margin-bottom: 12px;
            }}
            button {{
                width: 100%;
                padding: 10px;
                background: #2563eb;
                border: none;
                border-radius: 6px;
                color: white;
                cursor: pointer;
            }}
            .row {{
                margin-top: 8px;
            }}
            .label {{
                color: #94a3b8;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🌍 IP Location</h1>

            <form method="get">
                <input type="text" name="ip" placeholder="Enter an IP (e.g. 8.8.8.8)">
                <button type="submit">Check IP</button>
            </form>

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


