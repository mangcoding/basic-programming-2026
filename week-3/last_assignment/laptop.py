harga_laptop = int(input("Masukkan harga laptop: "))
tabungan_per_bulan = int(input("Target tabungan per bulan: "))

total_bulan_yang_dibutuhkan = harga_laptop/tabungan_per_bulan
total_tahun = total_bulan_yang_dibutuhkan/12

print(f"Bulan yang dibutuhkan untuk membeli laptop seharga Rp {harga_laptop:,} dengan tabungan Rp{tabungan_per_bulan:,} adalah {total_bulan_yang_dibutuhkan} bulan atau {total_tahun:.2f} tahun")