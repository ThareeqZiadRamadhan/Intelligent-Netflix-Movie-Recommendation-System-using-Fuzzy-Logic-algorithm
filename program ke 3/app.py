import pandas as pd
import numpy as np
import skfuzzy as fuzz
from fuzzywuzzy import process
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Memuat dataset
data_cleaned = pd.read_csv('data-cleaned.csv')
top_movies = pd.read_csv('top-movies.csv')

# Mengambil kolom yang relevan dari kedua dataset
top_movies = top_movies[['title', 'genres', 'imdbAverageRating']]
data_cleaned = data_cleaned[['title', 'genres', 'imdbAverageRating']]

# Membuat variabel fuzzy untuk rating dan genre dengan skala 0-1
rating = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'rating')  # Skala rating 0-1
genre_similarity = ctrl.Antecedent(np.arange(0, 1.1, 0.1), 'genre_similarity')  # Similaritas genre 0-1
recommendation_score = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'recommendation_score')  # Skor rekomendasi 0-1

# Fuzzyfication - Keanggotaan fuzzy untuk rating
rating['low'] = fuzz.trimf(rating.universe, [0, 0, 0.3])
rating['medium'] = fuzz.trimf(rating.universe, [0, 0.5, 0.7])  # Perbaiki 0,7 menjadi 0.7
rating['high'] = fuzz.trimf(rating.universe, [0.7, 1, 1])

# Fuzzyfication - Keanggotaan fuzzy untuk genre similarity
genre_similarity['low'] = fuzz.trimf(genre_similarity.universe, [0, 0, 0.4])  # Low
genre_similarity['medium'] = fuzz.trimf(genre_similarity.universe, [0, 0.5, 0.7])  # Medium
genre_similarity['high'] = fuzz.trimf(genre_similarity.universe, [0.6, 1, 1])  # High

# Fuzzyfication - Keanggotaan fuzzy untuk recommendation_score
recommendation_score['low'] = fuzz.trimf(recommendation_score.universe, [0, 0, 0.4])  # Low
recommendation_score['medium'] = fuzz.trimf(recommendation_score.universe, [0, 0.5, 0.7])  # Medium
recommendation_score['high'] = fuzz.trimf(recommendation_score.universe, [0.6, 1, 1])  # High

# Definisi aturan fuzzy
rule1 = ctrl.Rule(rating['low'] & genre_similarity['low'], recommendation_score['low'])  # Rating rendah, genre rendah -> Skor rendah
rule2 = ctrl.Rule(rating['low'] & genre_similarity['medium'], recommendation_score['medium'])  # Rating rendah, genre medium -> Skor medium
rule3 = ctrl.Rule(rating['low'] & genre_similarity['high'], recommendation_score['medium'])  # Rating rendah, genre tinggi -> Skor medium
rule4 = ctrl.Rule(rating['medium'] & genre_similarity['low'], recommendation_score['medium'])  # Rating medium, genre rendah -> Skor medium
rule5 = ctrl.Rule(rating['medium'] & genre_similarity['medium'], recommendation_score['high'])  # Rating medium, genre medium -> Skor tinggi
rule6 = ctrl.Rule(rating['medium'] & genre_similarity['high'], recommendation_score['high'])  # Rating medium, genre tinggi -> Skor tinggi
rule7 = ctrl.Rule(rating['high'] & genre_similarity['low'], recommendation_score['medium'])  # Rating tinggi, genre rendah -> Skor medium
rule8 = ctrl.Rule(rating['high'] & genre_similarity['medium'], recommendation_score['high'])  # Rating tinggi, genre medium -> Skor tinggi
rule9 = ctrl.Rule(rating['high'] & genre_similarity['high'], recommendation_score['high'])  # Rating tinggi, genre tinggi -> Skor tinggi

# Membuat sistem kontrol
recommendation_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
recommendation = ctrl.ControlSystemSimulation(recommendation_ctrl)

