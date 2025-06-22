import re
import json
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Load slang dictionary (ambil dict dari list)
with open("utils/slang_dict_combined.json", "r") as f:
    data = json.load(f)
    if isinstance(data, list) and len(data) > 0:
        slang_dict = data[0]
    else:
        slang_dict = {}

# Inisialisasi stemmer dan stopword dari Sastrawi
stemmer = StemmerFactory().create_stemmer()
default_stopwords = set(StopWordRemoverFactory().get_stop_words())

def cleaning_text(text):
    text = str(text).lower()
    # Hilangkan URL
    text = re.sub(r'https?://\S*|www\.\S+', '', text)
    # Hilangkan teks dalam kurung
    text = re.sub(r'\[.*?\]|\(.*?\)', '', text)
    # Hilangkan format tanggal & waktu
    text = re.sub(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', '', text)
    text = re.sub(r'\d{1,2}\s\w{3,}\s\d{4}', '', text)
    # Hilangkan satuan waktu
    text = re.sub(r'\b(menit|mnt|thn|tahun|minggu|mg|hari|hr|jam|jm|detik|dtk|sekon)\b', '', text)
    # Ganti satuan data dengan token
    text = re.sub(r'\d+\s*(gb|kb|mb|tb|g)\b', '<DATA_SIZE>', text)
    text = re.sub(r'\d+(gb|kb|mb|tb|g)\b', '<DATA_SIZE>', text)
    # Hilangkan bentuk pecahan atau slash
    text = re.sub(r'\w*\.*\w{1,}\.*\/\w{1,}', '', text)
    # Ganti jumlah tarif dengan token
    text = re.sub(r'rp\s*\d{1,}\s', '<PRICE>', text)
    # Ganti kode aktivasi
    text = re.sub(r'\*\d{2,}(\*\d{2,})?#', '<ACTIVATION_CODE>', text)
    # Hilangkan angka
    text = re.sub(r'\d+', '', text)
    # Ganti satuan uang dengan token
    text = re.sub(r'\b(ribu|rb|rp|jt|juta|milyar|miliar|triliun|trilyun)\b', '<MONEY_UNIT>', text)
    # Hilangkan tanda baca
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def normalize_text(text):
    words = text.split()
    return ' '.join([slang_dict.get(word, word) for word in words])

def remove_stopwords(text):
    return ' '.join([word for word in text.split() if word not in default_stopwords])

def stem_text(text):
    return stemmer.stem(text)

def preprocess_pipeline(text):
    text = cleaning_text(text)
    text = normalize_text(text)
    text = remove_stopwords(text)
    text = stem_text(text)
    return text
