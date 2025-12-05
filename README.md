1. Analisis Pelanggaran (README.md)
   Masalah awal (code smell): ada satu class ValidatorManager yang menampung banyak logika validasi (validasi SKS, validasi prasyarat, dst.) menggunakan banyak if/else.


Pelanggaran SOLID yang ditemukan:
- SRP (Single Responsibility Principle): ValidatorManager melakukan lebih dari satu tanggung jawab (validasi SKS, prasyarat, jadwal, notifikasi, dll.). Seharusnya satu class hanya punya satu alasan untuk berubah.

- OCP (Open/Closed Principle): Menambah aturan validasi baru (mis. JadwalBentrokRule) mengharuskan mengubah method validate yang berisi banyak if/else. Seharusnya kita bisa menambahkan aturan baru tanpa mengubah kode existing.

- DIP (Dependency Inversion Principle): ValidatorManager atau code yang memanggilnya bergantung langsung pada implementasi konkret (function/if-block), bukan pada abstraksi. Dengan bergantung pada abstraksi (interface IValidationRule), kita bisa menyuntikkan (inject) aturan baru.

Kesimpulan: 
- Solusi yang tepat adalah membuat abstraksi IValidationRule (ABC), membuat kelas-kelas aturan konkret, dan membuat RegistrationService sebagai koordinator yang menerima daftar aturan via dependency injection.
