from fpdf import FPDF
import matplotlib.pyplot as plt
import pandas as pd
import random
import os
import tempfile
from PIL import ImageFont

# Menggunakan path lengkap ke Arial
font_path = "C:\\Windows\\Fonts\\arial.ttf"
font = ImageFont.truetype(font_path, size=12)

class CustomPDF(FPDF):
    def header(self):
        if self.page_no() > 1:  
            self.set_font('Arial', 'B', 12) 
            self.cell(0, 10, f'Mock User Manual - Halaman {self.page_no()}', align='C', ln=True)
            self.ln(5)

    def footer(self):
        if self.page_no() > 1:  
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, f'Halaman {self.page_no()}', align='C')

    def __init__(self):
        super().__init__()
        # Menggunakan path lengkap untuk font Arial
        self.add_font('Arial', '', "C:\\Windows\\Fonts\\arial.ttf", uni=True)  
        self.set_font('Arial', '', 11)
        self.toc_entries = []
    
    def add_text_section(self, title, content, align="L"):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, title, ln=True, align=align)
        self.ln(5)
        self.set_font('Arial', '', 11)  # Pastikan font mendukung Unicode
        self.multi_cell(0, 10, content)
        self.ln(10)
        self.toc_entries.append((title, self.page_no()))

    def add_image(self, img_path, x=None, y=None, w=150, h=0):
        self.image(img_path, x=x, y=y, w=w, h=h)
        self.ln(10)

    def add_graph(self, graph_title, data):
        plt.figure(figsize=(6, 4))
        plt.bar(data.keys(), data.values(), color='skyblue')
        plt.title(graph_title)
        plt.xlabel('Kategori')
        plt.ylabel('Nilai')
        plt.tight_layout()

        # Simpan ke file sementara
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            tmpfile_path = tmpfile.name
        plt.savefig(tmpfile_path)
        plt.close()

        self.add_image(tmpfile_path, x=30, y=None, w=100)
        os.remove(tmpfile_path)  # Hapus setelah digunakan

    def add_workflow_diagram(self, workflow_steps):
        plt.figure(figsize=(6, 4))
        plt.plot(workflow_steps, marker='o', linestyle='-', color='green')
        plt.title('Diagram Alur Proses')
        plt.xlabel('Langkah')
        plt.ylabel('Progress')
        plt.grid(True)
        plt.xticks(range(len(workflow_steps)), workflow_steps, rotation=0)
        plt.yticks(range(len(workflow_steps)), workflow_steps)
        plt.tight_layout()

        # Simpan ke file sementara
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmpfile:
            tmpfile_path = tmpfile.name
        plt.savefig(tmpfile_path, bbox_inches='tight')
        plt.close()

        self.add_image(tmpfile_path, x=30, y=None, w=100)
        os.remove(tmpfile_path)  # Hapus setelah digunakan

    def add_csv_table(self, csv_path, limit=10):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Tabel Produk Robot Pembersih Lantai", ln=True, align="C")
        self.ln(5)

        df = pd.read_csv(csv_path)
        df = df.head(limit)
        selected_columns = ["product_id", "product_name", "price", "stock_availability"]

        self.set_font("Arial", "B", 10)
        for col in selected_columns:
            self.cell(40, 10, col, border=1)
        self.ln()

        self.set_font("Arial", "", 10)
        for _, row in df.iterrows():
            for col in selected_columns:
                value = str(row[col])[:20]
                self.cell(40, 10, value, border=1)
            self.ln()

        self.ln(10)
        

# **Fungsi untuk menghasilkan data unik per halaman**
EXAMPLES = [
    ("Pembersihan Otomatis", "Dapat digunakan untuk membersihkan lantai tanpa perlu intervensi pengguna.", "Menghemat waktu dan tenaga dalam membersihkan lantai."),
    ("Navigasi Cerdas", "Dapat mendeteksi dan menghindari rintangan di ruangan.", "Mengurangi kemungkinan benturan dan kerusakan perangkat."),
    ("Mode Pembersihan Fleksibel", "Mendukung beberapa mode pembersihan seperti menyapu, mengepel, atau keduanya.", "Memungkinkan pengguna menyesuaikan metode pembersihan sesuai kebutuhan."),
    ("Kontrol Aplikasi", "Dapat diatur melalui aplikasi seluler.", "Memudahkan pengguna dalam mengontrol robot dari jarak jauh."),
    ("Sensor Debu", "Mendeteksi area yang lebih kotor dan meningkatkan daya hisap otomatis.", "Meningkatkan efisiensi pembersihan tanpa intervensi manual.")
]

