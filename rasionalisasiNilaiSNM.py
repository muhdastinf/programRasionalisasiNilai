from fastapi import FastAPI, HTTPException
import json
from pydantic import BaseModel

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class InputUser(BaseModel):
    idUser: int
    userName: str
    kampusTujuan: str
    nilaiMatW: int
    nilaiMatM: int
    nilaiFis: int
    nilaiKim: int
    nilaiBio: int
    nilaiInd: int
    nilaiIng: int

class DataUser(BaseModel):
    idUser: int
    userName: str

app = FastAPI()

# Membuka dan membaca JSON untuk user_rasionalisasi dan hasil_rasionalisasi
with open("user_rasionalisasi.json", "r") as read_file:
    user_rasionalisasi = json.load(read_file)

with open("hasil_rasionalisasi.json", "r") as read_file:
    hasil_rasionalisasi = json.load(read_file)  

# Membaca file dataset nilai SNM untuk ITB UI dan UGM
dataNilaiITB = pd.read_csv("mockDatasetSNMITBFix.csv")
dataNilaiUI = pd.read_csv("mockDatasetSNMUIFix.csv")
dataNilaiUGM = pd.read_csv("mockDatasetSNMUGMFix.csv")

# Memisahkan fitur (X) dan label (y)
X_itb = dataNilaiITB[["NilaiMatW", "NilaiMatM", "NilaiFis", "NilaiKim", "NilaiBio", "NilaiInd", "NilaiIng"]]
y_itb = dataNilaiITB["Status"]

X_ui = dataNilaiUI[["NilaiMatW", "NilaiMatM", "NilaiFis", "NilaiKim", "NilaiBio", "NilaiInd", "NilaiIng"]]
y_ui = dataNilaiUI["Status"]

X_ugm = dataNilaiUGM[["NilaiMatW", "NilaiMatM", "NilaiFis", "NilaiKim", "NilaiBio", "NilaiInd", "NilaiIng"]]
y_ugm = dataNilaiUGM["Status"]

# Inisialisasi model RandomForestClassifier dan melatih model
model_itb = RandomForestClassifier()
model_itb.fit(X_itb.values, y_itb.values)

model_ui = RandomForestClassifier()
model_ui.fit(X_ui.values, y_ui.values)

model_ugm = RandomForestClassifier()
model_ugm.fit(X_ugm.values, y_ugm.values)

# Fungsi untuk save ke json setiap hasil_rasionalisasi dilakukan
def save_result_to_json(data, filename):
    with open(filename, "w") as write_file:
        json.dump(data, write_file)

# Mendapatkan seluruh riwayat hasil rasionalisasi
@app.get('/hasil')
async def read_data_hasil_rasionalisasi():
    return hasil_rasionalisasi['hasil']

# Mendapatkan riwayat hasil rasionalisasi untuk user_id tertentu
@app.get('/hasil/{user_id}')
async def get_data_hasil_rasionalisasi_user(user_id: int):
    matching_user = []
    for hasil in hasil_rasionalisasi['hasil']:
        if hasil['idUser'] == user_id:
            matching_user.append(hasil)

    if not matching_user:
        raise HTTPException(
            status_code=404, detail=f'User ID belum pernah melakukan rasionalisasi atau tidak terdaftar'
        )

    return matching_user

# Mendapatkan seluruh user yang berhak melakukan rasionalisasi
@app.get('/user')
async def read_data_user_rasionalisasi():
    return user_rasionalisasi['user']

# Mengecek apakah user ini berhak melakukan rasionalisasi
@app.get('/user/{user_id}')
async def get_data_user_rasionalisasi(user_id: int):
    for user in user_rasionalisasi['user']:
        if user['idUser'] == user_id:
            return user
    raise HTTPException(
         status_code=404, detail=f'User ID tidak sesuai.'
    )

# Melakukan post ke dalam JSON user_rasionalisasi dan mengembalikan daftar user yang berhak rasionalisasi
@app.post('/add_user')
async def add_user(dataUser: DataUser):
    data = dataUser.dict()
    dataUser_found = False
    for user in user_rasionalisasi['user']:
        if user['idUser'] == data['idUser'] or user['userName'] == data['userName']:
            dataUser_found = True
            return "User " + str(user['idUser']) + " dengan username " + str(user['userName']) + " telah terdaftar."
        
    if not dataUser_found:
        user_rasionalisasi['user'].append(data)
        save_result_to_json(user_rasionalisasi, "user_rasionalisasi.json")
        return data

    raise HTTPException(
         status_code=404, detail=f'User not found'
    )

