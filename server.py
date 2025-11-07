from flask import Flask, jsonify
import requests
from google.transit import gtfs_realtime_pb2

app = Flask(__name__)

API_KEY = "d799cfda566b4df995110bc454eeb45b"

# De regioner som just nu har öppna och fungerande feeds
REGIONS = [
    "skane",
    "sl",
    "orebro",
    "ul",
    "gotland"
]

@app.route("/api/vehicles")
def vehicles():
    all_vehicles = []
    for region in REGIONS:
        url = f"https://opendata.samtrafiken.se/gtfs-rt-sweden/{region}/VehiclePositionsSweden.pb?key={API_KEY}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                feed = gtfs_realtime_pb2.FeedMessage()
                feed.ParseFromString(r.content)
                count = 0
                for entity in feed.entity:
                    if entity.HasField("vehicle") and entity.vehicle.position.latitude != 0:
                        vp = entity.vehicle
                        all_vehicles.append({
                            "region": region,
                            "id": vp.vehicle.id,
                            "lat": vp.position.latitude,
                            "lon": vp.position.longitude
                        })
                        count += 1
                print(f"[{region}] {count} fordon")
            else:
                print(f"[{region}] HTTP {r.status_code}")
        except Exception as e:
            print(f"[{region}] Fel: {e}")
    return jsonify(all_vehicles)

@app.route("/")
def home():
    return "KollektivKoll API är online 🚍 – använd /api/vehicles för data."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
