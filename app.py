from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import MenuModel, KategoriModel, Auth

app = Flask(__name__)
app.secret_key = "fix_total_pasti_jalan"

# --- FILTER RUPIAH ---


@app.template_filter('rupiah')
def rupiah(value):
    try:
        return f"Rp {float(value):,.0f}".replace(',', '.')
    except:
        return f"Rp {value}"


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == 'POST':
        res = Auth().login(email, password)
        print(res)
        email = res['data'].user.email

        if email == 'admin@resto.com':
            role = 'admin'
        else:
            role = 'user'

        session['user_id'] = res['data'].user.id
        session['email'] = res['data'].user.email
        session['role'] = role

        if role == 'admin':
            flash(f'Selamat datang, admin', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash(f'{res["message"]}', 'success')
            return redirect(url_for('landing_page'))

    return render_template('login.html')


@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == 'POST':
        res = Auth().sign_up(email, password)
        flash('Daftar berhasil, silahkan login', 'success')
        return redirect(url_for('login'))

    return render_template('sign_up.html')


@app.route("/")
def landing_page():
    res = MenuModel().get_all()
    # Halaman awal pilihan Admin/Pelanggan
    return render_template("index.html", menus=res.data)


@app.route("/admin")
def admin_dashboard():
    # Menampilkan tabel menu
    menu_list = MenuModel.get_all()
    return render_template("admin_dashboard.html", menus=menu_list.data)

# --- FIX: NAMA FUNGSI DISAMAKAN DENGAN HTML ---


@app.route("/insert_menu", methods=["GET", "POST"])
def insert_menu():
    if request.method == "POST":
        data = {
            "nama_menu": request.form["nama_menu"],
            "id_kategori": int(request.form["id_kategori"]),
            "harga": float(request.form["harga"]),
            "stok": int(request.form["stok"]),
            "deskripsi": request.form["deskripsi"]
        }
        MenuModel.create(data)
        flash("Menu Berhasil Ditambah!", "success")
        return redirect(url_for('admin_dashboard'))

    categories = KategoriModel.get_all()
    print(categories.data[0]['nama_kategori'])
    return render_template("form_menu.html", kategori=categories.data)


@app.route("/insert_kategori")
def insert_kategori():
    return "Fungsi tambah kategori belum aktif."


@app.route("/admin/menu/add")
def add_menu():
    return redirect(url_for('insert_menu'))


@app.route("/admin/menu/edit/<int:menu_id>", methods=["GET", "POST"])
def edit_menu(menu_id):
    if request.method == "POST":
        data = {
            "nama_menu": request.form["nama_menu"],
            "id_kategori": int(request.form["id_kategori"]),
            "harga": float(request.form["harga"]),
            "stok": int(request.form["stok"]),
            "deskripsi": request.form["deskripsi"]
        }
        MenuModel.update(menu_id, data)
        return redirect(url_for('admin_dashboard'))

    menu_data = MenuModel.get_by_id(menu_id)
    kategori_list = KategoriModel.get_all()
    return render_template("edit_menu.html", m=menu_data, kategori=kategori_list.data)


@app.route("/admin/menu/delete/<int:menu_id>")
def delete_menu(menu_id):
    MenuModel.delete(menu_id)
    flash('Data berhasil di hapus.')
    return redirect(url_for('admin_dashboard'))

# --- FIX LOGOUT ---


@app.route("/logout")
def logout():
    session.clear()
    flash('Logout berhasil!', 'success')
    return redirect(url_for('landing_page'))


if __name__ == "__main__":
    app.run(debug=True)
