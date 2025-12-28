from models import supabase

def daftar():
    # DAFTAR ADMIN
    try:
        supabase.auth.sign_up({
            "email": "admin@resto.com", # Ini Username/Email Anda
            "password": "password123",  # Ini Password Anda
            "options": {"data": {"role": "admin"}}
        })
        print("Akun ADMIN berhasil dibuat: admin@resto.com / password123")
    except Exception as e:
        print(f"Gagal/Sudah ada: {e}")

    # DAFTAR CUSTOMER
    try:
        supabase.auth.sign_up({
            "email": "pembeli@gmail.com",
            "password": "password123",
            "options": {"data": {"role": "customer"}}
        })
        print("Akun CUSTOMER berhasil dibuat: pembeli@gmail.com / password123")
    except Exception as e:
        print(f"Gagal/Sudah ada: {e}")

if __name__ == "__main__":
    daftar()