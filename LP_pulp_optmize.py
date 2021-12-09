import pulp
# import numpy as np
import pandas as pd
import re
import sqlite3
import datetime as dt
import os.path as path

from pulp import value as value_op


def create_database(ted, name):
    headers = []
    for row in ted:
        headers.append(row)

    conn = sqlite3.connect(name + '.db')
    cursor = conn.cursor()
    # Create table - CLIENTS
    cursor.execute('DROP TABLE IF EXISTS tb_person')
    strQuery = "CREATE TABLE IF NOT EXISTS tb_person (id_main INTEGER PRIMARY KEY AUTOINCREMENT, "
    for i in range(len(headers)):
        if i < len(headers) - 1:
            strQuery += str(headers[i]) + " text, "
        else:
            strQuery += str(headers[i]) + " text) "

    cursor.execute(strQuery)

    query = "INSERT INTO tb_person ("
    for i in range(len(headers)):
        if i < len(headers) - 1:
            query += str(headers[i]) + " , "
        else:
            query += str(headers[i]) + " ) "
    query += "VALUES("
    for i in range(len(headers)):
        if i < len(headers) - 1:
            query += "?" + ", "
        else:
            query += "?) "

    for i in range(len(ted.index)):
        row_value = ted.iloc[i]
        cursor.execute(query, row_value)
    conn.commit()
    conn.close()


def getGroupName(col_name):
    conn = sqlite3.connect('temp_data.db')
    cursor = conn.cursor()
    query = "select " + col_name + " from tb_person group by " + col_name
    result = cursor.execute(query)
    count_person_rows = result.fetchall()
    arr_col = []
    for col in count_person_rows:
        arr_col.append(col[0])

    # print(arr_col)
    conn.close()
    return arr_col


