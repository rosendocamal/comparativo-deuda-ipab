import json

# ---------- Importar el JSON
with open('../data/processed/deuda_ipab.json') as file:
    datos = json.load(file)

# ---------- Leer archivos y obtener los nombres de cuentas, nombre de columnas y fechas finales
def read_csv(csv):
    with open(f'../data/interim/{csv}', 'r') as file:
        lines = file.read().split('\n')
        if '' in lines:
            lines.remove('')
        return lines

accounts = read_csv('accounts.csv')
end_dates = read_csv('end_dates.csv')

"""
with open('../data/interim/accounts.csv', 'r') as file:
    accounts = file.read().split('\n')
    if '' in accounts:
        accounts.remove('')

with open('../data/interim/fields.csv', 'r') as file:
    fields = file.read().split('\n')
    if '' in fields:
        fields.remove('')

with open('../data/interim/end_dates.csv', 'r') as file:
    end_dates = file.read().split('\n')
    if '' in end_dates:
        end_dates.remove('')
"""

# ---------- Análisis de Crecimiento
# ¿Cuál es la cuenta que más ha crecido en términos porcentuales desde 1999?

first_date = '1999-12-31'

account_and_growth_records = list()

with open('../data/processed/cuentas_crecimiento.csv', 'w') as file_dataset:
    file_dataset.write(f'cuenta,saldo_inicial,saldo_final,crecimiento_porcentual\n')
    for account in accounts:
        if account != 'Pasivos Totales' and account != 'Pasivos Netos':
            initial_balance = datos[account][f'{end_dates[0]}/{first_date}']['saldo_base_1999']
            current_balance = datos[account][f'{end_dates[len(end_dates) - 1]}/{first_date}']['saldo_acumulado']
        
            try:
                account_growth_percentage = round(((current_balance / initial_balance) - 1) * 100, 2)
            except ZeroDivisionError:
                account_growth_percentage = 0
            finally:
                account_and_growth_records.append(account_growth_percentage)
                file_dataset.write(f'"{account}",{initial_balance},{current_balance},{account_growth_percentage}%\n')

max_growth = max(account_and_growth_records)

if max_growth in account_and_growth_records:
    index = account_and_growth_records.index(max_growth)
    print('-'*90)
    print('¿Cuál es la cuenta que más ha crecido en términos porcentuales desde 1999?')
    print('-'*90+'\n')
    print(f'La cuenta "{accounts[index]}" es la que más ha crecido con un crecimiento de {account_and_growth_records[index]}%.\n')
    print(f'Cuenta con un saldo acumulado de ${datos[accounts[index]][f"{end_dates[len(end_dates) - 1]}/{first_date}"]["saldo_acumulado"]} MXN, habiendo en 1999 el monto de ${datos[accounts[index]][f"{end_dates[0]}/{first_date}"]["saldo_base_1999"]} MXN.\n')
    print(f'Contabilizado desde {first_date} hasta {end_dates[len(end_dates) - 1]}.\n')
    print('-'*90 + '\n')

# ¿Cómo se ha comportado la deuda bruta vs la deuda neta?

with open('../data/processed/pasivo_total_vs_neto_crecimiento.csv', 'w') as file_dataset:
    file_dataset.write(f'cuenta,saldo_inicial,saldo_final,diferencia,crecimiento\n')
    date = f'{end_dates[len(end_dates) - 1]}/{first_date}'
    liabilities_growth = list()

    for liability in ['Pasivos Totales', 'Pasivos Netos']:
        initial_balance = datos[liability][date]['saldo_base_1999']
        current_balance = datos[liability][date]['saldo_acumulado']

        try:
            liability_growth = round(((current_balance / initial_balance) - 1) * 100, 2)
        except ZeroDivisionError:
            liability_growth = 0
        finally:
            liabilities_growth.append(liability_growth)
            file_dataset.write(f'"{liability}",{initial_balance},{current_balance},{round(current_balance - initial_balance, 2)},{liability_growth}%\n')
            
print('-' * 90)
print('Crecimiento Pasivo Total vs Neto')
print('=' * 90)
print(f'Pasivos Totales\t\t{liabilities_growth[0]}%')
print(f'Pasivos Netos\t\t{liabilities_growth[1]}%')
print('-' * 90 + '\n')
