from models import supabase

# Jalankan satu per satu
def create_users():
    # Buat Admin
    try:
        supabase.auth.sign_up({
            "email": "admin@resto.com",
            "password": "password123",
            "options": {"data": {"role": "admin"}}
        })
        print("Akun Admin berhasil dibuat!")
    except:
        print("Admin mungkin sudah ada.")

    # Buat Customer
    try:
        supabase.auth.sign_up({
            "email": "customer@gmail.com",
            "password": "password123",
            "options": {"data": {"role": "customer"}}
        })
        print("Akun Customer berhasil dibuat!")
    except:
        print("Customer mungkin sudah ada.")

if __name__ == "__main__":
    create_users()