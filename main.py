from flask import Flask,render_template
import pandas as pd

app=Flask(__name__)

app = Flask(__name__, static_url_path='/static')

stations=pd.read_csv("data_small/stations.txt", skiprows=17)
stations=stations[["STAID","STANAME                                 ","HGHT"]]

@app.route("/")
def home():
    return render_template("home.html",data=stations.to_html())

@app.route("/api/v1/<station>/<date>")
def about(station,date):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    temperature=df.loc[df["    DATE"] == "1972-04-30"]["   TG"].squeeze() / 10
    return {"station": station,
            "temperature": temperature,
            "date": date
            }

@app.route("/api/v1/<station>/")
def station_data(station):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20)
    return render_template("result.html",
                           name=station, data=df.to_html())

@app.route("/api/v1/annual/<station>/<year>")
def year_wise(station,year):
    filepath = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filepath, skiprows=20, parse_dates=["    DATE"])
    # Extract year as new col
    df['Year'] = df['    DATE'].dt.year

    # Filter DF based on year
    year_wise_data = df[df['Year'] == int(year)]
    return render_template("result.html",
                           name=station, data=year_wise_data.to_html())

if __name__=="__main__":
    app.run(debug=True)