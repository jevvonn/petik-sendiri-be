"""
Plant Seeder - Seeds plant data into the database
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.db.base import SessionLocal, engine
from app.models.plant import Plant


def seed_plants():
    """Create plant data if not exists."""
    db: Session = SessionLocal()
    
    try:
        # Check if plants already exist
        existing_plants = db.query(Plant).count()
        
        if existing_plants > 0:
            print(f"Plants already exist ({existing_plants} plants). Skipping...")
            return
        
        plants_data = [
            # ============ TANAMAN PANGAN ============
            {
                "name": "Kentang",
                "description": "Kentang adalah tanaman umbi yang kaya karbohidrat, cocok ditanam di dataran tinggi maupun rendah dengan media pot atau polybag.",
                "category": "Pangan",
                "difficulty_level": "Sedang",
                "duration_days": "90 - 120 Hari",
                "unit": "kg",
                "market_price_per_unit": 14542,
                "image_url": "/plants/kentang.jpg",
                "recommendations": [
                    {"title": "Pilih Bibit Berkualitas", "desc": "Gunakan umbi kentang yang sudah bertunas dengan mata tunas minimal 2-3 buah untuk hasil optimal."},
                    {"title": "Media Gembur", "desc": "Campurkan tanah, kompos, dan sekam dengan perbandingan 2:1:1 agar umbi berkembang maksimal."}
                ],
                "prohibitions": [
                    {"title": "Hindari Genangan Air", "desc": "Kentang sangat rentan terhadap busuk umbi jika media terlalu basah atau tergenang."},
                    {"title": "Jangan Terlalu Dalam", "desc": "Tanam umbi pada kedalaman 5-10 cm saja, terlalu dalam akan menghambat pertumbuhan."}
                ],
                "requirements": {
                    "min_temp": 15, "max_temp": 24,
                    "min_humidity": 60, "max_humidity": 80,
                    "sunlight": "sedang",
                    "water": "sedang",
                    "min_space_cm": 30,
                    "growing_days": 105
                },
                "growth_phases": [
                    {"phase": 1, "name": "Penanaman", "days": 14, "care": "Siram secukupnya 2 hari sekali", "indicators": "Tunas muncul dari media"},
                    {"phase": 2, "name": "Vegetatif", "days": 45, "care": "Tambahkan pupuk NPK, siram rutin", "indicators": "Daun tumbuh lebat, batang kokoh"},
                    {"phase": 3, "name": "Pembentukan Umbi", "days": 30, "care": "Kurangi frekuensi penyiraman", "indicators": "Daun mulai menguning"},
                    {"phase": 4, "name": "Panen", "days": 16, "care": "Hentikan penyiraman 1 minggu sebelum panen", "indicators": "Daun mengering, siap panen"}
                ],
                "common_diseases": [
                    {"name": "Busuk Daun (Late Blight)", "symptoms": "Bercak coklat pada daun, membusuk", "treatment": "Semprot fungisida berbahan tembaga, buang daun terinfeksi", "severity": "tinggi"},
                    {"name": "Kutu Daun", "symptoms": "Daun keriting, terlihat kutu kecil", "treatment": "Semprot pestisida organik atau larutan sabun", "severity": "sedang"}
                ]
            },
            {
                "name": "Bayam",
                "description": "Bayam adalah sayuran hijau yang cepat tumbuh, kaya zat besi dan vitamin, sangat cocok untuk pemula urban farming.",
                "category": "Pangan",
                "difficulty_level": "Mudah",
                "duration_days": "30 - 40 Hari",
                "unit": "ikat",
                "market_price_per_unit": 5042,
                "image_url": "/plants/bayam.jpg",
                "recommendations": [
                    {"title": "Panen Bertahap", "desc": "Petik daun luar yang sudah besar terlebih dahulu, biarkan yang dalam terus tumbuh untuk panen berkelanjutan."},
                    {"title": "Tanam Rapat", "desc": "Jarak tanam 10-15 cm sudah cukup karena bayam tidak memerlukan banyak ruang."}
                ],
                "prohibitions": [
                    {"title": "Hindari Sinar Langsung Berlebih", "desc": "Bayam lebih suka tempat teduh parsial, terlalu panas akan membuat daun keras dan pahit."},
                    {"title": "Jangan Kekurangan Air", "desc": "Bayam butuh media lembab konsisten, kekeringan membuat daun cepat layu."}
                ],
                "requirements": {
                    "min_temp": 20, "max_temp": 30,
                    "min_humidity": 65, "max_humidity": 85,
                    "sunlight": "sedang",
                    "water": "tinggi",
                    "min_space_cm": 15,
                    "growing_days": 35
                },
                "growth_phases": [
                    {"phase": 1, "name": "Perkecambahan", "days": 5, "care": "Jaga kelembaban media, semprot air 2x sehari", "indicators": "Biji berkecambah, muncul daun lembaga"},
                    {"phase": 2, "name": "Vegetatif", "days": 20, "care": "Berikan pupuk organik cair seminggu sekali", "indicators": "Daun tumbuh cepat, batang tegak"},
                    {"phase": 3, "name": "Siap Panen", "days": 10, "care": "Panen secara bertahap dari daun luar", "indicators": "Tinggi 20-25 cm, daun lebar dan hijau"}
                ],
                "common_diseases": [
                    {"name": "Bercak Daun", "symptoms": "Bintik coklat pada permukaan daun", "treatment": "Pangkas daun terinfeksi, semprotkan fungisida organik", "severity": "rendah"},
                    {"name": "Ulat Daun", "symptoms": "Daun berlubang, terlihat ulat hijau", "treatment": "Ambil ulat manual atau gunakan pestisida organik", "severity": "sedang"}
                ]
            },
            {
                "name": "Selada",
                "description": "Selada adalah sayuran daun renyah yang cocok untuk salad, mudah tumbuh di iklim tropis dengan perawatan yang tepat.",
                "category": "Pangan",
                "difficulty_level": "Mudah",
                "duration_days": "40 - 50 Hari",
                "unit": "ikat",
                "market_price_per_unit": 5000,
                "image_url": "/plants/selada.jpg",
                "recommendations": [
                    {"title": "Sistem Hidroponik", "desc": "Selada sangat cocok ditanam secara hidroponik untuk hasil yang lebih bersih dan cepat."},
                    {"title": "Panen Pagi Hari", "desc": "Panen selada di pagi hari untuk mendapatkan kesegaran dan kerenyahan maksimal."}
                ],
                "prohibitions": [
                    {"title": "Hindari Panas Terik", "desc": "Selada mudah layu dan pahit jika terkena sinar matahari langsung terlalu lama."},
                    {"title": "Jangan Overwatering", "desc": "Meski butuh air, selada rentan busuk akar jika media terlalu basah."}
                ],
                "requirements": {
                    "min_temp": 18, "max_temp": 28,
                    "min_humidity": 60, "max_humidity": 75,
                    "sunlight": "sedang",
                    "water": "sedang",
                    "min_space_cm": 20,
                    "growing_days": 45
                },
                "growth_phases": [
                    {"phase": 1, "name": "Semai", "days": 7, "care": "Tabur benih di media semai, jaga kelembaban", "indicators": "Benih berkecambah, daun kecil muncul"},
                    {"phase": 2, "name": "Pindah Tanam", "days": 7, "care": "Pindahkan bibit ke pot/bedengan lebih besar", "indicators": "Daun sejati 2-4 helai"},
                    {"phase": 3, "name": "Vegetatif", "days": 25, "care": "Berikan pupuk NPK dan organic setiap minggu", "indicators": "Daun tumbuh roset, membentuk kepala"},
                    {"phase": 4, "name": "Panen", "days": 6, "care": "Panen dengan memotong pangkal batang", "indicators": "Kepala padat, daun renyah"}
                ],
                "common_diseases": [
                    {"name": "Downy Mildew", "symptoms": "Bercak putih seperti tepung di daun", "treatment": "Hindari kelembaban berlebih, aplikasi fungisida", "severity": "sedang"},
                    {"name": "Aphids", "symptoms": "Kutu kecil hijau di daun muda", "treatment": "Semprot air bertekanan atau pestisida organik", "severity": "rendah"}
                ]
            },
            {
                "name": "Daun Bawang",
                "description": "Daun bawang adalah bumbu dapur yang mudah tumbuh, dapat dipanen berkali-kali dengan sistem cut and come again.",
                "category": "Pangan",
                "difficulty_level": "Mudah",
                "duration_days": "60 - 75 Hari",
                "unit": "ikat",
                "market_price_per_unit": 12000,
                "image_url": "/plants/daun-bawang.jpg",
                "recommendations": [
                    {"title": "Panen Bertahap", "desc": "Potong hanya bagian atas daun, sisakan 3-5 cm dari pangkal agar tumbuh kembali."},
                    {"title": "Tanam dari Sisa Akar", "desc": "Gunakan sisa akar daun bawang dari pasar, rendam dalam air hingga tumbuh lalu tanam."}
                ],
                "prohibitions": [
                    {"title": "Hindari Media Asam", "desc": "Daun bawang tidak suka tanah terlalu asam, tambahkan kapur dolomit jika perlu."},
                    {"title": "Jangan Tanam Terlalu Dalam", "desc": "Tanam hanya sedalam 2-3 cm untuk pertumbuhan optimal."}
                ],
                "requirements": {
                    "min_temp": 20, "max_temp": 30,
                    "min_humidity": 60, "max_humidity": 80,
                    "sunlight": "tinggi",
                    "water": "sedang",
                    "min_space_cm": 10,
                    "growing_days": 67
                },
                "growth_phases": [
                    {"phase": 1, "name": "Penanaman", "days": 10, "care": "Siram rutin pagi dan sore", "indicators": "Tunas hijau muncul dari umbi"},
                    {"phase": 2, "name": "Pertumbuhan Awal", "days": 25, "care": "Berikan pupuk nitrogen untuk pertumbuhan daun", "indicators": "Daun tumbuh memanjang, hijau segar"},
                    {"phase": 3, "name": "Panen Pertama", "days": 25, "care": "Potong daun yang sudah tinggi 25-30 cm", "indicators": "Daun panjang dan segar"},
                    {"phase": 4, "name": "Regenerasi", "days": 7, "care": "Berikan pupuk dan air rutin", "indicators": "Daun baru tumbuh dari pangkal"}
                ],
                "common_diseases": [
                    {"name": "Bercak Ungu", "symptoms": "Bercak ungu memanjang pada daun", "treatment": "Kurangi kelembaban, semprot fungisida", "severity": "sedang"},
                    {"name": "Trips", "symptoms": "Daun berwarna keperakan, ada serangga kecil", "treatment": "Gunakan insektisida atau perangkap kuning", "severity": "rendah"}
                ]
            },
            {
                "name": "Pakcoy",
                "description": "Pakcoy adalah sayuran hijau khas Asia yang kaya nutrisi, mudah tumbuh dan cocok untuk masakan tumis maupun sup.",
                "category": "Pangan",
                "difficulty_level": "Mudah",
                "duration_days": "35 - 45 Hari",
                "unit": "kg",
                "market_price_per_unit": 15000,
                "image_url": "/plants/pakcoy.jpg",
                "recommendations": [
                    {"title": "Tanam di Tempat Teduh", "desc": "Pakcoy lebih suka area yang teduh parsial, terutama di siang hari Jakarta yang panas."},
                    {"title": "Panen Tepat Waktu", "desc": "Jangan terlambat panen, pakcoy yang terlalu tua akan berbunga dan rasanya pahit."}
                ],
                "prohibitions": [
                    {"title": "Hindari Panas Berlebih", "desc": "Suhu terlalu tinggi membuat pakcoy cepat berbunga dan tidak produktif."},
                    {"title": "Jangan Biarkan Kering", "desc": "Pakcoy butuh air konsisten, kekeringan membuat daun keras dan pahit."}
                ],
                "requirements": {
                    "min_temp": 15, "max_temp": 25,
                    "min_humidity": 65, "max_humidity": 85,
                    "sunlight": "sedang",
                    "water": "tinggi",
                    "min_space_cm": 20,
                    "growing_days": 40
                },
                "growth_phases": [
                    {"phase": 1, "name": "Semai", "days": 7, "care": "Tabur benih, jaga media lembab", "indicators": "Biji berkecambah"},
                    {"phase": 2, "name": "Bibit", "days": 7, "care": "Pindah ke pot lebih besar", "indicators": "Daun sejati 2-4 helai"},
                    {"phase": 3, "name": "Vegetatif", "days": 21, "care": "Pupuk NPK seminggu sekali, siram rutin", "indicators": "Roset daun terbentuk"},
                    {"phase": 4, "name": "Panen", "days": 5, "care": "Cabut seluruh tanaman atau potong pangkal", "indicators": "Tinggi 15-20 cm, batang putih tebal"}
                ],
                "common_diseases": [
                    {"name": "Busuk Akar", "symptoms": "Tanaman layu, akar berwarna coklat", "treatment": "Perbaiki drainase, kurangi penyiraman", "severity": "tinggi"},
                    {"name": "Ulat Grayak", "symptoms": "Daun berlubang besar", "treatment": "Ambil ulat manual atau gunakan BT (Bacillus thuringiensis)", "severity": "sedang"}
                ]
            },
            {
                "name": "Kangkung",
                "description": "Kangkung adalah sayuran hijau yang sangat cepat tumbuh, mudah perawatan, dan bisa dipanen berkali-kali.",
                "category": "Pangan",
                "difficulty_level": "Mudah",
                "duration_days": "25 - 30 Hari",
                "unit": "ikat",
                "market_price_per_unit": 30000,
                "image_url": "/plants/kangkung.jpg",
                "recommendations": [
                    {"title": "Sistem Cut and Come Again", "desc": "Potong batang 5 cm dari pangkal, kangkung akan tumbuh kembali dalam 2 minggu."},
                    {"title": "Tanam di Air", "desc": "Kangkung juga bisa ditanam hidroponik atau sistem rakit apung untuk hasil lebih cepat."}
                ],
                "prohibitions": [
                    {"title": "Jangan Kekurangan Air", "desc": "Kangkung adalah tanaman semi-aquatik, sangat butuh air melimpah."},
                    {"title": "Hindari Naungan Total", "desc": "Meski tahan teduh, kangkung tetap butuh sinar matahari untuk pertumbuhan optimal."}
                ],
                "requirements": {
                    "min_temp": 25, "max_temp": 35,
                    "min_humidity": 70, "max_humidity": 90,
                    "sunlight": "tinggi",
                    "water": "tinggi",
                    "min_space_cm": 15,
                    "growing_days": 27
                },
                "growth_phases": [
                    {"phase": 1, "name": "Perkecambahan", "days": 3, "care": "Rendam benih 24 jam sebelum tanam, jaga media basah", "indicators": "Benih berkecambah"},
                    {"phase": 2, "name": "Vegetatif Cepat", "days": 17, "care": "Siram 2x sehari, pupuk organik cair 1x seminggu", "indicators": "Daun tumbuh cepat, batang memanjang"},
                    {"phase": 3, "name": "Panen Pertama", "days": 5, "care": "Potong batang di atas pangkal 5 cm", "indicators": "Tinggi 20-25 cm, daun hijau segar"},
                    {"phase": 4, "name": "Regenerasi", "days": 2, "care": "Terus siram dan pupuk", "indicators": "Tunas baru muncul dari pangkal"}
                ],
                "common_diseases": [
                    {"name": "Karat Putih", "symptoms": "Bercak putih seperti karat pada daun", "treatment": "Semprot fungisida, perbaiki sirkulasi udara", "severity": "sedang"},
                    {"name": "Kutu Daun", "symptoms": "Daun keriting, ada kutu kecil", "treatment": "Semprot air sabun atau pestisida organik", "severity": "rendah"}
                ]
            },
            
            # ============ TOGA & BUMBU ============
            {
                "name": "Bawang Putih",
                "description": "Bawang putih adalah bumbu dapur yang juga berkhasiat obat, dapat ditanam di pot dengan perawatan yang tepat.",
                "category": "TOGA",
                "difficulty_level": "Sedang",
                "duration_days": "90 - 120 Hari",
                "unit": "kg",
                "market_price_per_unit": 32581,
                "image_url": "/plants/bawang-putih.jpg",
                "recommendations": [
                    {"title": "Pilih Varietas Lokal", "desc": "Gunakan varietas bawang putih lokal yang sudah beradaptasi dengan iklim tropis."},
                    {"title": "Tanam Siung Besar", "desc": "Pilih siung yang besar dan sehat untuk hasil umbi yang optimal."}
                ],
                "prohibitions": [
                    {"title": "Hindari Genangan", "desc": "Bawang putih sangat rentan busuk umbi jika media tergenang air."},
                    {"title": "Jangan Terlalu Dalam", "desc": "Tanam siung hanya sedalam 2-3 cm dengan ujung runcing menghadap atas."}
                ],
                "requirements": {
                    "min_temp": 15, "max_temp": 25,
                    "min_humidity": 60, "max_humidity": 75,
                    "sunlight": "tinggi",
                    "water": "rendah",
                    "min_space_cm": 15,
                    "growing_days": 105
                },
                "growth_phases": [
                    {"phase": 1, "name": "Penanaman", "days": 14, "care": "Siram sedikit, jangan terlalu basah", "indicators": "Tunas hijau muncul dari siung"},
                    {"phase": 2, "name": "Vegetatif", "days": 60, "care": "Berikan pupuk NPK dengan K tinggi", "indicators": "Daun tumbuh panjang dan hijau"},
                    {"phase": 3, "name": "Pembentukan Umbi", "days": 21, "care": "Kurangi penyiraman drastis", "indicators": "Daun mulai menguning dari ujung"},
                    {"phase": 4, "name": "Panen", "days": 10, "care": "Hentikan penyiraman total", "indicators": "Daun kering 75%, siap dipanen"}
                ],
                "common_diseases": [
                    {"name": "Fusarium", "symptoms": "Daun menguning, umbi busuk", "treatment": "Gunakan bibit sehat, rotasi tanaman", "severity": "tinggi"},
                    {"name": "Trips", "symptoms": "Bercak putih pada daun", "treatment": "Semprot insektisida organik", "severity": "sedang"}
                ]
            },
            {
                "name": "Kemangi",
                "description": "Kemangi adalah herba aromatik yang mudah tumbuh, cocok untuk lalapan dan bumbu masakan, serta mengusir nyamuk.",
                "category": "TOGA",
                "difficulty_level": "Mudah",
                "duration_days": "30 - 40 Hari",
                "unit": "ikat",
                "market_price_per_unit": 1900,
                "image_url": "/plants/kemangi.jpg",
                "recommendations": [
                    {"title": "Panen Rutin", "desc": "Petik ujung batang secara rutin untuk merangsang pertumbuhan cabang baru."},
                    {"title": "Hindari Bunga", "desc": "Potong bunga yang muncul agar energi tanaman fokus ke daun."}
                ],
                "prohibitions": [
                    {"title": "Jangan Kering Kerontang", "desc": "Kemangi butuh media lembab konsisten, kekeringan membuat daun layu."},
                    {"title": "Hindari Pestisida Kimia", "desc": "Kemangi untuk konsumsi, gunakan pestisida organik saja."}
                ],
                "requirements": {
                    "min_temp": 20, "max_temp": 30,
                    "min_humidity": 65, "max_humidity": 85,
                    "sunlight": "tinggi",
                    "water": "sedang",
                    "min_space_cm": 20,
                    "growing_days": 35
                },
                "growth_phases": [
                    {"phase": 1, "name": "Semai", "days": 7, "care": "Jaga media lembab, tempatkan di tempat teduh", "indicators": "Benih berkecambah"},
                    {"phase": 2, "name": "Bibit", "days": 7, "care": "Pindah ke pot lebih besar", "indicators": "Daun sejati 4-6 helai"},
                    {"phase": 3, "name": "Vegetatif", "days": 16, "care": "Pupuk organik cair seminggu sekali", "indicators": "Cabang banyak, daun lebat"},
                    {"phase": 4, "name": "Panen Berkelanjutan", "days": 5, "care": "Panen ujung batang secara rutin", "indicators": "Tinggi 20-30 cm, siap dipanen"}
                ],
                "common_diseases": [
                    {"name": "Bercak Daun", "symptoms": "Bintik coklat pada daun", "treatment": "Buang daun terinfeksi, semprot fungisida organik", "severity": "rendah"},
                    {"name": "Kutu Putih", "symptoms": "Lapisan putih seperti kapas", "treatment": "Semprot alkohol 70% atau insektisida organik", "severity": "rendah"}
                ]
            },
            {
                "name": "Jahe",
                "description": "Jahe adalah tanaman rimpang yang berkhasiat obat dan bumbu, cocok ditanam di pot dengan media yang gembur.",
                "category": "TOGA",
                "difficulty_level": "Sedang",
                "duration_days": "240 - 300 Hari",
                "unit": "kg",
                "market_price_per_unit": 15000,
                "image_url": "/plants/jahe.jpg",
                "recommendations": [
                    {"title": "Media Gembur", "desc": "Campuran tanah, kompos, dan sekam 1:1:1 untuk rimpang berkembang maksimal."},
                    {"title": "Tanam Rimpang Bertunas", "desc": "Pilih rimpang yang sudah ada tunasnya untuk pertumbuhan lebih cepat."}
                ],
                "prohibitions": [
                    {"title": "Hindari Sinar Langsung", "desc": "Jahe lebih suka tempat teduh parsial, sinar langsung membuat daun terbakar."},
                    {"title": "Jangan Terlalu Basah", "desc": "Media terlalu basah menyebabkan rimpang mudah busuk."}
                ],
                "requirements": {
                    "min_temp": 20, "max_temp": 35,
                    "min_humidity": 70, "max_humidity": 90,
                    "sunlight": "rendah",
                    "water": "sedang",
                    "min_space_cm": 30,
                    "growing_days": 270
                },
                "growth_phases": [
                    {"phase": 1, "name": "Penanaman", "days": 30, "care": "Siram secukupnya, jangan terlalu basah", "indicators": "Tunas muncul dari rimpang"},
                    {"phase": 2, "name": "Vegetatif", "days": 120, "care": "Berikan pupuk kompos setiap bulan", "indicators": "Batang tumbuh tinggi, daun lebat"},
                    {"phase": 3, "name": "Pembentukan Rimpang", "days": 90, "care": "Tambahkan media di sekitar batang", "indicators": "Rimpang membesar di dalam media"},
                    {"phase": 4, "name": "Panen", "days": 30, "care": "Kurangi penyiraman menjelang panen", "indicators": "Daun menguning, rimpang siap panen"}
                ],
                "common_diseases": [
                    {"name": "Busuk Rimpang", "symptoms": "Rimpang lunak dan berbau busuk", "treatment": "Perbaiki drainase, gunakan fungisida", "severity": "tinggi"},
                    {"name": "Bercak Daun", "symptoms": "Bercak coklat pada daun", "treatment": "Semprot fungisida organik, perbaiki sirkulasi", "severity": "sedang"}
                ]
            },
            {
                "name": "Daun Pandan",
                "description": "Daun pandan adalah tanaman aromatik yang wangi, cocok untuk pewarna dan pengharum makanan serta minuman.",
                "category": "TOGA",
                "difficulty_level": "Mudah",
                "duration_days": "60 - 90 Hari",
                "unit": "ikat",
                "market_price_per_unit": 5000,
                "image_url": "/plants/daun-pandan.jpg",
                "recommendations": [
                    {"title": "Tanam dari Anakan", "desc": "Gunakan anakan yang tumbuh di sekitar tanaman induk untuk hasil lebih cepat."},
                    {"title": "Panen Daun Tua", "desc": "Petik daun yang sudah tua dari pangkal untuk aroma lebih wangi."}
                ],
                "prohibitions": [
                    {"title": "Jangan Kering Total", "desc": "Pandan butuh media lembab, kekeringan membuat daun kering dan tidak wangi."},
                    {"title": "Hindari Genangan", "desc": "Meski suka lembab, genangan air tetap berbahaya untuk akar."}
                ],
                "requirements": {
                    "min_temp": 22, "max_temp": 32,
                    "min_humidity": 70, "max_humidity": 90,
                    "sunlight": "sedang",
                    "water": "tinggi",
                    "min_space_cm": 30,
                    "growing_days": 75
                },
                "growth_phases": [
                    {"phase": 1, "name": "Penanaman Anakan", "days": 21, "care": "Siram rutin pagi dan sore", "indicators": "Anakan berakar dan mulai tumbuh"},
                    {"phase": 2, "name": "Vegetatif", "days": 39, "care": "Berikan pupuk kompos setiap bulan", "indicators": "Daun tumbuh lebat dan panjang"},
                    {"phase": 3, "name": "Panen Berkelanjutan", "days": 15, "care": "Panen daun tua dari pangkal", "indicators": "Daun panjang 40-60 cm, wangi kuat"}
                ],
                "common_diseases": [
                    {"name": "Bercak Daun", "symptoms": "Bintik coklat pada daun", "treatment": "Buang daun terinfeksi, semprotkan fungisida", "severity": "rendah"},
                    {"name": "Akar Busuk", "symptoms": "Daun menguning, tanaman layu", "treatment": "Perbaiki drainase, kurangi penyiraman", "severity": "sedang"}
                ]
            },
            {
                "name": "Kunyit",
                "description": "Kunyit adalah tanaman rimpang yang berkhasiat sebagai obat dan pewarna alami, mudah tumbuh di pot.",
                "category": "TOGA",
                "difficulty_level": "Mudah",
                "duration_days": "240 - 270 Hari",
                "unit": "kg",
                "market_price_per_unit": 8000,
                "image_url": "/plants/kunyit.jpg",
                "recommendations": [
                    {"title": "Media Gembur Kaya Organik", "desc": "Campurkan kompos banyak untuk rimpang berkualitas baik."},
                    {"title": "Tanam di Tempat Teduh", "desc": "Kunyit lebih produktif di area yang teduh parsial."}
                ],
                "prohibitions": [
                    {"title": "Hindari Media Padat", "desc": "Media padat menghambat pertumbuhan rimpang."},
                    {"title": "Jangan Terlalu Basah", "desc": "Kelembaban berlebih menyebabkan rimpang busuk."}
                ],
                "requirements": {
                    "min_temp": 20, "max_temp": 35,
                    "min_humidity": 70, "max_humidity": 90,
                    "sunlight": "rendah",
                    "water": "sedang",
                    "min_space_cm": 30,
                    "growing_days": 255
                },
                "growth_phases": [
                    {"phase": 1, "name": "Penanaman", "days": 30, "care": "Siram secukupnya 2-3 hari sekali", "indicators": "Tunas muncul dari rimpang"},
                    {"phase": 2, "name": "Vegetatif", "days": 120, "care": "Pupuk organik setiap bulan", "indicators": "Daun tumbuh tinggi dan lebat"},
                    {"phase": 3, "name": "Pembentukan Rimpang", "days": 75, "care": "Tambahkan kompos di sekitar batang", "indicators": "Rimpang membesar dalam media"},
                    {"phase": 4, "name": "Panen", "days": 30, "care": "Kurangi penyiraman", "indicators": "Daun menguning, siap panen"}
                ],
                "common_diseases": [
                    {"name": "Busuk Rimpang", "symptoms": "Rimpang lunak dan berbau", "treatment": "Perbaiki drainase, fungisida", "severity": "tinggi"},
                    {"name": "Bercak Daun", "symptoms": "Bercak coklat pada daun", "treatment": "Semprot fungisida organik", "severity": "sedang"}
                ]
            },
            {
                "name": "Seledri",
                "description": "Seledri adalah sayuran aromatik yang digunakan sebagai penyedap masakan, mudah ditanam di pot kecil.",
                "category": "TOGA",
                "difficulty_level": "Sedang",
                "duration_days": "75 - 90 Hari",
                "unit": "kg",
                "market_price_per_unit": 30000,
                "image_url": "/plants/seledri.jpg",
                "recommendations": [
                    {"title": "Panen Bertahap", "desc": "Potong batang luar secara bertahap, biarkan yang dalam terus tumbuh."},
                    {"title": "Tanam dari Sisa Pangkal", "desc": "Rendam pangkal seledri dari pasar dalam air, akan tumbuh akar baru."}
                ],
                "prohibitions": [
                    {"title": "Hindari Panas Berlebih", "desc": "Seledri lebih suka tempat teduh parsial, panas membuat batang keras."},
                    {"title": "Jangan Kekeringan", "desc": "Seledri butuh media lembab konsisten."}
                ],
                "requirements": {
                    "min_temp": 15, "max_temp": 25,
                    "min_humidity": 65, "max_humidity": 85,
                    "sunlight": "sedang",
                    "water": "tinggi",
                    "min_space_cm": 20,
                    "growing_days": 82
                },
                "growth_phases": [
                    {"phase": 1, "name": "Semai", "days": 14, "care": "Jaga media lembab, benih kecil butuh waktu", "indicators": "Benih berkecambah lambat"},
                    {"phase": 2, "name": "Bibit", "days": 21, "care": "Pindah ke pot lebih besar", "indicators": "Daun sejati 3-4 helai"},
                    {"phase": 3, "name": "Vegetatif", "days": 40, "care": "Pupuk NPK dan organik bergantian", "indicators": "Batang tumbuh tinggi, daun lebat"},
                    {"phase": 4, "name": "Panen", "days": 7, "care": "Panen batang luar secara bertahap", "indicators": "Tinggi 25-30 cm, batang tebal"}
                ],
                "common_diseases": [
                    {"name": "Bercak Daun", "symptoms": "Bercak coklat pada daun", "treatment": "Semprot fungisida, perbaiki sirkulasi", "severity": "sedang"},
                    {"name": "Aphids", "symptoms": "Kutu kecil di batang muda", "treatment": "Semprot air sabun atau pestisida organik", "severity": "rendah"}
                ]
            },
            {
                "name": "Bawang Merah",
                "description": "Bawang merah adalah bumbu dapur esensial yang bisa ditanam di pot, cocok untuk urban farming skala kecil.",
                "category": "TOGA",
                "difficulty_level": "Sedang",
                "duration_days": "60 - 75 Hari",
                "unit": "kg",
                "market_price_per_unit": 37358,
                "image_url": "/plants/bawang-merah.jpg",
                "recommendations": [
                    {"title": "Pilih Bibit Lokal", "desc": "Gunakan varietas bawang merah lokal yang cocok dengan iklim tropis."},
                    {"title": "Tanam Umbi Kecil-Sedang", "desc": "Umbi ukuran sedang menghasilkan anakan lebih banyak."}
                ],
                "prohibitions": [
                    {"title": "Hindari Genangan", "desc": "Bawang merah sangat rentan busuk jika media tergenang."},
                    {"title": "Jangan Overwatering", "desc": "Siram sedikit saja, media cukup lembab tidak basah."}
                ],
                "requirements": {
                    "min_temp": 25, "max_temp": 32,
                    "min_humidity": 60, "max_humidity": 80,
                    "sunlight": "tinggi",
                    "water": "rendah",
                    "min_space_cm": 15,
                    "growing_days": 67
                },
                "growth_phases": [
                    {"phase": 1, "name": "Penanaman", "days": 7, "care": "Tanam umbi sedalam 2/3 bagian, siram sedikit", "indicators": "Tunas hijau muncul"},
                    {"phase": 2, "name": "Vegetatif", "days": 35, "care": "Pupuk NPK dengan K tinggi setiap 10 hari", "indicators": "Daun tumbuh panjang, anakan muncul"},
                    {"phase": 3, "name": "Pembentukan Umbi", "days": 18, "care": "Kurangi penyiraman drastis", "indicators": "Daun mulai rebah dan menguning"},
                    {"phase": 4, "name": "Panen", "days": 7, "care": "Hentikan penyiraman total", "indicators": "Daun kering 75%, umbi siap dipanen"}
                ],
                "common_diseases": [
                    {"name": "Fusarium", "symptoms": "Daun menguning, umbi busuk", "treatment": "Gunakan bibit sehat, rotasi tanaman", "severity": "tinggi"},
                    {"name": "Ulat Bawang", "symptoms": "Daun berlubang", "treatment": "Semprot pestisida organik", "severity": "sedang"}
                ]
            },
            
            # ============ BUAH ============
            {
                "name": "Cabe Rawit Merah",
                "description": "Cabe rawit adalah tanaman buah pedas yang produktif, cocok ditanam di pot dan bisa panen berkali-kali.",
                "category": "Buah",
                "difficulty_level": "Sedang",
                "duration_days": "90 - 120 Hari",
                "unit": "kg",
                "market_price_per_unit": 60995,
                "image_url": "/plants/cabe-rawit.jpg",
                "recommendations": [
                    {"title": "Rajin Membuang Bunga Pertama", "desc": "Buang 2-3 bunga pertama agar tanaman fokus pada pertumbuhan batang dan akar."},
                    {"title": "Pasang Ajir", "desc": "Pasang tongkat penyangga saat tanaman mulai berbuah agar batang tidak patah."}
                ],
                "prohibitions": [
                    {"title": "Hindari Overwatering", "desc": "Cabe tidak suka media terlalu basah, rentan busuk akar."},
                    {"title": "Jangan Pupuk Nitrogen Berlebih", "desc": "Nitrogen tinggi membuat daun lebat tapi buah sedikit."}
                ],
                "requirements": {
                    "min_temp": 24, "max_temp": 32,
                    "min_humidity": 60, "max_humidity": 80,
                    "sunlight": "tinggi",
                    "water": "sedang",
                    "min_space_cm": 30,
                    "growing_days": 105
                },
                "growth_phases": [
                    {"phase": 1, "name": "Semai", "days": 14, "care": "Jaga media lembab, tabur di seedtray", "indicators": "Biji berkecambah"},
                    {"phase": 2, "name": "Bibit", "days": 21, "care": "Pindah ke pot lebih besar saat daun sejati 4 helai", "indicators": "Bibit kuat, siap tanam"},
                    {"phase": 3, "name": "Vegetatif", "days": 35, "care": "Pupuk NPK seimbang, buang bunga pertama", "indicators": "Batang kokoh, cabang banyak"},
                    {"phase": 4, "name": "Berbunga & Berbuah", "days": 25, "care": "Pupuk dengan P dan K tinggi", "indicators": "Bunga muncul, buah mulai terbentuk"},
                    {"phase": 5, "name": "Panen Berkelanjutan", "days": 10, "care": "Panen buah merah secara bertahap", "indicators": "Buah merah, siap dipanen"}
                ],
                "common_diseases": [
                    {"name": "Antraknosa", "symptoms": "Bercak coklat pada buah", "treatment": "Semprot fungisida, jaga kelembaban tidak berlebih", "severity": "tinggi"},
                    {"name": "Thrips", "symptoms": "Daun keriting, buah cacat", "treatment": "Semprot insektisida organik", "severity": "sedang"},
                    {"name": "Layu Fusarium", "symptoms": "Tanaman layu tiba-tiba", "treatment": "Buang tanaman terinfeksi, sterilkan media", "severity": "tinggi"}
                ]
            },
            {
                "name": "Tomat",
                "description": "Tomat adalah tanaman buah yang populer untuk urban farming, kaya vitamin dan bisa ditanam di pot.",
                "category": "Buah",
                "difficulty_level": "Sedang",
                "duration_days": "75 - 90 Hari",
                "unit": "kg",
                "market_price_per_unit": 8391,
                "image_url": "/plants/tomat.jpg",
                "recommendations": [
                    {"title": "Pangkas Tunas Air", "desc": "Buang tunas yang tumbuh di ketiak daun agar nutrisi fokus ke buah."},
                    {"title": "Pasang Ajir Kokoh", "desc": "Gunakan tongkat bambu setinggi 1.5 meter untuk menopang tanaman."}
                ],
                "prohibitions": [
                    {"title": "Hindari Penyiraman dari Atas", "desc": "Siram langsung ke media, menghindari daun basah yang rentan penyakit."},
                    {"title": "Jangan Tanam Terlalu Rapat", "desc": "Jarak tanam minimal 50 cm untuk sirkulasi udara baik."}
                ],
                "requirements": {
                    "min_temp": 18, "max_temp": 29,
                    "min_humidity": 60, "max_humidity": 75,
                    "sunlight": "tinggi",
                    "water": "sedang",
                    "min_space_cm": 50,
                    "growing_days": 82
                },
                "growth_phases": [
                    {"phase": 1, "name": "Semai", "days": 10, "care": "Tabur benih, jaga media lembab", "indicators": "Biji berkecambah"},
                    {"phase": 2, "name": "Bibit", "days": 21, "care": "Pindah ke pot saat daun sejati 4-6 helai", "indicators": "Bibit kuat, batang tegak"},
                    {"phase": 3, "name": "Vegetatif", "days": 28, "care": "Pupuk NPK, pasang ajir, pangkas tunas air", "indicators": "Batang tinggi, daun lebat"},
                    {"phase": 4, "name": "Berbunga", "days": 14, "care": "Pupuk dengan P dan K tinggi", "indicators": "Bunga kuning muncul"},
                    {"phase": 5, "name": "Berbuah & Panen", "days": 9, "care": "Panen buah yang sudah merah", "indicators": "Buah merah, siap dipanen"}
                ],
                "common_diseases": [
                    {"name": "Late Blight", "symptoms": "Bercak coklat pada daun dan buah", "treatment": "Semprot fungisida berbahan tembaga", "severity": "tinggi"},
                    {"name": "Busuk Ujung Buah", "symptoms": "Ujung buah hitam dan keras", "treatment": "Tambahkan kalsium, siram konsisten", "severity": "sedang"},
                    {"name": "Kutu Daun", "symptoms": "Daun keriting, kutu hijau", "treatment": "Semprot air sabun atau pestisida organik", "severity": "rendah"}
                ]
            },
            {
                "name": "Terong",
                "description": "Terong adalah tanaman buah yang mudah tumbuh, produktif, dan cocok untuk berbagai masakan Indonesia.",
                "category": "Buah",
                "difficulty_level": "Mudah",
                "duration_days": "70 - 90 Hari",
                "unit": "kg",
                "market_price_per_unit": 15000,
                "image_url": "/plants/terong.jpg",
                "recommendations": [
                    {"title": "Pilih Varietas yang Cocok", "desc": "Terong ungu lokal atau terong hijau lebih adaptif di iklim tropis."},
                    {"title": "Panen Muda", "desc": "Panen terong saat masih muda untuk tekstur lebih lembut dan tidak pahit."}
                ],
                "prohibitions": [
                    {"title": "Hindari Media Terlalu Basah", "desc": "Terong rentan busuk akar jika media tergenang."},
                    {"title": "Jangan Biarkan Buah Terlalu Tua", "desc": "Buah terlalu tua akan keras dan banyak biji."}
                ],
                "requirements": {
                    "min_temp": 22, "max_temp": 30,
                    "min_humidity": 60, "max_humidity": 80,
                    "sunlight": "tinggi",
                    "water": "sedang",
                    "min_space_cm": 40,
                    "growing_days": 80
                },
                "growth_phases": [
                    {"phase": 1, "name": "Semai", "days": 14, "care": "Tabur benih, jaga kelembaban", "indicators": "Benih berkecambah"},
                    {"phase": 2, "name": "Bibit", "days": 21, "care": "Pindah tanam saat daun sejati 4 helai", "indicators": "Bibit siap tanam"},
                    {"phase": 3, "name": "Vegetatif", "days": 28, "care": "Pupuk NPK seimbang setiap 2 minggu", "indicators": "Batang kokoh, daun besar"},
                    {"phase": 4, "name": "Berbunga & Berbuah", "days": 10, "care": "Pupuk dengan K tinggi", "indicators": "Bunga ungu muncul, buah terbentuk"},
                    {"phase": 5, "name": "Panen", "days": 7, "care": "Panen buah yang masih mengkilap", "indicators": "Buah besar, kulit mengkilap"}
                ],
                "common_diseases": [
                    {"name": "Layu Bakteri", "symptoms": "Tanaman layu mendadak", "treatment": "Buang tanaman, sterilkan area", "severity": "tinggi"},
                    {"name": "Penggerek Buah", "symptoms": "Buah berlubang, ada ulat", "treatment": "Bungkus buah muda, gunakan insektisida", "severity": "sedang"},
                    {"name": "Kutu Kebul", "symptoms": "Kutu putih di bawah daun", "treatment": "Semprot insektisida organik", "severity": "sedang"}
                ]
            },
            {
                "name": "Paprika",
                "description": "Paprika adalah cabai manis yang kaya vitamin C, cocok untuk salad dan masakan, bisa ditanam di pot besar.",
                "category": "Buah",
                "difficulty_level": "Sulit",
                "duration_days": "90 - 120 Hari",
                "unit": "kg",
                "market_price_per_unit": 60000,
                "image_url": "/plants/paprika.jpg",
                "recommendations": [
                    {"title": "Kontrol Suhu", "desc": "Paprika sensitif suhu, usahakan suhu tetap 20-28°C dengan naungan jika perlu."},
                    {"title": "Pupuk Kalsium", "desc": "Berikan kalsium ekstra untuk mencegah busuk ujung buah."}
                ],
                "prohibitions": [
                    {"title": "Hindari Panas Ekstrem", "desc": "Suhu di atas 32°C membuat bunga rontok dan buah tidak terbentuk."},
                    {"title": "Jangan Overwatering", "desc": "Media harus lembab tapi tidak basah, paprika rentan busuk akar."}
                ],
                "requirements": {
                    "min_temp": 20, "max_temp": 28,
                    "min_humidity": 60, "max_humidity": 75,
                    "sunlight": "tinggi",
                    "water": "sedang",
                    "min_space_cm": 50,
                    "growing_days": 105
                },
                "growth_phases": [
                    {"phase": 1, "name": "Semai", "days": 14, "care": "Suhu stabil 25°C, jaga kelembaban", "indicators": "Benih berkecambah lambat"},
                    {"phase": 2, "name": "Bibit", "days": 28, "care": "Pindah tanam saat daun sejati 6 helai", "indicators": "Bibit kuat, siap tanam"},
                    {"phase": 3, "name": "Vegetatif", "days": 35, "care": "Pupuk NPK seimbang, pasang ajir", "indicators": "Batang kokoh, percabangan baik"},
                    {"phase": 4, "name": "Berbunga", "days": 21, "care": "Pupuk K dan Ca tinggi, jaga suhu", "indicators": "Bunga putih muncul"},
                    {"phase": 5, "name": "Berbuah & Panen", "days": 7, "care": "Panen saat buah sudah berwarna penuh", "indicators": "Buah merah/kuning/oranye"}
                ],
                "common_diseases": [
                    {"name": "Busuk Ujung Buah", "symptoms": "Ujung buah hitam", "treatment": "Tambahkan kalsium, siram konsisten", "severity": "tinggi"},
                    {"name": "Antraknosa", "symptoms": "Bercak pada buah matang", "treatment": "Semprot fungisida, panen tepat waktu", "severity": "sedang"},
                    {"name": "Thrips", "symptoms": "Bunga rontok, daun keriting", "treatment": "Semprot insektisida", "severity": "sedang"}
                ]
            },
            {
                "name": "Zukini",
                "description": "Zukini adalah sayuran buah yang cepat tumbuh dan produktif, cocok untuk urban farming dengan hasil melimpah.",
                "category": "Buah",
                "difficulty_level": "Mudah",
                "duration_days": "45 - 60 Hari",
                "unit": "kg",
                "market_price_per_unit": 25000,
                "image_url": "/plants/zukini.jpg",
                "recommendations": [
                    {"title": "Panen Saat Muda", "desc": "Panen zukini saat panjang 15-20 cm untuk rasa terbaik, jangan biarkan terlalu besar."},
                    {"title": "Penyerbukan Manual", "desc": "Jika kurang serangga penyerbuk, lakukan penyerbukan manual dengan kuas."}
                ],
                "prohibitions": [
                    {"title": "Jangan Siram Daun", "desc": "Siram langsung ke media, daun basah rentan embun tepung."},
                    {"title": "Hindari Buah Terlalu Tua", "desc": "Buah terlalu besar akan keras dan kurang enak."}
                ],
                "requirements": {
                    "min_temp": 18, "max_temp": 30,
                    "min_humidity": 60, "max_humidity": 75,
                    "sunlight": "tinggi",
                    "water": "tinggi",
                    "min_space_cm": 60,
                    "growing_days": 52
                },
                "growth_phases": [
                    {"phase": 1, "name": "Perkecambahan", "days": 7, "care": "Tanam benih langsung di pot besar", "indicators": "Benih berkecambah"},
                    {"phase": 2, "name": "Vegetatif", "days": 21, "care": "Pupuk NPK seimbang, siram rutin", "indicators": "Daun besar, batang kokoh"},
                    {"phase": 3, "name": "Berbunga", "days": 10, "care": "Pupuk dengan P dan K tinggi", "indicators": "Bunga kuning muncul"},
                    {"phase": 4, "name": "Berbuah & Panen", "days": 14, "care": "Panen buah muda setiap 2-3 hari", "indicators": "Buah terbentuk cepat, siap panen"}
                ],
                "common_diseases": [
                    {"name": "Embun Tepung", "symptoms": "Lapisan putih seperti tepung di daun", "treatment": "Semprot larutan baking soda atau fungisida", "severity": "sedang"},
                    {"name": "Busuk Buah", "symptoms": "Buah membusuk dari ujung", "treatment": "Perbaiki drainase, hindari kontak buah dengan tanah basah", "severity": "sedang"},
                    {"name": "Kutu Daun", "symptoms": "Daun keriting, ada kutu", "treatment": "Semprot air sabun atau pestisida organik", "severity": "rendah"}
                ]
            }
        ]
        
        # Insert all plants
        for plant_data in plants_data:
            plant = Plant(**plant_data)
            db.add(plant)
        
        db.commit()
        
        print("=" * 70)
        print(f"✅ Successfully seeded {len(plants_data)} plants!")
        print("=" * 70)
        print("\nPlants by category:")
        pangan = [p for p in plants_data if p['category'] == 'Pangan']
        toga = [p for p in plants_data if p['category'] == 'TOGA']
        buah = [p for p in plants_data if p['category'] == 'Buah']
        
        print(f"\n📦 Tanaman Pangan ({len(pangan)} plants):")
        for p in pangan:
            print(f"   - {p['name']} ({p['unit']}) - Rp{p['market_price_per_unit']:,}")
        
        print(f"\n🌿 TOGA & Bumbu ({len(toga)} plants):")
        for p in toga:
            print(f"   - {p['name']} ({p['unit']}) - Rp{p['market_price_per_unit']:,}")
        
        print(f"\n🍅 Buah ({len(buah)} plants):")
        for p in buah:
            print(f"   - {p['name']} ({p['unit']}) - Rp{p['market_price_per_unit']:,}")
        
        print("\n" + "=" * 70)
        
    except Exception as e:
        print(f"❌ Error seeding plants: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting plant seeder...")
    seed_plants()
    print("Plant seeding completed!")
