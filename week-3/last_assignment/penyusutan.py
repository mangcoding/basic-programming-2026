harga_awal = 12000000
nilai_sisa = 2000000
umur_eco = 4

susut_per_tahun = (harga_awal - nilai_sisa) / umur_eco
susut_2_tahun = susut_per_tahun*2
nilai_sisa_2tahun = harga_awal - susut_2_tahun

print("Penyusutan per tahun",susut_per_tahun)
print("Nilai laptop setelah dipakai 2 tahun",nilai_sisa_2tahun)
