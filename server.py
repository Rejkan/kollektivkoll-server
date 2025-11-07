from flask import Flask, jsonify
import requests
from google.transit import gtfs_realtime_pb2

app = Flask(__name__)

API_KEY = "d799cfda566b4df995110bc454eeb45b"
REGIONS = ["skane"]

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
                for entity in feed.entity:
                    vp = entity.vehicle
                    all_vehicles.append({
                        "region": region,
                        "id": vp.vehicle.id,
                        "lat": vp.position.latitude,
                        "lon": vp.position.longitude
                    })
        except Exception as e:
            print(f"[{region}] Error: {e}")
    return jsonify(all_vehicles)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
