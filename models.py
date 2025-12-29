from supabase import create_client, Client

SUPABASE_URL = "https://xlflptaouhxnjyqarsgt.supabase.co"
# WAJIB: Pakai Service Role Key / Secret Key kamu!
SUPABASE_KEY = "sb_secret_V6Vw8Xox8OgPgbEqCiFxqA_VZ_r8g2E"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


class MenuModel:
    @staticmethod
    def get_all():
        res = supabase.table("menu").select(
            "*, kategori(nama_kategori)").execute()
        return res

    @staticmethod
    def get_by_id(menu_id):
        res = supabase.table("menu").select(
            "*").eq("id", menu_id).single().execute()
        return res.data

    @staticmethod
    def create(data):
        return supabase.table("menu").insert(data).execute()

    @staticmethod
    def update(menu_id, data):
        return supabase.table("menu").update(data).eq("id", menu_id).execute()

    @staticmethod
    def delete(menu_id):
        return supabase.table("menu").delete().eq("id", menu_id).execute()


class KategoriModel:
    @staticmethod
    def get_all():
        res = supabase.table("kategori").select("*").execute()
        return res


class Auth:
    @staticmethod
    def login(email, password):
        try:
            res = supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })

            return {
                "message": "Login berhasil!",
                "data": res
            }
        except Exception as e:
            print("Error detail: ", str(e))
            return "Error cok"

    @staticmethod
    def sign_up(email, password):
        try:
            res = supabase.auth.sign_up({
                "email": email,
                "password": password
            })

            return {
                "message": "Daftar berhasil!",
                "data": res
            }
        except Exception as e:
            print("Error detail: ", e)
            return "Customer sudah terdaftar."
