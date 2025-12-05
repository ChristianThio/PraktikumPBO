# BAD VALIDATOR (contoh kode buruk)

class RegistrationService:
    def __init__(self):
        self.users = []

    def register(self, username, email):

        # ---- VALIDASI YANG BURUK ----
        # 1. Campur ke logika register
        # 2. Tidak reusable
        # 3. Magic condition
        # 4. Jika nanti ada aturan baru → harus ubah class ini (melanggar OCP)
        if len(username) < 3:
            print("Gagal: Username harus lebih dari 3 karakter.")
            return False

        if "@" not in email or "." not in email:
            print("Gagal: Email tidak valid.")
            return False

        # ------------------------------------------------

        # Simpan user (langsung di sini → melanggar SRP)
        self.users.append({
            "username": username,
            "email": email
        })

        # Kirim email (logika campur → melanggar SRP)
        print(f"Mengirim email selamat datang ke {email}...")

        print("Registrasi berhasil!")
        return True


# Contoh pemakaian
if __name__ == "__main__":
    service = RegistrationService()
    service.register("an", "salah-email")    # gagal
    service.register("budi", "budi@mail.com")  # sukses
