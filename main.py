import json
import csv

with open('history_japan.txt') as history_file: 
    history_data = json.loads(history_file.read())

history_data = history_data['history']

for date in list(history_data):
    new_date = date[0:4]
    history_data[new_date] = history_data.pop(date, None)

countries = set()
for date in history_data.keys():
    new_countries = set(country['tag'] for country in history_data[date]['countries'])
    countries |= new_countries

products = set()
for date in history_data.keys():
    new_products = set(product['name'] for product in history_data[date]['products'])
    products |= new_products

history_countries = {}
for country in countries:
    history_countries[country] = {}
    for date in history_data.keys():
        for data in history_data[date]['countries']:
            if data['tag'] == country:
                history_countries[country][date] = data

history_products = {}
for product in products:
    history_products[product] = {}
    for date in history_data.keys():
        for data in history_data[date]['products']:
            if data['name'] == product:
                history_products[product][date] = data

country_columns = ['date'] + list(history_countries['RUS']['1838'].keys())

for country, data in history_countries.items():
    with open(country + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=country_columns)
        writer.writeheader()
        for date, yearly_data in data.items():
            yearly_data['date'] = date
            writer.writerow(yearly_data)

product_columns = ['date'] + list(history_products['timber']['1838'].keys())

for product, data in history_products.items():
    with open(product + '.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=product_columns)
        writer.writeheader()
        for date, yearly_data in data.items():
            yearly_data['date'] = date
            writer.writerow(yearly_data)