def generate_unique_data(page_number):
    feature_index = (page_number - 5) % len(EXAMPLES)
    title, example, benefit = EXAMPLES[feature_index]

    text_title = f"Bagian {page_number}: {title}"
    text_content = (
        f"{example}\n\n"
        f"Manfaat utama: {benefit}"
    )

    graph_data = {f"Kategori {i}": random.randint(50, 100) for i in range(1, 6)}
    workflow_steps = [f"Langkah {i}" for i in range(1, random.randint(3, 7))]

    return text_title, text_content, graph_data, workflow_steps
# **Fungsi untuk membuat PDF**
def create_mock_user_manual():
    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    table_of_contents = []  # Menyimpan daftar isi
    csv_path = "dini_anggriyani_synthetic_data.csv"

    # Cover Page
    pdf.add_page()
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 10, "Mock User Manual", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("Arial", "", 14)
    pdf.cell(0, 10, "Produk Robot Pembersih Lantai", ln=True, align="C")
    pdf.ln(20)
    pdf.add_image("image.png", x=40, y=None, w=120)

    # Kata Sambutan
    pdf.add_page()
    kata_sambutan = ("Halo dan selamat datang!"
        "Terima kasih telah memilih Robot Pembersih Lantai sebagai solusi kebersihan rumah Anda. "
        "Kami sangat menghargai kepercayaan Anda dalam menggunakan produk inovatif ini.\n\n"
        "Di era modern ini, efisiensi dan kenyamanan menjadi prioritas utama. Oleh karena itu, robot ini "
        "dirancang untuk membantu Anda dalam menjaga kebersihan rumah tanpa harus repot. Dengan teknologi canggih, "
        "robot ini mampu membersihkan lantai secara otomatis, mendeteksi hambatan, dan menyesuaikan pola pembersihan "
        "sesuai dengan kebutuhan ruangan Anda."
        "Buku petunjuk ini akan membantu Anda memahami cara kerja, fitur, serta cara perawatan robot agar dapat "
        "digunakan secara optimal. Kami menyarankan Anda untuk membaca setiap bagian dengan cermat sebelum mulai "
        "mengoperasikan perangkat ini.\n\n"
        "Jika ada pertanyaan atau kendala dalam penggunaan, silakan hubungi tim dukungan pelanggan kami melalui kontak "
        "yang tersedia di bagian akhir buku ini. Kami siap membantu Anda kapan saja.\n\n"
        "Selamat menikmati pengalaman membersihkan rumah dengan cara yang lebih mudah dan efisien!"
    )
    
    # Pastikan teks tercetak dengan jarak yang cukup
    pdf.add_text_section("Kata Sambutan", kata_sambutan)

    # Tambahkan jarak setelah kata sambutan
    pdf.ln(10)  # Memberikan jarak tambahan setelah kata sambutan


    # Pendahuluan
    pdf.add_page()
    pendahuluan = (
        "Mengenal Robot Pembersih Lantai\n\n"
        "Robot Pembersih Lantai ini adalah perangkat pintar yang dirancang untuk membersihkan rumah secara otomatis. "
        "Dengan menggunakan teknologi sensor yang canggih, robot ini mampu mendeteksi kotoran, menghindari rintangan, "
        "dan menyesuaikan pola pembersihan sesuai dengan tata letak ruangan Anda.\n\n"
        "Fitur utama robot ini meliputi:\n"
        "- Navigasi Cerdas → Menggunakan sensor untuk menghindari tabrakan dan jatuh dari tangga.\n"
        "- Mode Pembersihan Beragam → Bisa digunakan untuk menyapu, mengepel, atau kombinasi keduanya.\n"
        "- Daya Hisap Kuat → Mampu menangkap debu, rambut, dan partikel kecil lainnya dengan efisien.\n"
        "- Baterai Tahan Lama → Dapat beroperasi hingga 120 menit sebelum kembali ke dock pengisian daya otomatis.\n"
        "- Kontrol Pintar → Bisa dikendalikan melalui aplikasi di smartphone untuk menjadwalkan pembersihan.\n\n"
        "Kenapa Anda Membutuhkan Robot Ini?\n\n"
        "Dengan semakin sibuknya kehidupan sehari-hari, banyak orang kesulitan menemukan waktu untuk membersihkan rumah "
        "secara manual. Robot ini hadir sebagai solusi untuk membantu Anda menjaga kebersihan rumah tanpa harus "
        "menghabiskan banyak waktu dan tenaga.\n\n"
        "Pada bagian selanjutnya, kita akan membahas fitur-fitur yang lebih spesifik serta bagaimana cara menggunakannya "
        "dengan maksimal."
    )
    pdf.add_text_section("Pendahuluan", pendahuluan.replace("→", "->"))  # Ganti karakter Unicode

    # Halaman Fitur Produk
    for i in range(5, 50):
        pdf.add_page()
        title, content, graph_data, workflow_steps = generate_unique_data(i)
        pdf.add_text_section(title, content)
        pdf.add_graph(f"Grafik Fitur Halaman {i}", graph_data)
        pdf.add_workflow_diagram(workflow_steps)

    # Halaman Akhir
    pdf.add_page()
    penutup = ("Terima Kasih & Harapan Kami\n\n"
    "Terima kasih telah memilih Robot Pembersih Lantai sebagai solusi kebersihan rumah Anda. "
    "Kami sangat menghargai kepercayaan yang Anda berikan kepada produk kami. Semoga perangkat ini "
    "dapat membantu meringankan pekerjaan rumah tangga Anda dan memberikan kenyamanan lebih dalam kehidupan sehari-hari.\n\n"
    "Dengan teknologi canggih yang terus berkembang, kami berkomitmen untuk memberikan produk terbaik yang tidak hanya efisien "
    "tetapi juga mudah digunakan. Kami memahami bahwa setiap rumah memiliki kebutuhan yang berbeda, dan oleh karena itu, "
    "kami terus berinovasi untuk menghadirkan fitur-fitur yang dapat menyesuaikan dengan kebutuhan pengguna.\n\n"
    
    "Dukungan & Layanan Pelanggan\n\n"
    "Jika Anda memiliki pertanyaan, kendala teknis, atau membutuhkan bantuan lebih lanjut, tim layanan pelanggan kami siap membantu. "
    "Jangan ragu untuk menghubungi kami melalui:\n"
    "- 📧 Email: support@robotcleaning.com\n"
    "- ☎️ Telepon: 0800-123-4567 (Senin - Jumat, 09.00 - 18.00)\n"
    "- 🌐 Website: www.robotcleaning.com\n\n"
    
    "Selain itu, kami juga memiliki komunitas pengguna di media sosial yang bisa Anda ikuti untuk mendapatkan tips & trik, "
    "pembaruan produk, serta informasi promo terbaru.\n\n"
    
    "Garansi & Pemeliharaan\n\n"
    "Untuk memastikan robot pembersih lantai Anda selalu bekerja dengan optimal, kami menyarankan untuk:\n"
    "- Membersihkan filter dan sikat secara berkala agar performa tetap maksimal.\n"
    "- Menyimpan robot di tempat kering dan aman untuk menghindari kerusakan akibat kelembaban.\n"
    "- Memeriksa pembaruan perangkat lunak secara rutin melalui aplikasi pendukung.\n"
    "- Menggunakan suku cadang resmi jika ada komponen yang perlu diganti.\n\n"
    
    "Kata Terakhir\n\n"
    "Kami berharap robot pembersih ini dapat menjadi bagian dari gaya hidup pintar Anda. Dengan penggunaan yang tepat, "
    "robot ini dapat membantu menciptakan lingkungan yang lebih bersih dan sehat, serta memberikan Anda lebih banyak waktu "
    "untuk melakukan hal-hal yang Anda sukai.\n\n"
    "Selamat menikmati pengalaman membersihkan rumah yang lebih mudah dan efisien!\n\n"
    "Salam hangat,\n"
    "Tim Robot Cleaning Solutions"
)
    pdf.set_auto_page_break(auto=True, margin=15)
    # Menambahkan Kata Penutup di halaman baru
    pdf.add_text_section("Kata Penutup", penutup)

    # Memberikan jarak setelah kata penutup
    pdf.ln(10)  # Menambahkan jarak setelah kata penutup

    pdf.output("dini_anggriyani_synthetic_data.pdf")
    print("✅ PDF berhasil dibuat!")

# **Jalankan**
create_mock_user_manual()
