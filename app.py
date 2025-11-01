from flask import Flask, render_template, request
import pandas as pd
import webbrowser

app = Flask(__name__)

# Load your CSV
df = pd.read_csv("placement.csv")

# Get all unique years & companies from dataset
YEARS = sorted(df["Year"].unique())
COMPANIES = sorted(df["Company"].unique())

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/year-wise", methods=["GET", "POST"])
def year_wise():
    selected_year = None
    results = None

    if request.method == "POST":
        selected_year = int(request.form.get("year"))
        results = (
            df[df["Year"] == selected_year]
            .groupby("Company")["Name"]   # count students by name
            .count()
            .reset_index(name="Student_Count")
        )

    return render_template(
        "year_wise.html",
        YEARS=YEARS,
        selected_year=selected_year,
        results=results
    )

@app.route("/company-wise", methods=["GET", "POST"])
def company_wise():
    selected_company = None
    results = None

    if request.method == "POST":
        selected_company = request.form.get("company")
        results = (
            df[df["Company"] == selected_company]
            .groupby("Year")["Name"]      # count students per year
            .count()
            .reset_index(name="Student_Count")
        )

    return render_template(
        "company_wise.html",
        COMPANIES=COMPANIES,
        selected_company=selected_company,
        results=results
    )

if __name__ == "__main__":
    # Automatically open browser on start
    webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)
