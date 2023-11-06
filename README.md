# Tugas TST - Microservice Deployment: Program Rasionalisasi Nilai
## by Muhammad Dastin Fauzi - 18221062
### [FastAPI-Rasionalisasi-Nilai-via-FQDN](http://tugaststcorerasionalisasi.f4d0ezdmbgb7c9bb.southeastasia.azurecontainer.io/docs#/)
### [FastAPI-Rasionalisasi-Nilai-via-IP_Address_Public](http://20.247.227.210/docs)

### Pendahuluan
Program rasionalisasi nilai merupakan program API yang digunakan untuk memprediksi apakah nilai dari seorang memenuhi kriteria untuk masuk atau berhasil dalam suatu tes masuk. Pada program ini, hanya diperuntukan untuk rasionalisasi nilai SNMPTN dengan cakupan pada bidang Saintek dan terbatas pada pilihan kampus ITB/UI/UGM. Prediksi yang dilakukan didasarkan atas mock database yang berisi nilai-nilai dari pelajaran yang terkait dengan status keberhasilan dalam angka 1 dan 0 jika gagal. Mock dataset telah disesuaikan oleh penulis sehingga tidak ada data yang outlier. Dalam prediksi kelulusan, program ini dilengkapi oleh machine learning dengan model RandomForestClassifier dikarenakan tidak memerlukan normalisasi data atau penghapusan outliers.

Library yang digunakan yaitu
- fastapi
- uvicorn
- pandas
- scikit-learn

### Cara Run Via Virtual Enviroment (venv) Python -- Windows
1. Pull repository ini ke dalam local folder
2. Buka terminal di VS Code atau via command prompt bisa
3. Pastikan sudah berada di folder tempat menyimpan repository ini
4. Buat virtual enviroment (venv)
```
python -m venv <nama virtual enviroment (dibebaskan)>
``` 
5. Masuk ke venv
```
<nama virtual enviroment (dibebaskan)>\Scripts\activate
```
6. Install library terkait. Disini saya menggunakan fastapi, uvicorn, pandas, dan scikit-learn dengan cara
```
pip install fastapi uvicorn pandas scikit-learn
```
7. Jalankan aplikasi
```
uvicorn rasionalisasiNilaiSNM:app --port 8000 --reload
```

### Cara Buat Code ini Hingga Deploy ke Microsoft Azure
#### 1. Pull code ini ke dalam suatu folder lalu masuk ke VS Code di folder itu
#### 2. Buat virtual enviroment (venv)
```
python -m venv <nama_venv_bebas>
```
#### 3. Masuk ke venv untuk windows
```
<nama_venv_bebas>\Scripts\activate
```
#### 4. Install library terkait
```
pip install fastapi uvicorn pandas scikit-learn
```
#### 5. Pastikan Dockerfile sudah terisi
```
# Use the official Python image from the Docker Hub
FROM python:3

# Set the working directory inside the container
ADD <file_name.py> .

# Copy the current directory contents into the container at /app
COPY . /<folder_name>
WORKDIR /<folder_name>

# Install any necessary dependencies
RUN pip install fastapi uvicorn <other packages>

# Command to run the FastAPI server when the container starts
CMD ["uvicorn", "<folder_name>", "--host=0.0.0.0", "--port=80"]
```
#### 6. Buat Azure Container Registry Service
#### 7. Buka folder terkait lalu login ke Azure Server Container Registry dengan Docker
```
docker login <container_server> -u <container_username> -p <container_password>
```
#### 8. Buat docker image
```
docker build -t <container_server>/<image_name>:<image_tag> .
```
#### 9. Push docker image
```
docker push <container_server>/<image_name>:<image_tag>
```
#### 10. Buat Azure Instance menyesuaikan dengan lokasi Container Registry
