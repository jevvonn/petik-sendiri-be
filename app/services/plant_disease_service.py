import os
# Use legacy Keras 2 API for compatibility with older models
os.environ['TF_USE_LEGACY_KERAS'] = '1'

import tensorflow as tf
import numpy as np
from PIL import Image
import io
import json


class PlantDiseasePredictor:
    def __init__(self, model_path: str, class_names_path: str):
        """
        Initialize predictor dengan model dan class names
        
        Args:
            model_path: Path ke file model .h5
            class_names_path: Path ke file class_names.json
        """
        print(f"Loading model from: {model_path}")
        self.model = tf.keras.models.load_model(model_path)
        
        print(f"Loading class names from: {class_names_path}")
        with open(class_names_path, 'r') as f:
            self.class_names = json.load(f)
        
        print(f"Model loaded successfully with {len(self.class_names)} classes")
        
        # Informasi penyakit lengkap
        self.disease_info = {
            'Pepper__bell___Bacterial_spot': {
                'plant': 'Paprika',
                'disease': 'Bercak Bakteri',
                'description': 'Penyakit yang disebabkan oleh bakteri Xanthomonas campestris. Menyebabkan bercak-bercak kecil berwarna coklat pada daun dan buah.',
                'treatment': 'Semprotkan bakterisida berbahan tembaga setiap 7-10 hari. Buang dan musnahkan bagian tanaman yang terinfeksi.',
                'prevention': 'Gunakan benih sehat, jaga jarak tanam, hindari penyiraman dari atas, rotasi tanaman.'
            },
            'Pepper__bell___healthy': {
                'plant': 'Paprika',
                'disease': 'Sehat',
                'description': 'Tanaman paprika dalam kondisi sehat, tidak terdeteksi penyakit.',
                'treatment': 'Tidak diperlukan treatment, pertahankan perawatan rutin.',
                'prevention': 'Lanjutkan pemupukan teratur, penyiraman cukup, dan monitor berkala.'
            },
            'Potato___Early_blight': {
                'plant': 'Kentang',
                'disease': 'Hawar Daun Awal',
                'description': 'Penyakit jamur yang disebabkan oleh Alternaria solani. Ditandai dengan bercak coklat konsentris pada daun.',
                'treatment': 'Aplikasi fungisida berbasis tembaga atau mancozeb setiap 7-14 hari. Buang daun terinfeksi.',
                'prevention': 'Rotasi tanaman, jaga kebersihan lahan, gunakan mulsa, hindari kelembaban berlebih.'
            },
            'Potato___Late_blight': {
                'plant': 'Kentang',
                'disease': 'Hawar Daun Akhir',
                'description': 'Penyakit serius yang disebabkan oleh Phytophthora infestans. Dapat menghancurkan tanaman dalam waktu singkat.',
                'treatment': 'Gunakan fungisida sistemik seperti metalaxyl atau cymoxanil. Panen segera jika infeksi parah.',
                'prevention': 'Gunakan varietas tahan, hindari kelembaban tinggi, jaga sirkulasi udara, aplikasi fungisida preventif.'
            },
            'Potato___healthy': {
                'plant': 'Kentang',
                'disease': 'Sehat',
                'description': 'Tanaman kentang dalam kondisi sehat, tidak terdeteksi penyakit.',
                'treatment': 'Tidak diperlukan treatment, pertahankan perawatan rutin.',
                'prevention': 'Pemupukan berimbang, penyiraman teratur, monitor hama dan penyakit.'
            },
            'Tomato_Bacterial_spot': {
                'plant': 'Tomat',
                'disease': 'Bercak Bakteri',
                'description': 'Infeksi bakteri Xanthomonas spp. yang menyebabkan bercak hitam pada daun dan buah.',
                'treatment': 'Semprot dengan bakterisida tembaga. Buang tanaman yang terinfeksi parah.',
                'prevention': 'Gunakan benih bersertifikat, sterilisasi alat, hindari kerja saat tanaman basah.'
            },
            'Tomato_Early_blight': {
                'plant': 'Tomat',
                'disease': 'Hawar Daun Awal',
                'description': 'Penyakit jamur Alternaria solani dengan bercak coklat target pada daun bawah.',
                'treatment': 'Aplikasi fungisida chlorothalonil atau mancozeb setiap 7-10 hari. Pemangkasan daun terinfeksi.',
                'prevention': 'Mulsa plastik, drip irrigation, jaga jarak tanam, rotasi tanaman minimal 2 tahun.'
            },
            'Tomato_Late_blight': {
                'plant': 'Tomat',
                'disease': 'Hawar Daun Akhir',
                'description': 'Penyakit mematikan oleh Phytophthora infestans. Bercak basah kehijauan pada daun dan batang.',
                'treatment': 'Fungisida sistemik (metalaxyl, dimethomorph). Musnahkan tanaman terinfeksi parah.',
                'prevention': 'Varietas tahan, sirkulasi udara baik, hindari overhead watering, aplikasi fungisida preventif.'
            },
            'Tomato_Leaf_Mold': {
                'plant': 'Tomat',
                'disease': 'Jamur Daun',
                'description': 'Jamur Passalora fulva yang tumbuh di permukaan bawah daun. Umum di greenhouse.',
                'treatment': 'Fungisida berbasis tembaga atau chlorothalonil. Tingkatkan ventilasi.',
                'prevention': 'Jaga kelembaban rendah (<85%), sirkulasi udara baik, jarak tanam cukup.'
            },
            'Tomato_Septoria_leaf_spot': {
                'plant': 'Tomat',
                'disease': 'Bercak Daun Septoria',
                'description': 'Jamur Septoria lycopersici menyebabkan bercak bulat dengan titik hitam di tengah.',
                'treatment': 'Fungisida chlorothalonil atau mancozeb. Buang daun terinfeksi.',
                'prevention': 'Mulsa, hindari percikan air ke daun, rotasi tanaman, jarak tanam optimal.'
            },
            'Tomato_Spider_mites_Two_spotted_spider_mite': {
                'plant': 'Tomat',
                'disease': 'Tungau Laba-laba',
                'description': 'Hama tungau (Tetranychus urticae) yang menghisap cairan daun, menyebabkan bercak kuning.',
                'treatment': 'Mitisida atau insektisida organik (minyak neem). Semprotkan air kuat untuk mengurangi populasi.',
                'prevention': 'Jaga kelembaban, hindari kekeringan, gunakan predator alami, bersihkan gulma.'
            },
            'Tomato__Target_Spot': {
                'plant': 'Tomat',
                'disease': 'Bercak Target',
                'description': 'Jamur Corynespora cassiicola dengan pola bercak konsentris seperti target panah.',
                'treatment': 'Fungisida azoxystrobin atau chlorothalonil. Pemangkasan sanitasi.',
                'prevention': 'Rotasi tanaman, mulsa, penyiraman di pagi hari, hindari kelembaban tinggi.'
            },
            'Tomato__Tomato_YellowLeaf__Curl_Virus': {
                'plant': 'Tomat',
                'disease': 'Virus Keriting Daun Kuning',
                'description': 'Virus TYLCV yang ditularkan kutu kebul (whitefly). Daun menguning dan keriting ke atas.',
                'treatment': 'Tidak ada obat untuk virus. Cabut dan musnahkan tanaman terinfeksi. Kontrol whitefly dengan insektisida.',
                'prevention': 'Gunakan varietas tahan, mulsa reflektif, jaring serangga, kontrol whitefly sejak dini.'
            },
            'Tomato__Tomato_mosaic_virus': {
                'plant': 'Tomat',
                'disease': 'Virus Mosaik Tomat',
                'description': 'Virus TMV yang menyebabkan pola mosaik terang-gelap pada daun. Sangat menular.',
                'treatment': 'Tidak ada pengobatan. Cabut tanaman terinfeksi. Sterilisasi alat dan cuci tangan.',
                'prevention': 'Gunakan benih sehat, cuci tangan sebelum bekerja, sterilisasi alat, jangan merokok di dekat tanaman.'
            },
            'Tomato_healthy': {
                'plant': 'Tomat',
                'disease': 'Sehat',
                'description': 'Tanaman tomat dalam kondisi sehat, tidak terdeteksi penyakit atau hama.',
                'treatment': 'Tidak diperlukan treatment, lanjutkan perawatan rutin.',
                'prevention': 'Pemupukan NPK berimbang, penyiraman konsisten, pemangkasan tunas air, monitoring rutin.'
            }
        }
    
    def preprocess_image(self, image_bytes: bytes):
        """
        Preprocessing gambar sebelum prediksi
        
        Args:
            image_bytes: Bytes dari gambar
            
        Returns:
            numpy array yang sudah diproses
        """
        try:
            # Buka gambar
            image = Image.open(io.BytesIO(image_bytes))
            
            # Convert ke RGB (jika grayscale atau RGBA)
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize ke ukuran yang diharapkan model
            image = image.resize((224, 224))
            
            # Convert ke numpy array dan normalize
            image_array = np.array(image) / 255.0
            
            # Expand dimensions untuk batch
            image_array = np.expand_dims(image_array, axis=0)
            
            return image_array
        
        except Exception as e:
            raise ValueError(f"Error preprocessing image: {str(e)}")
    
    def extract_plant_type(self, class_name: str):
        """Extract jenis tanaman dari nama class"""
        if 'Pepper' in class_name or 'pepper' in class_name:
            return 'Paprika'
        elif 'Potato' in class_name or 'potato' in class_name:
            return 'Kentang'
        elif 'Tomato' in class_name or 'tomato' in class_name:
            return 'Tomat'
        else:
            return 'Unknown'
    
    def validate_plant_type(self, predicted_class: str, user_plant_type: str):
        """
        Validasi apakah tanaman yang diprediksi sesuai dengan input user
        
        Args:
            predicted_class: Class yang diprediksi oleh model
            user_plant_type: Jenis tanaman yang diinput user
            
        Returns:
            bool: True jika sesuai, False jika tidak
        """
        predicted_plant = self.extract_plant_type(predicted_class).lower()
        user_plant = user_plant_type.lower()
        
        # Mapping alternatif nama
        plant_mapping = {
            'paprika': ['paprika', 'pepper', 'bell pepper', 'cabai besar'],
            'kentang': ['kentang', 'potato'],
            'tomat': ['tomat', 'tomato']
        }
        
        for standard_name, alternatives in plant_mapping.items():
            if predicted_plant in alternatives and user_plant in alternatives:
                return True
        
        return False
    
    def predict(self, image_bytes: bytes, user_plant_type: str = None):
        """
        Melakukan prediksi penyakit tanaman
        
        Args:
            image_bytes: Bytes dari gambar
            user_plant_type: Jenis tanaman yang diinput user (opsional)
            
        Returns:
            Dictionary berisi hasil prediksi
        """
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_bytes)
            
            # Predict
            predictions = self.model.predict(processed_image, verbose=0)[0]
            
            # Get top prediction
            top_index = np.argmax(predictions)
            predicted_class = self.class_names[top_index]
            confidence = float(predictions[top_index])
            
            # Get top 3 predictions
            top_3_indices = np.argsort(predictions)[-3:][::-1]
            all_predictions = [
                {
                    'disease': self.class_names[i],
                    'confidence': float(predictions[i])
                }
                for i in top_3_indices
            ]
            
            # If confidence < 0.85, return null/empty result
            if confidence < 0.85:
                return {
                    'plant_type': None,
                    'disease_name': None,
                    'confidence': confidence,
                    'is_healthy': None,
                    'description': None,
                    'treatment': None,
                    'prevention': None,
                    'all_predictions': all_predictions,
                    'plant_match': False,
                    'warning': 'Confidence terlalu rendah untuk memberikan hasil yang akurat. Silakan upload gambar yang lebih jelas.'
                }
            
            # Validasi jenis tanaman jika user memberikan input
            plant_match = True
            if user_plant_type:
                plant_match = self.validate_plant_type(predicted_class, user_plant_type)
            
            # Get disease info
            info = self.disease_info.get(predicted_class, {
                'plant': self.extract_plant_type(predicted_class),
                'disease': 'Unknown',
                'description': 'Informasi tidak tersedia untuk penyakit ini.',
                'treatment': 'Silakan konsultasikan dengan ahli pertanian.',
                'prevention': 'Monitor tanaman secara berkala.'
            })
            
            # Check if healthy
            is_healthy = 'healthy' in predicted_class.lower()
            
            result = {
                'plant_type': info['plant'],
                'disease_name': info['disease'],
                'confidence': confidence,
                'is_healthy': is_healthy,
                'description': info['description'],
                'treatment': info['treatment'],
                'prevention': info['prevention'],
                'all_predictions': all_predictions,
                'plant_match': plant_match
            }
            
            # Jika tanaman tidak sesuai, tambahkan warning
            if not plant_match and user_plant_type:
                result['warning'] = f"Perhatian: Anda menginput '{user_plant_type}' tetapi model mendeteksi '{info['plant']}'. Hasil mungkin tidak akurat."
            
            return result
            
        except Exception as e:
            raise Exception(f"Error during prediction: {str(e)}")


# Singleton instance for the predictor
_predictor_instance = None


def get_plant_disease_predictor() -> PlantDiseasePredictor:
    """
    Get or create the singleton PlantDiseasePredictor instance
    
    Returns:
        PlantDiseasePredictor instance
    """
    global _predictor_instance
    
    if _predictor_instance is None:
        # Get the base directory (project root)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        model_path = os.path.join(base_dir, "model-ai", "plant-diasease", "plant_disease_model.h5")
        class_names_path = os.path.join(base_dir, "model-ai", "plant-diasease", "class_names.json")
        
        _predictor_instance = PlantDiseasePredictor(model_path, class_names_path)
    
    return _predictor_instance
