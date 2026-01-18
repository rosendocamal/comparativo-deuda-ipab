# ---------- Obtener las cuentas o filas (conceptos), las columnas (tipos de datos enumerados) y las fechas finales

categories = { 'accounts': None, 'fields': None, 'end_dates': None }

with open('../data/raw/comparativodeudaactualvs1999-092025.csv', 'r') as dataset:
    records = dataset.read().split('\n')

    accounts, end_dates = [], []
    for record in records:
        tmp = record.split(',')
        accounts.append(tmp[0])
        try:
            end_dates.append(tmp[4])
        except IndexError:
            pass

    accounts = list(dict.fromkeys(accounts))
    if '' in accounts:
        accounts.remove('')
    if 'concepto' in accounts:
        accounts.remove('concepto')

    end_dates = list(dict.fromkeys(end_dates))
    if '' in end_dates:
        end_dates.remove('')
    if 'fecha_final' in end_dates:
        end_dates.remove('fecha_final')

    fields = set(records[0].split(','))

    categories['accounts'] = accounts
    categories['fields'] = fields
    categories['end_dates'] = end_dates

# ---------- Guardar concepts, columns y fechas finales en archivos

with open('../data/interim/accounts.csv', 'w') as accounts:
    for account in categories['accounts']:
        accounts.write(f'{account}\n')

with open('../data/interim/fields.csv', 'w') as fields:
    for field in categories['fields']:
        fields.write(f'{field}\n')

with open('../data/interim/end_dates.csv', 'w') as end_dates:
    for end_date in categories['end_dates']:
        end_dates.write(f'{end_date}\n')

# ---------- Crear nuestra propio diccionario de la forma concepts -> end_final -> balance

data_set = { concept:None for concept in categories['accounts'] }

for account in data_set:
    data_set[account] = { f'{end_date}/1999-12-31':None for end_date in categories['end_dates'] }

for account in data_set:
    for end_date in data_set[account]:
        data_set[account][end_date] = { 'saldo_base_1999': 0, 'saldo_acumulado': 0 }

with open('../data/raw/comparativodeudaactualvs1999-092025.csv', 'r') as dataset:
    records = dataset.read().split('\n')

    for record in records[1:]:
        tmp = record.split(',')
        try:
            target_concept = tmp[0]
            target_date = f'{tmp[4]}/1999-12-31'

            data_set[target_concept][target_date]['saldo_base_1999'] = float(tmp[1])
            data_set[target_concept][target_date]['saldo_acumulado'] = float(tmp[2]) 
        except IndexError:
            pass

# ---------- Guardar el diccionario en un archivo json

import json

with open('../data/processed/deuda_ipab.json', 'w') as dataset_json:
    json.dump(data_set, dataset_json, indent=4)

# ---------- Cargar configuración de json

with open('config.json', 'r') as config_json:
    order = json.load(config_json)['ordered_accounts'] 

# Cargar el json deuda_ipab

with open('../data/processed/deuda_ipab.json', 'r') as dataset_json:
    data = json.load(dataset_json)

# ---------- Reordenar cada objeto de la lista

data_set = {}

for account in order:
    data_set[account] = data[account]

with open('../data/processed/deuda_ipab.json', 'w') as dataset_json:
    json.dump(data_set, dataset_json, indent=4)
