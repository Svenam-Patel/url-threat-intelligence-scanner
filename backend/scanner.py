import re
import requests

def scan_url(url):

    if not url.startswith("http"):
        url = "http://" + url

    score = 0
    reasons = []

    if url.startswith("http://"):
        score += 20
        reasons.append("Uses HTTP instead of HTTPS")

    if len(url) > 75:
        score += 10
        reasons.append("URL too long")

    keywords = ["login","verify","bank","secure","account"]

    for k in keywords:
        if k in url.lower():
            score += 20
            reasons.append("Contains phishing keyword")
            break

    if re.match(r"http[s]?://\d+\.\d+\.\d+\.\d+", url):
        score += 20
        reasons.append("Uses IP address")

    try:
        r = requests.get(url, timeout=5)

        if len(r.history) > 2:
            score += 15
            reasons.append("Multiple redirects")

    except:
        return {
            "url": url,
            "status": "Invalid Domain",
            "reasons": ["Domain unreachable or invalid"]
        }

    if score >= 70:
        status = "Malicious"
    elif score >= 30:
        status = "Suspicious"
    else:
        status = "Safe"

    return {
        "url": url,
        "score": score,
        "status": status,
        "reasons": reasons
    }