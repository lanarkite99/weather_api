from flask import Flask,render_template
import pandas as pd

app=Flask(__name__)

app = Flask(__name__, static_url_path='/static')

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/<station>/<date>")
def about(station,date):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    print(filepath)
    temperature=df.loc[df["    DATE"] == "1972-04-30"]["   TG"].squeeze() / 10
    print(temperature)
    return {"station": station,
            "temperature": temperature,
            "date": date
            }

if __name__=="__main__":
    app.run(debug=True)