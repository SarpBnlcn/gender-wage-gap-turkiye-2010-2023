
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import os

df_raw = pd.read_csv('data.csv', delimiter=';', header=None)

# Analize odaklanmak için 'Toplam' ve 'Temel meslekler' satırlarını çıkartır.
df_raw = df_raw[~df_raw['Occupation_TR'].isin(['Toplam', 'Temel meslekler'])]

# Veri yapısına göre Cinsiyet sütununu ekle.
df_raw['Gender'] = ['General'] * 9 + ['Male'] * 9 + ['Female'] * 9

# DataFrame'i uzun formata dönüştürür (yılları tek bir sütun haline getirir).
df_melted = df_raw.melt(id_vars=['Occupation_TR', 'Occupation_EN', 'Gender'],
                        var_name='year',
                        value_name='Hourly_Gross_Wage')

# 'year' sütununu sayısal türe dönüştürür.
df_melted['year'] = pd.to_numeric(df_melted['year'])

# Tutarlılık için İngilizce meslek isimlerini kullan ve orijinal dil sütunlarını çıkarır.
df_melted['Occupation'] = df_melted['Occupation_EN']
df_melted.drop(columns=['Occupation_TR', 'Occupation_EN'], inplace=True)

# 'Hourly_Gross_Wage' sütunundaki boş veya '(0)' değerlerini 0 ile doldur ve sayısal türe dönüştürür.
df_melted['Hourly_Gross_Wage'] = df_melted['Hourly_Gross_Wage'].fillna(0)

# Sadece Erkek ve Kadın verilerini içeren bir DataFrame oluşturur (Genel toplamları hariç).
df_gender_specific = df_melted[df_melted['Gender'].isin(['Male', 'Female'])].copy()

# Grafikleri kaydetmek için 'visualizations' dizinini oluştur (varsa atla).
output_dir = 'visualizations'
os.makedirs(output_dir, exist_ok=True)

# Keşifçi Veri Analizi (EDA) ve Görselleştirmeler ---

# Cinsiyetler arası ücret farkını hesaplamak için pivot tablo oluşturur.
df_pivot_wages = df_gender_specific.pivot_table(
    index=['Occupation', 'year'],
    columns='Gender',
    values='Hourly_Gross_Wage'
).reset_index()
df_pivot_wages.columns.name = None

# Ücret farkını hesapla: Erkek Ücreti - Kadın Ücreti.
df_pivot_wages['Wage_Gap'] = df_pivot_wages['Male'] - df_pivot_wages['Female']

# Yıllara Göre Ortalama Saatlik Brüt Ücretler (Cinsiyete Göre).
plt.figure(figsize=(12, 6))
sns.lineplot(data=df_gender_specific, x='year', y='Hourly_Gross_Wage', hue='Gender', marker='o')
plt.title('Yıllara Göre Ortalama Saatlik Brüt Ücretler (Cinsiyete Göre)', fontsize=16)
plt.xlabel('Yıl', fontsize=12)
plt.ylabel('Ortalama Saatlik Brüt Ücret (TL)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Cinsiyet')
plt.xticks(df_gender_specific['year'].unique())
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'ortalama_ucretler_yillara_gore.png'))
plt.show()

# Meslek Gruplarına Göre Ortalama Ücret Farkları (Tüm Yıllar Ortalaması).
avg_wage_gap_by_occupation = df_pivot_wages.groupby('Occupation')['Wage_Gap'].mean().sort_values(ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(x=avg_wage_gap_by_occupation.values, y=avg_wage_gap_by_occupation.index, hue=avg_wage_gap_by_occupation.index, palette='viridis', legend=False)
plt.title('Meslek Gruplarına Göre Ortalama Saatlik Ücret Farkları (Erkek - Kadın)', fontsize=16)
plt.xlabel('Ortalama Ücret Farkı (TL)', fontsize=12)
plt.ylabel('Meslek Grubu', fontsize=12)
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'meslek_bazli_ucret_farklari.png'))
plt.show()

# En Yüksek Ücret Farkının Gözlemlendiği Yıl ve Meslek Grubunu Belirler.
max_wage_gap_row = df_pivot_wages.loc[df_pivot_wages['Wage_Gap'].idxmax()]

print(f"\n--- Gözlemlenen En Yüksek Ücret Farkı ---")
print(f"Meslek Grubu: {max_wage_gap_row['Occupation']}")
print(f"Yıl: {int(max_wage_gap_row['year'])}")
print(f"Erkek Ücreti: {max_wage_gap_row['Male']:.2f} TL")
print(f"Kadın Ücreti: {max_wage_gap_row['Female']:.2f} TL")
print(f"Ücret Farkı: {max_wage_gap_row['Wage_Gap']:.2f} TL")

# Belirli Meslek Gruplarında Cinsiyet Bazlı Ücret Eğilimleri.
selected_occupations = ['Managers', 'Clerical support workers', 'Professionals']
df_selected_occupations = df_gender_specific[df_gender_specific['Occupation'].isin(selected_occupations)]

plt.figure(figsize=(14, 8))
sns.lineplot(data=df_selected_occupations, x='year', y='Hourly_Gross_Wage', hue='Gender', style='Occupation', marker='o', hue_order=['Male', 'Female'])
plt.title('Seçili Meslek Gruplarında Yıllara Göre Cinsiyet Bazlı Ücret Eğilimleri', fontsize=16)
plt.xlabel('Yıl', fontsize=12)
plt.ylabel('Saatlik Brüt Ücret (TL)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Cinsiyet / Meslek', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(df_selected_occupations['year'].unique())
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'secili_meslekler_ucret_egilimleri.png'))
plt.show()

# Makine Öğrenimi Modeli (RandomForestRegressor) ---
df_ml = df_gender_specific.copy()
y_ml = df_ml['Hourly_Gross_Wage']
X_ml = pd.get_dummies(df_ml[['year', 'Occupation', 'Gender']], columns=['Occupation', 'Gender'], drop_first=True)

X_train, X_test, y_train, y_test = train_test_split(X_ml, y_ml, test_size=0.2, random_state=42)

print("\n--- Model Eğitim Detayları ---")
print(f"Eğitim seti boyutu (X_train): {X_train.shape}")
print(f"Test seti boyutu (X_test): {X_test.shape}")

model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

print("\nModel başarıyla eğitildi.")

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\n--- Model Performansı ---")
print(f"Ortalama Mutlak Hata (MAE): {mae:.3f}")
print(f"R-kare (R²): {r2:.3f}")
