# Tugas TST - Program Rasionalisasi Nilai
### by Muhammad Dastin Fauzi - 18221062

#### Pendahuluan
Program rasionalisasi nilai merupakan program API yang digunakan untuk memprediksi apakah nilai dari seorang memenuhi kriteria untuk masuk atau berhasil dalam suatu tes masuk. Pada program ini, hanya diperuntukan untuk rasionalisasi nilai SNMPTN dengan cakupan pada bidang Saintek dan terbatas pada pilihan kampus ITB/UI/UGM. Prediksi yang dilakukan didasarkan atas mock database yang berisi nilai-nilai dari pelajaran yang terkait dengan status keberhasilan dalam angka 1 dan 0 jika gagal. Mock dataset telah disesuaikan oleh penulis sehingga tidak ada data yang outlier. Dalam prediksi kelulusan, program ini dilengkapi oleh machine learning dengan model RandomForestClassifier dikarenakan tidak memerlukan normalisasi data atau penghapusan outliers.

Library yang digunakan yaitu
- fastapi
- uvicorn
- pandas
- scikit-learn

#### Cara Run Via Virtual Enviroment (venv) Python -- Windows
1. Pull repository ini ke dalam local folder
2. Buka terminal di VS Code atau via command prompt bisa
3. Pastikan sudah berada di folder tempat menyimpan repository ini
4. Ketik ```python -m venv [nama virtual enviroment (dibebaskan)]``` lalu enter
5. Masuk ke venv dengan cara ketik ```[nama virtual enviroment (dibebaskan)]\Scripts\activate```
6. Install library terkait. Disini saya menggunakan fastapi, uvicorn, pandas, dan scikit-learn dengan cara ```pip install fastapi uvicorn pandas scikit-learn```
7. Jalankan aplikasi dengan ```uvicorn rasionalisasiNilaiSNM:app --port 8000 --reload```
