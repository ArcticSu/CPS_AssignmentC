from flask import Flask, render_template, request
import pandas as pd
from data_processing import get_temperature_data, get_locations
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    img = None
    locations = get_locations()  
    selected_location = None

    if request.method == "POST":
        date = request.form.get("date")
        selected_location = request.form.get("location")

        data = get_temperature_data(date, selected_location)
        
        plt.figure(figsize=(10, 5))
        plt.plot(pd.to_datetime(data['time']), data['avg_temperature'], marker='o', linestyle='-')
        plt.title(f"Temperature on {date} at {selected_location}")
        plt.xlabel("Time")
        plt.ylabel("Average Temperature (°C)")
        plt.xticks(rotation=45)
        plt.tight_layout()

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        img = base64.b64encode(img.getvalue()).decode()

    return render_template("index.html", img=img, locations=locations, selected_location=selected_location)

if __name__ == "__main__":
    app.run(debug=True)