# Melakukan post ke dalam JSON hasil_rasionalisasi dan mengembalikan hasil rasionalisasi
@app.post('/rasionalisasikan')
async def add_hasil_rasionalisasi(item: InputUser):
    item_dict = item.dict()
    i=1

    arr_input = [item_dict.get("nilaiMatW"), item_dict.get("nilaiMatM"), item_dict.get("nilaiFis"), item_dict.get("nilaiKim"), item_dict.get("nilaiBio"), item_dict.get("nilaiInd"), item_dict.get("nilaiIng")]

    rasionalisasi_ITB = model_itb.predict([arr_input])
    rasionalisasi_UI = model_ui.predict([arr_input])
    rasionalisasi_UGM = model_ugm.predict([arr_input])

    rasionalisasi_ITB = (rasionalisasi_ITB.tolist())[0]
    rasionalisasi_UI = (rasionalisasi_UI.tolist())[0]
    rasionalisasi_UGM = (rasionalisasi_UGM.tolist())[0]

   
    kampusTujuan = item_dict.get("kampusTujuan")

    if kampusTujuan == "ITB":
        if any(0<= x <=75 for x in arr_input):
            hasil_prediksi = "Anda berpeluang TIDAK LULUS ITB pada SNMPTN 2024."
        else:
            if any((x >= 101 or x <= -1) for x in arr_input):
                hasil_prediksi = "Anda berpeluang TIDAK LULUS ITB pada SNMPTN 2024. Periksa kembali input nilai Anda!"
            else: 
                if (rasionalisasi_ITB) == 1:
                    hasil_prediksi = "Anda berpeluang LULUS ITB pada SNMPTN 2024."
                elif (rasionalisasi_ITB) == 0:
                    hasil_prediksi = "Anda berpeluang TIDAK LULUS ITB pada SNMPTN 2024."

    elif kampusTujuan == "UI":
        if any(0<= x <=75 for x in arr_input):
            hasil_prediksi = "Anda berpeluang TIDAK LULUS UI pada SNMPTN 2024."
        else:
            if any((x >= 101 or x <= -1) for x in arr_input):
                hasil_prediksi = "Anda berpeluang TIDAK LULUS UI pada SNMPTN 2024. Periksa kembali input nilai Anda!"
            else: 
                if (rasionalisasi_UI) == 1:
                    hasil_prediksi = "Anda berpeluang LULUS UI pada SNMPTN 2024."
                elif (rasionalisasi_UI) == 0:
                    hasil_prediksi = "Anda berpeluang TIDAK LULUS UI pada SNMPTN 2024."

    elif kampusTujuan == "UGM":
        if any(0<= x <=75 for x in arr_input):
            hasil_prediksi = "Anda berpeluang TIDAK LULUS UGM pada SNMPTN 2024."
        else:
            if any((x >= 101 or x <= -1) for x in arr_input):
                hasil_prediksi = "Anda berpeluang TIDAK LULUS UGM pada SNMPTN 2024. Periksa kembali input nilai Anda!"
            else: 
                if (rasionalisasi_UGM) == 1:
                    hasil_prediksi = "Anda berpeluang LULUS UGM pada SNMPTN 2024."
                elif (rasionalisasi_UGM) == 0:
                    hasil_prediksi = "Anda berpeluang TIDAK LULUS UGM pada SNMPTN 2024."

    else:
        hasil_prediksi = "Masukkan kampus yang benar. Pilihan rasionalisasi saat ini hanya ITB/UI/UGM."

    for user in user_rasionalisasi['user']:
        if user['idUser'] == item_dict['idUser']:
            for count in hasil_rasionalisasi['hasil']:
                i+=1
            
            result = {
                "idHasil": i,
                "idUser": item_dict['idUser'],
                "nameUser": item_dict['userName'],
                "kampusTujuan": item_dict['kampusTujuan'],
                "nilaiMatW": item_dict['nilaiMatW'],
                "nilaiMatM": item_dict['nilaiMatM'],
                "nilaiFis": item_dict['nilaiFis'],
                "nilaiKim": item_dict['nilaiKim'],
                "nilaiBio": item_dict['nilaiBio'],
                "nilaiInd": item_dict['nilaiInd'],
                "nilaiIng": item_dict['nilaiIng'],
                "hasilRasionalisasi": hasil_prediksi
            }

            hasil_rasionalisasi['hasil'].append(result)
            save_result_to_json(hasil_rasionalisasi, "hasil_rasionalisasi.json")
            return hasil_prediksi
        
    raise HTTPException(
        status_code=404, detail=f'User belum terdaftar ke dalam program rasionalisasi SNMPTN.'
    )

@app.delete('/user/{user_id}')
async def delete_user(user_id: int):
	item_found = False
	for user_idx, user_item in enumerate(user_rasionalisasi['user']):
		if user_item['idUser'] == user_id:
			item_found = True
			user_rasionalisasi['user'].pop(user_idx)
			
			save_result_to_json(user_rasionalisasi, "user_rasionalisasi.json")
			return "User updated!"
	if not item_found:
		return "User ID not found."
	raise HTTPException(
		status_code=404, detail=f'User not found'
	)
