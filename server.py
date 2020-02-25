import peeweedbevolve
from flask import Flask, render_template, request, flash, redirect, url_for
from models import db, Store, Warehouse  # new line
app = Flask(__name__)

app.secret_key = b'\xcb\x15\rD\x9c\x88\xcf\x99\xbbt\xe9`j\xdf\x1b+'


@app.before_request  # new line
def before_request():
    db.connect()


@app.after_request  # new line
def after_request(response):
    db.close()
    return response


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/store", methods=["GET"])
def show_store():

    return render_template('show_store.html',)


@app.route("/store/create", methods=["POST"])
def create():
    store_name = request.form.get("store_name")
    store = Store(name=store_name)
    # store.save()
    # return redirect(url_for("show_store"))
    try:
        store.save()
        flash(f"Saved store: {store_name}")
        return redirect(url_for("show_store"))
    except:
        flash("That name is already taken")
        return render_template("show_store.html")


@app.route("/warehouse", methods=["GET"])
def warehouse():
    select_store = Store.select()
    return render_template('warehouse.html', select_store=select_store)


@app.route("/warehouse/create", methods=["POST"])
def warehouse_create():
    w = request.form.get("w")
    s = request.form.get("s")
    wh = Warehouse(location=w, store_id=s)
    wh.save()
    return redirect(url_for("warehouse"))


# @app.route("/warehouse/index", method=["GET"], store=store)
# def warehouse_index():
#     store = Store.get_by_id(request.form['store_id'])


@app.route("/warehouse/store_select", )
def store_select():
    select_store = Store.select()


@app.cli.command()  # new
def migrate():  # new
    db.evolve(ignore_tables={'base_model'})  # new


if __name__ == '__main__':
    app.run()