def get_movie_recommendations_with_fuzzy(input_title, dataset, rating_value, genre_value, top_n=10):
    # Ambil semua film yang mirip judulnya
    choices = dataset['title'].tolist()
    recommendations = process.extract(input_title, choices, limit=30)  # ambil lebih banyak
    recommended_titles = [rec[0] for rec in recommendations]
    recommended_movies = dataset[dataset['title'].isin(recommended_titles)]

    # Proses fuzzy recommendation
    results = []
    for _, row in recommended_movies.iterrows():
        # Normalisasi rating IMDB ke 0–1
        normalized_rating = row['imdbAverageRating'] / 10.0
        # Genre similarity dummy sementara
        genre_sim = genre_value

        recommendation.input['rating'] = normalized_rating
        recommendation.input['genre_similarity'] = genre_sim
        recommendation.compute()
        results.append((row['title'], recommendation.output['recommendation_score']))

    # Urutkan berdasarkan skor rekomendasi
    sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
    return sorted_results[:top_n]

# Fungsi GUI dengan Tkinter
def show_recommendations():
    input_movie = movie_input.get()
    rating_value = rating_slider.get()  # Ambil nilai dari slider rating
    genre_value = genre_slider.get()  # Ambil nilai dari slider genre similarity
    
    if input_movie:
        # Mendapatkan rekomendasi film berdasarkan nilai slider
        recommended_movies = get_movie_recommendations_with_fuzzy(input_movie, top_movies, rating_value, genre_value, top_n=10)
        
        # Menampilkan rekomendasi
        result_text = f"Rekomendasi untuk '{input_movie}':\n"
        for movie in recommended_movies:
            score = movie[1]
            if score >= 0.8:
                recommendation = f"Film: {movie[0]}, Skor Rekomendasi: {score} - Sangat Direkomendasikan"
            elif score >= 0.7:
                recommendation = f"Film: {movie[0]}, Skor Rekomendasi: {score} - Direkomendasikan"
            else:
                recommendation = f"Film: {movie[0]}, Skor Rekomendasi: {score} - Kurang Direkomendasikan"
            result_text += recommendation + "\n"
        
        # Menampilkan hasil di label
        result_label.config(text=result_text)
    else:
        messagebox.showwarning("Peringatan", "Harap masukkan judul film!")

# Membuat GUI dengan Tkinter
root = tk.Tk()
root.title("Rekomendasi Film Netflix")

# Menambahkan warna latar belakang yang lebih modern dan font yang bersih
root.config(bg="#f4f4f9")  # Background warna terang dan modern
root.geometry("600x550")  # Menentukan ukuran jendela

# Menambahkan elemen desain yang bersih dan modern menggunakan ttk
style = ttk.Style()
style.configure("TButton", font=("Times New Roman", 12, "bold"), background="#E50914", padding=15)
style.configure("TLabel", font=("Times New Roman", 12), padding=5, background="#f4f4f9", foreground="black")

# Label untuk memasukkan judul film
tk.Label(root, text="Masukkan Judul Film yang Anda Cari:", font=("Times New Roman", 14), bg="#f4f4f9", fg="black").pack(pady=20)

# Input untuk memasukkan judul film
movie_input = tk.Entry(root, font=("Times New Roman", 12), width=40, bd=2, relief="solid")
movie_input.pack(pady=10)

# Slider untuk rating
rating_slider = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1, label="Rating Film (0-1)", length=400)
rating_slider.pack(pady=20)

# Slider untuk genre similarity
genre_slider = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1, label="Genre Similarity (0-1)", length=400)
genre_slider.pack(pady=20)

# Tombol untuk mendapatkan rekomendasi
ttk.Button(root, text="Dapatkan Rekomendasi", command=show_recommendations).pack(pady=20)

# Label untuk menampilkan hasil rekomendasi
result_label = tk.Label(root, text="", font=("Times New Roman", 12), justify=tk.LEFT, bg="#f4f4f7", fg="black", anchor="w")
result_label.pack(pady=10)

# Menjalankan aplikasi GUI
root.mainloop()
