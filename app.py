from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import MenuModel, KategoriModel

app = Flask(__name__)
app.secret_key = "fix_total_pasti_jalan"

# --- FILTER RUPIAH ---
@app.template_filter('format_rupiah')
def format_rupiah(value):
    try:
        return f"Rp {float(value):,.0f}".replace(',', '.')
    except:
        return f"Rp {value}"

@app.route("/")
def landing_page():
    # Halaman awal pilihan Admin/Pelanggan
    return render_template("index.html")

@app.route("/admin")
def admin_dashboard():
    # Menampilkan tabel menu
    menu_list = MenuModel.get_all()
    return render_template("admin_dashboard.html", menus=menu_list)

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
    return render_template("form_menu.html", kategori=categories)

# --- FIX: NAMA FUNGSI KATEGORI ---
@app.route("/insert_kategori")
def insert_kategori():
    return "Fungsi tambah kategori belum aktif."

# Alias rute add_menu agar tidak error jika ada tombol lain manggil ini
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
    return render_template("edit_menu.html", m=menu_data, kategori=kategori_list)

@app.route("/admin/menu/delete/<int:menu_id>")
def delete_menu(menu_id):
    MenuModel.delete(menu_id)
    return redirect(url_for('admin_dashboard'))

# --- FIX LOGOUT ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('landing_page'))

if __name__ == "__main__":
    app.run(debug=True)