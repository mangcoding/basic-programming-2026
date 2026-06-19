"""
Infografis distribusi nilai quiz berdasarkan grup skor.
Membaca data dari score-quiz.xlsx dan menampilkan visualisasi dengan matplotlib.
"""

import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Konfigurasi grup nilai: (label, batas_bawah, batas_atas)
# batas_bawah inklusif, batas_atas inklusif
GRUP_NILAI = [
    ("0 - 50", 0, 50),
    ("50 - 70", 50, 70),
    ("70 - 80", 70, 80),
    ("80 - 90", 80, 90),
    ("> 90", 90, 100),
]

WARNA = ["#E74C3C", "#F39C12", "#3498DB", "#2ECC71", "#9B59B6"]


def parse_skor(nilai):
    """Ambil angka skor dari kolom 'Total Skor (norm.)', contoh: '95.3 (90%)'."""
    if pd.isna(nilai):
        return None
    cocok = re.match(r"^([\d.]+)", str(nilai).strip())
    return float(cocok.group(1)) if cocok else None


def kelompokkan_skor(skor):
    """Masukkan skor ke grup yang sesuai."""
    if skor <= 50:
        return "0 - 50"
    if skor <= 70:
        return "50 - 70"
    if skor < 80:
        return "70 - 80"
    if skor <= 90:
        return "80 - 90"
    return "> 90"


def hitung_per_grup(skor_list):
    """Hitung jumlah peserta per grup nilai."""
    label_grup = [g[0] for g in GRUP_NILAI]
    jumlah = {label: 0 for label in label_grup}

    for skor in skor_list:
        grup = kelompokkan_skor(skor)
        if grup:
            jumlah[grup] += 1

    return label_grup, [jumlah[label] for label in label_grup]


def buat_infografis(label_grup, jumlah, skor_list, total_peserta, simpan_ke):
    """Buat dan simpan infografis matplotlib."""
    fig = plt.figure(figsize=(14, 8))
    fig.patch.set_facecolor("#F8F9FA")

    # Judul utama
    fig.suptitle(
        "Infografis Nilai Quiz\nDasar Pemrograman",
        fontsize=20,
        fontweight="bold",
        color="#2C3E50",
        y=0.98,
    )

    # Subplot kiri: diagram batang
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_facecolor("#FFFFFF")
    bars = ax1.bar(
        label_grup,
        jumlah,
        color=WARNA,
        edgecolor="white",
        linewidth=1.5,
        width=0.65,
    )

    for bar, count in zip(bars, jumlah):
        if count > 0:
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.15,
                str(count),
                ha="center",
                va="bottom",
                fontsize=13,
                fontweight="bold",
                color="#2C3E50",
            )

    ax1.set_title("Jumlah Peserta per Grup Nilai", fontsize=14, fontweight="bold", pad=12)
    ax1.set_xlabel("Grup Nilai", fontsize=11)
    ax1.set_ylabel("Jumlah Peserta", fontsize=11)
    ax1.set_ylim(0, max(jumlah) + 2 if jumlah else 1)
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    ax1.grid(axis="y", linestyle="--", alpha=0.4)

    # Subplot kanan: diagram pie
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.set_facecolor("#FFFFFF")

    data_pie = [(label, count) for label, count in zip(label_grup, jumlah) if count > 0]
    if data_pie:
        labels_pie, sizes_pie = zip(*data_pie)
        colors_pie = [WARNA[label_grup.index(l)] for l in labels_pie]
        wedges, texts, autotexts = ax2.pie(
            sizes_pie,
            labels=labels_pie,
            autopct=lambda p: f"{p:.1f}%" if p > 0 else "",
            startangle=90,
            colors=colors_pie,
            explode=[0.03] * len(sizes_pie),
            textprops={"fontsize": 10},
            wedgeprops={"edgecolor": "white", "linewidth": 2},
        )
        for autotext in autotexts:
            autotext.set_fontweight("bold")
            autotext.set_color("white")

    ax2.set_title("Persentase per Grup Nilai", fontsize=14, fontweight="bold", pad=12)

    # Ringkasan statistik di bawah
    rata_rata = sum(skor_list) / len(skor_list) if skor_list else 0
    tertinggi = max(skor_list) if skor_list else 0
    terendah = min(skor_list) if skor_list else 0

    info_text = (
        f"Total Peserta: {total_peserta}  |  "
        f"Rata-rata: {rata_rata:.1f}  |  "
        f"Tertinggi: {tertinggi:.1f}  |  "
        f"Terendah: {terendah:.1f}"
    )
    fig.text(0.5, 0.02, info_text, ha="center", fontsize=11, color="#555555")

    plt.tight_layout(rect=[0, 0.05, 1, 0.93])
    plt.savefig(simpan_ke, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Infografis disimpan ke: {simpan_ke}")
    plt.close(fig)


if __name__ == "__main__":
    folder = Path(__file__).parent
    file_excel = folder / "score-quiz.xlsx"
    file_output = folder / "infografis_quiz.png"

    df = pd.read_excel(file_excel)
    skor_data = df["Total Skor (norm.)"].apply(parse_skor).dropna().tolist()

    label_grup, jumlah = hitung_per_grup(skor_data)

    print("\n=== Distribusi Nilai Quiz ===")
    for label, count in zip(label_grup, jumlah):
        persen = (count / len(skor_data) * 100) if skor_data else 0
        print(f"  {label:>10}: {count:>2} peserta ({persen:.1f}%)")
    print(f"\nTotal: {len(skor_data)} peserta")

    buat_infografis(label_grup, jumlah, skor_data, len(skor_data), file_output)
