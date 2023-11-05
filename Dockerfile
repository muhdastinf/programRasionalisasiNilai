FROM python:3

ADD rasionalisasiNilaiSNM.py .

COPY . /rasionalisasiNilaiSNMFix
WORKDIR /rasionalisasiNilaiSNMFix
RUN pip install fastapi uvicorn pandas scikit-learn
CMD ["uvicorn", "rasionalisasiNilaiSNM:app", "--host=0.0.0.0", "--port=80"]