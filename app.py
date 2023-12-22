from db import db
from flask import Flask, render_template, request, redirect

db = db()
app = Flask(__name__)

TABLES_LIST = db.get_tables_list()
TABLES_COUNT = len(TABLES_LIST)
STATS_COUNT = 5


def get_stats(statistic_id: int):
    headers = data = []
    stat_name = ""
    if statistic_id == 1:
        q = "SELECT SUM(material_order.cost_order) as СУММА_ЗАКУПКИ, SUM(factory_order.summa) as СУММА_ПРОДАЖИ" \
            " FROM material_order " \
            "JOIN factory_order ON 1=1"
        stat_name = "Сумма закупки материалов и сумма продажи готовой продукции"
        headers = db.get_headers(q)
        data = db.get_all_rows_from_table(q)
    elif statistic_id == 2:
        q = "SELECT provider.name_provider AS ПОСТАВЩИК, SUM(cost_order) as СУММА " \
            "FROM provider " \
            "JOIN material_order " \
            "ON provider.id_provider = material_order.id_provider " \
            "GROUP BY provider.id_provider"
        stat_name = "Поставщики и общая сумма, на которую у них были закуплены материалы"
        headers = db.get_headers(q)
        data = db.get_all_rows_from_table(q)
    elif statistic_id == 3:
        q = "SELECT material.name_material AS МАТЕРИАЛ, " \
            "material_supply.date_supplly AS ДАТА_ПОСТАВКИ, " \
            "SUM(material_supply.volume) AS КОЛИЧЕСТВО " \
            "FROM material JOIN material_supply " \
            "ON material_supply.id_material = material.id_material " \
            "GROUP BY material.name_material, material_supply.date_supplly " \
            "ORDER BY ДАТА_ПОСТАВКИ DESC"
        stat_name = "Поставка материалов по дням"
        headers = db.get_headers(q)
        data = db.get_all_rows_from_table(q)
    elif statistic_id == 4:
        q = "SELECT DISTINCT product.name_product ПРОДУКЦИЯ, " \
            "SUM(summa) AS СУММА " \
            "FROM factory_order " \
            "JOIN product on product.id_product = factory_order.id_product " \
            "GROUP BY product.id_product " \
            "ORDER BY СУММА"
        stat_name = "Сумма на которую заказали продукции"
        headers = db.get_headers(q)
        data = db.get_all_rows_from_table(q)
    elif statistic_id == 5:
        q = "SELECT name_product AS ПРОДУКТ, (cost_product * volume) AS ОБЩАЯ_СТОИМОСТЬ " \
            "FROM product"
        stat_name = "Общая стоимость имеющейся продукции"
        headers = db.get_headers(q)
        data = db.get_all_rows_from_table(q)

    return stat_name, headers, data


def check_val(value: str, length: int):
    if not value.isdigit():
        return False
    if int(value) <= 0 or int(value) > length:
        return False
    return True


@app.route('/edit', methods=['GET', 'POST'])
def edit_data():
    table_id = request.args.get("table")
    row = request.args.get("row")

    if request.method == "POST":
        table_id = request.form.get("table")
        row = request.form.get("row")
        table = TABLES_LIST[int(table_id) - 1]
        q = f"SELECT * FROM {table}"
        headers = db.get_headers(q)
        editing_row = db.get_all_rows_from_table(q)[int(row)]
        data = [val for val in request.form.values()][2:]

        query = f"UPDATE {table} SET {headers[0]}=%s"
        query_end = f" WHERE {headers[0]}='{editing_row[0]}'"

        for i in range(1, len(headers)):
            query += f",{headers[i]}=%s"
            query_end += f" AND {headers[i]}='{editing_row[i]}'"
        if db.exec(query + query_end, data=data):
            print(query + query_end, data)
            return render_template("edit_row.html", tables_list=TABLES_LIST, success=True)
        else:
            return render_template("edit_row.html", tables_list=TABLES_LIST, success=False)

    if row:
        if row.isdigit():
            q = f"SELECT * FROM {TABLES_LIST[int(table_id) - 1]}"
            headers = db.get_headers(q)
            editing_row = db.get_all_rows_from_table(q)[int(row)]
            print(editing_row)
            return render_template("edit_row.html", headers=headers, table_id=table_id, row=row, data=editing_row)
    if table_id:
        if check_val(table_id, TABLES_COUNT):
            q = "SELECT * FROM " + TABLES_LIST[int(table_id) - 1]

            headers = db.get_headers(q)
            data = db.get_all_rows_from_table(q)

            return render_template("edit.html", tables_list=TABLES_LIST, headers=headers, data=data, table_id=table_id)
    return render_template("edit.html", tables_list=TABLES_LIST)


