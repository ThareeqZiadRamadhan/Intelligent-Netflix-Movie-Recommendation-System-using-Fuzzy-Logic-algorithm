import numpy as np
import matplotlib.pyplot as plt

# Fungsi trimf manual (fungsi keanggotaan segitiga)
def trimf(x, abc):
    a, b, c = abc
    return np.maximum(0, np.minimum((x - a) / (b - a + 1e-6), np.minimum((c - x) / (c - b + 1e-6), 1)))

# Domain untuk semua variabel
x = np.linspace(0, 1, 100)

# Rating
rating_low = trimf(x, [0, 0, 0.3])
rating_medium = trimf(x, [0, 0.7, 1])
rating_high = trimf(x, [0.7, 1, 1])

# Genre Similarity
genre_low = trimf(x, [0, 0, 0.4])
genre_medium = trimf(x, [0, 0.5, 0.7])  # Perbaikan: gunakan titik, bukan koma
genre_high = trimf(x, [0.6, 1, 1])

# Recommendation Score
rec_low = trimf(x, [0, 0, 0.5])
rec_medium = trimf(x, [0, 0.5, 1])
rec_high = trimf(x, [0.5, 1, 1])

# Plotting
fig, axs = plt.subplots(nrows=3, figsize=(12, 9), constrained_layout=True)

# Rating
axs[0].plot(x, rating_low, label='Low')
axs[0].plot(x, rating_medium, label='Medium')
axs[0].plot(x, rating_high, label='High')
axs[0].set_title('Fungsi Keanggotaan: Rating')
axs[0].set_xlabel('Rating (0-1)')
axs[0].set_ylabel('Keanggotaan')
axs[0].legend(loc='upper right')

# Genre Similarity
axs[1].plot(x, genre_low, label='Low')
axs[1].plot(x, genre_medium, label='Medium')
axs[1].plot(x, genre_high, label='High')
axs[1].set_title('Fungsi Keanggotaan: Genre Similarity')
axs[1].set_xlabel('Genre Similarity (0-1)')
axs[1].set_ylabel('Keanggotaan')
axs[1].legend(loc='upper right')

# Recommendation Score
axs[2].plot(x, rec_low, label='Low')
axs[2].plot(x, rec_medium, label='Medium')
axs[2].plot(x, rec_high, label='High')
axs[2].set_title('Fungsi Keanggotaan: Recommendation Score')
axs[2].set_xlabel('Score (0-1)')
axs[2].set_ylabel('Keanggotaan')
axs[2].legend(loc='upper right')

# Simpan ke file
fig.savefig("fuzzy_diagram.png")

plt.close(fig)  # Menutup setelah disimpan agar tidak muncul saat run otomatis
print("Diagram berhasil disimpan sebagai 'fuzzy_diagram.png' di folder program.")
plt.show()
