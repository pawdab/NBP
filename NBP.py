import requests
import csv
from flask import Flask, render_template, request

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
data = data[0]['rates']

currency_list = []

with open('plik.csv', 'w', newline='') as csvfile:
    fieldnames = ['currency', 'code', 'bid', 'ask']
    writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)

    writer.writeheader()
    for element in data:
        writer.writerow(element)
        currency_list.append(element["code"])

x = data


@app.route("/convert/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        currency = data.get('Currency')
        x = float(data.get("Hajsy"))

        import csv
        with open('plik.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
            for row in spamreader:
                if row[1] == currency:
                    y =  float(row[3]) * x
                    break


        return "To wychodzi " + str(round(y,2))

    return render_template("currency.html", items = currency_list)


if __name__ == "__main__":
    app.run(debug=True)