@app.route('/delete', methods=['GET', 'POST'])
def delete_data():
    table_id = request.args.get("table")
    success = request.args.get("success")
    if success:
        return render_template("delete.html", tables_list=TABLES_LIST, success=success)
    if request.method == "POST":
        redirect("/")
        r = request.json.get('selectedRows')
        table_id = int(r[0])
        selected = r[1:]
        table = TABLES_LIST[table_id - 1]
        headers = db.get_headers(f"SELECT * FROM {table}")
        rows = db.get_all_rows_from_table(f"SELECT * FROM {table}")

        deleted = True
        for row_id in selected:
            row = rows[row_id]
            query = f"DELETE FROM {table} WHERE {headers[0]}='{row[0]}'"
            for i in range(1, len(headers)):
                query += f" AND {headers[i]}='{row[i]}'"
            if not db.exec(query):
                deleted = False
        if deleted:
            return render_template("delete.html", tables_list=TABLES_LIST, success=deleted)
        else:
            return render_template("delete.html", tables_list=TABLES_LIST, success=deleted)

    if table_id:
        if check_val(str(table_id), TABLES_COUNT):
            q = "SELECT * FROM " + TABLES_LIST[int(table_id) - 1]

            headers = db.get_headers(q)
            data = db.get_all_rows_from_table(q)

            return render_template("delete.html", tables_list=TABLES_LIST, headers=headers, data=data, table_id=table_id)
        else:
            return render_template("delete.html", tables_list=TABLES_LIST, error=True)
    return render_template("delete.html", tables_list=TABLES_LIST)


@app.route('/insert', methods=['GET', 'POST'])
def insert_in_table():
    table_id = request.args.get("table")

    if request.method == "POST":
        table_id = request.form.get("table")
        table = TABLES_LIST[int(table_id) - 1]
        headers = db.get_headers(f"SELECT * FROM {table}")
        data = [val for val in request.form.values()]

        query = f"INSERT INTO {table}({headers[0]}"
        for i in range(1, len(headers)):
            query += f",{headers[i]}"
        query += ") VALUES ("
        for i in range(len(headers)):
            query += "'" + str(data[i + 1]) + "',"
        query = query[:len(query) - 1] + ")"
        if db.exec(query):
            return render_template("insert.html", tables_list=TABLES_LIST, success=True)
        else:
            return render_template("insert.html", tables_list=TABLES_LIST, success=False)

    if table_id:
        if not check_val(table_id, TABLES_COUNT):
            return render_template("insert.html", tables_list=TABLES_LIST, error=True)

        headers = db.get_headers(f"SELECT * FROM {TABLES_LIST[int(table_id) - 1]}")

        return render_template("insert.html", tables_list=TABLES_LIST, headers=headers, value=table_id)

    return render_template("insert.html", tables_list=TABLES_LIST)


@app.route('/print')
def print_table():
    table_id = request.args.get("table")

    if table_id:
        if check_val(table_id, TABLES_COUNT):
            q = "SELECT * FROM " + TABLES_LIST[int(table_id) - 1]

            headers = db.get_headers(q)
            data = db.get_all_rows_from_table(q)

            return render_template("print.html", table_name=TABLES_LIST[int(table_id) - 1], headers=headers, data=data)
        else:
            return render_template("print.html", tables_list=TABLES_LIST, error=True)
    return render_template("print.html", tables_list=TABLES_LIST)


@app.route('/stats')
def statistics():
    statistic_id = request.args.get("statistic")
    if statistic_id:
        if check_val(statistic_id, STATS_COUNT):
            stat_name, headers, data = get_stats(int(statistic_id))
            return render_template("stats.html", stat_name=stat_name, headers=headers, data=data)
        else:
            return render_template("stats.html", error=True)
    return render_template("stats.html")


@app.route('/')
def index():
    choice = request.args.get('choice')
    if choice == '1':
        return redirect("/print")
    if choice == '2':
        return redirect("/insert")
    if choice == '3':
        return redirect("/delete")
    if choice == '4':
        return redirect("/edit")
    if choice == '5':
        return redirect("/stats")
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
