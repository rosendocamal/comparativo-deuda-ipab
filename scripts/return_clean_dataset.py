import json

START_DATE = '1999-12-31'

with open('../data/processed/deuda_ipab.json') as file:
    dataset = json.load(file)

with open('../data/processed/deuda_ipab.csv', 'w') as csv:
    with open('../data/interim/end_dates.csv', 'r') as cutoff_dates:
        dates = cutoff_dates.read().split("\n")

        if '' in dates:
            dates.remove('')

    csv.write(f'CONCEPTO,{START_DATE},{",".join(dates)}\n')
    
    for account in dataset.keys():
        csv.write(f'"{account}",')
        
        initial_balance = 0
        for cutoff_date in dataset[account].keys():
            if initial_balance < dataset[account][cutoff_date]['saldo_base_1999']:
                initial_balance = dataset[account][cutoff_date]['saldo_base_1999']
        csv.write(f'{initial_balance},')
         
        for cutoff_date in dataset[account].keys():
            if tuple(dataset[account].keys())[len(dataset[account].keys()) - 1] != cutoff_date:
                csv.write(f'{float(dataset[account][cutoff_date]['saldo_acumulado'])},')
            else:
                csv.write(f'{float(dataset[account][cutoff_date]['saldo_acumulado'])}\n')
