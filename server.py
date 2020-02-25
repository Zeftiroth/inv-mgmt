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

@app.route("/stores")
def store_select():
    stores = Store.select()
    warehouse = Warehouse.select()
    return render_template('list_stores.html', stores=stores, warehouse=warehouse)


@app.route("/stores/delete/<id>", methods=["POST"])
def store_delete(id):
    store = Store.get_by_id(id)
    store.delete_instance(recursive=True)
    # store_del = Store.delete().where(Store.id == id)
    # store_del.execute()
    return redirect(url_for('store_select'))


@app.route("/store/<id>")
def ind_store_select(id):
    st = Store.get_or_none(Store.id == id)

    if not st:
        return redirect(url_for('show_store'))

    return render_template('ind_store.html', st=st)
    # return f"{id}"


@app.route("/store/<id>/edit",  methods=["POST"])
def store_edit(id):
    ns = request.form.get("ns")

    upd_store = Store.update(name=ns).where(Store.id == id)
    upd_store.execute()

    return redirect(url_for('ind_store_select', id=id))


@app.cli.command()  # new
def migrate():  # new
    db.evolve(ignore_tables={'base_model'})  # new


if __name__ == '__main__':
    app.run()
