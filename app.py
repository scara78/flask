import os
import tls_client
from flask import Flask, request, Response
API_KEY = os.getenv("AGENTROUTER_KEY")

AGENTROUTER_URL = "https://agentrouter.org"

app = Flask(__name__)

session = tls_client.Session(
    client_identifier="chrome_120",
    random_tls_extension_order=False
)

@app.route("/", methods=["GET"])
def health():
    return {"status": "AgentRouter proxy running"}

@app.route("/<path:path>", methods=["GET","POST","PUT","OPTIONS"])
def proxy(path):

    headers = {
        "Content-Type": "application/json",
        "Authorization": request.headers.get("Authorization") or f"Bearer {API_KEY}",
        "User-Agent": "Kilo-Code/5.10.0",
        "Referer": "https://kilocode.ai",
        "http-referer": "https://kilocode.ai",
        "x-title": "Kilo Code",
        "x-kilocode-version": "5.10.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "*",
        "sec-fetch-mode": "cors",
        "x-stainless-lang": "js",
        "x-stainless-package-version": "5.12.2",
        "x-stainless-os": "Linux",
        "x-stainless-arch": "x64",
        "x-stainless-runtime": "node",
        "x-stainless-runtime-version": "v22.21.1",
        "x-stainless-retry-count": "0"
    }

    # adaugă prefix v1 dacă lipsește
    if not path.startswith("v1/"):
        path = "v1/" + path

    target_url = f"{AGENTROUTER_URL}/{path}"

    print(f"Proxy {request.method} -> {target_url}", flush=True)

    if request.method == "POST":
        resp = session.post(
            target_url,
            headers=headers,
            data=request.get_data()
        )
    else:
        resp = session.get(
            target_url,
            headers=headers
        )

    content_type = resp.headers.get("content-type","application/json")

    return Response(
        resp.content,
        status=resp.status_code,
        content_type=content_type
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT",19999))
    print(f"AgentRouter TLS Proxy running on port {port}", flush=True)
    app.run(host="0.0.0.0", port=port)