def get_optimize():
    # crete universe request file
    name = "USD_IG_GC"
    ted = pd.read_excel("H:/Python/Tools/port_optimization/" + name + ".xlsx")

    # create database for group by, for data process
    create_database(ted, name)

    data = ted

    selected_cols = ['ID', 'ticker', 'spread', 'duration', 'sector', 'country', 'rating', 'rank', 'rating_score', 'currency']

    data = data[selected_cols]
    data.reset_index(inplace=True)

    # create the LP object
    # set up as a maximization problem
    prob = pulp.LpProblem('Spread Maximization', pulp.LpMaximize)

    # create decision -yes or no to select
    decision_variables = []
    for rownum, row in data.iterrows():
        variable = str('x' + str(row['index']))

        if row['rank'] == 'SUB':
            variable = pulp.LpVariable(str(variable), lowBound=0, upBound=0.0075, cat='Continuous')
        else:
            if row['rating'] == 'AAA':
                variable = pulp.LpVariable(str(variable), lowBound=0, upBound=0.02, cat='Continuous')
            elif row['rating'] == 'AA':
                variable = pulp.LpVariable(str(variable), lowBound=0, upBound=0.02, cat='Continuous')
            elif row['rating'] == 'A':
                variable = pulp.LpVariable(str(variable), lowBound=0, upBound=0.02, cat='Continuous')
            elif row['rating'] == 'BBB':
                variable = pulp.LpVariable(str(variable), lowBound=0, upBound=0.015, cat='Continuous')
            else:
                variable = pulp.LpVariable(str(variable), lowBound=0, upBound=0, cat='Continuous')

        # variable = pulp.LpVariable(str(variable), lowBound = 0, upBound = 1, cat = 'Continuous') # make variables binary
        decision_variables.append(variable)

    print("Total number of decision_variables: " + str(len(decision_variables)))
    total_yields = ""

    for rownum, row in data.iterrows():
        for i, yield_i in enumerate(decision_variables):
            if rownum == i:
                formula = row["spread"] * yield_i
                total_yields += formula

    prob += total_yields
    # print("Optimization function: " + str(total_yields))
    # print("Prob :", prob)

    # total duration Constraints
    duration_sum = ""
    min_duration_available = 0
    max_duration_available = 7
    for rownum, row in data.iterrows():
        for i, yield_i in enumerate(decision_variables):
            if rownum == i:
                formula = row["duration"] * yield_i
                duration_sum += formula
    prob += (min_duration_available <= duration_sum <= max_duration_available)

    # total score Constraints
    score_sum = ""
    min_score_available = 1
    max_score_available = 7.4
    for rownum, row in data.iterrows():
        for i, yield_i in enumerate(decision_variables):
            if rownum == i:
                formula = row["rating_score"] * yield_i
                score_sum += formula
    prob += (min_score_available <= score_sum <= max_score_available)

    # sector constraints
    sectors = data['sector'].drop_duplicates().to_list()
    # ex: Financials ==  x33 + x45 + x50 +... <= 0.2,

    for j in range(len(sectors)):
        sectors_sum = ""
        for rownum, row in data.iterrows():
            for i, yield_i in enumerate(decision_variables):
                if rownum == i:
                    if sectors[j] == row["sector"]:
                        formula = 1 * yield_i
                    else:
                        formula = 0 * yield_i
                    sectors_sum += formula

        prob += (sectors_sum <= 0.20)

    # country constraints
    countrys = data['country'].drop_duplicates().to_list()

    for j in range(len(countrys)):
        countrys_sum = ""
        for rownum, row in data.iterrows():
            for i, yield_i in enumerate(decision_variables):
                if rownum == i:
                    if countrys[j] == row["country"]:
                        formula = 1 * yield_i
                    else:
                        formula = 0 * yield_i
                    countrys_sum += formula

        prob += (countrys_sum <= 0.25)
    """
    # currency constraints
    usd = ["USD"]

    for j in range(len(usd)):
        usd_sum = ""
        for rownum, row in data.iterrows():
            for i, yield_i in enumerate(decision_variables):
                if rownum == i:
                    if usd[j] == row["currency"]:
                        formula = 1 * yield_i
                    else:
                        formula = 0 * yield_i
                    usd_sum += formula

        prob += (usd_sum <= 0.4)
    
    """
    # rating constraints
    tickers = data['ticker'].drop_duplicates().to_list()
    for j in range(len(tickers)):
        tickers_sum = ""
        rating_ticker = 0
        for rownum, row in data.iterrows():
            for i, yield_i in enumerate(decision_variables):
                if rownum == i:
                    if tickers[j] == row["ticker"]:
                        if row["rating"] == "AAA":
                            rating_ticker = 0.02
                        elif row["rating"] == 'AA':
                            rating_ticker = 0.02
                        elif row["rating"] == "A":
                            rating_ticker = 0.02
                        elif row["rating"] == 'BBB':
                            rating_ticker = 0.015
                        formula = 1 * yield_i
                    else:
                        formula = 0 * yield_i
                    tickers_sum += formula
            # print(tickers_sum)
        prob += (tickers_sum <= rating_ticker)

        # total sub allocation constraint by 10%
    """
    subs = ["SUB"]

    for j in range(len(subs)):
        subs_sum = ""
        for rownum, row in data.iterrows():
            for i, yield_i in enumerate(decision_variables):
                if rownum == i:
                    if subs[j] == row["rank"]:
                        formula = 1 * yield_i
                    else:
                        formula = 0 * yield_i
                    subs_sum += formula

        prob += (subs_sum <= 0.0)
    """

    # total allocation Constraints
    alloc_sum = ""
    for rownum, row in data.iterrows():
        for i, yield_i in enumerate(decision_variables):
            if rownum == i:
                formula = yield_i
                alloc_sum += formula
    prob += (alloc_sum == 1)

    # final format
    prob.writeLP(name + ".lp")

    # actual optimiztion
    optimization_result = prob.solve()
    # assert optimization_result == pulp.LpStatusOptimal

    print("status:", LpStatus[prob.status])
    print("Optimal Solution: ", value_op(prob.objective))

    # print("Individual decision_variables:")
    # for v in prob.variables():
    #	try:
    #		if v.varValue > 0:
    #			print(v.name, "=", v.varValue)
    #	except:
    #		pass

    # reorder results
    variable_name = []
    variable_value = []

    for v in prob.variables():
        variable_name.append(v.name)
        variable_value.append(v.varValue)

    df = pd.DataFrame({'index': variable_name, 'allocation': variable_value})
    # print(df)
    df = df.loc[df['allocation'] > 0]
    df['index'] = df['index'].str.replace('x', '').astype(int)

    df = df.sort_values(by='index')

    result = pd.merge(data, df, on='index')
    result = result[result["allocation"] > 0].sort_values(by='allocation', ascending=False)

    selected_cols_final = ['ID', 'ticker', 'spread', 'duration', 'sector', 'country', 'rating', 'rating_score', 'rank',
                           'currency', 'allocation']

    final_set_of_yield = result[selected_cols_final]

    print("Duration: " + str((final_set_of_yield["duration"] * final_set_of_yield["allocation"]).sum()))

    file = False
    while file == False:
        try:
            final_set_of_yield.to_excel(
                "H:/Python/Tools/port_optimization/" + dt.datetime.today().strftime("%Y-%m-%d") + name + "_result.xlsx",
                index=False)
            file = True
            print("Optimized Portfolio has been saved: " + dt.datetime.today().strftime("%Y-%m-%d") + name + "_result.xlsx")
        except:
            input("Please close file to proceed...")
    # print(final_set_of_yield)


def get_universe():
    link = "I:/ABT_IM/PMAR/Renten/Credits/Data/Market/Index/"
    xist = False
    date = dt.datetime.today()

    while xist == False:

        if path.isfile(link + date.strftime('%Y%m%d') + "_iboxx_eur_eod_underlyings.xlsx"):
            xist = True
            df = pd.read_excel(link + date.strftime('%Y%m%d') + "_iboxx_eur_eod_underlyings.xlsx")
            print("Data as of " + date.strftime("%Y-%m-%d") + " are ready to use.")
        else:
            date = date - dt.timedelta(1)
    col = ['ISIN', 'Ticker', 'OAS', 'Street Modified Duration', 'Level 3', 'Issuer Country', 'Markit iBoxx Rating',
           'Seniority Level 1']
    df = df[col]
    selected_cols = ['ID', 'ticker', 'spread', 'duration', 'sector', 'country', 'rating', 'rank', 'rating_score']

    return df


if __name__ == "__main__":
    # get_universe().to_excel("H:/Python/Tools/port_optimization/index.xlsx")

    get_optimize()
