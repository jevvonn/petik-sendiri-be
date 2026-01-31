# Knowledge Base

Folder ini berisi dokumen-dokumen yang akan diproses menjadi knowledge base untuk PetikSendiri Assistant.

## Format File yang Didukung

- PDF (`.pdf`)
- Microsoft Word (`.docx`)
- Text File (`.txt`)

## Cara Penggunaan

1. Letakkan file dokumen tentang urban farming di folder ini
2. Login sebagai superuser
3. Panggil endpoint `POST /api/v1/chat/knowledge-base/process` untuk memproses dokumen
4. Dokumen akan di-split menjadi chunks dan disimpan sebagai vector embeddings

## Contoh Konten yang Disarankan

- Panduan menanam sayuran di rumah
- Tips hidroponik untuk pemula
- Cara merawat tanaman indoor
- Panduan urban farming
- Informasi tentang hama dan penyakit tanaman
- Panduan pemupukan
