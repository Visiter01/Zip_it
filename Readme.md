# ZIPIT - File Compressor Web App

A Django-based web application designed to efficiently compress and decompress files. Unlike standard web wrappers for existing zip libraries, this project implements core lossless data compression algorithms from the ground up to reduce file sizes for easier storage and faster transfer.

## 🚀 Features
* **Web Interface:** Clean and intuitive UI built with Django templates for uploading and downloading files.
* **Lossless Compression:** Ensures that the decompressed file is an exact replica of the original.
* **Algorithm Implementations:** Custom backend logic for complex data structures and compression algorithms.
* **Compression Stats:** Displays original size, compressed size, and the compression ratio achieved.

## 💻 Tech Stack
* **Backend:** Python, Django
* **Frontend:** HTML, CSS
* **Core Algorithms:** Huffman Coding, Deflate Algorithm

## 🧠 How the Compression Works

This project utilizes a two-step approach to achieve optimal compression:

1. **Huffman Encoding:** The application reads the uploaded file and builds a frequency dictionary of all characters/bytes. It then constructs a Huffman Tree using a priority queue. By assigning shorter binary codes to the most frequent characters and longer codes to less frequent ones, it effectively reduces the overall file size without losing any data.

2. **Deflate Algorithm:** To optimize the compression even further, the app combines Huffman coding with LZ77-style dictionary compression. It scans the data for duplicate strings and replaces them with shorter pointers (distance and length) to previous occurrences, passing the output through the Huffman tree for maximum efficiency.

## 🛠️ How to Run Locally

If you want to run this project on your own machine, follow these steps:

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git)
cd YOUR-REPO-NAME
2. Create and activate a virtual environment (Recommended)

Windows:

DOS
python -m venv venv
.\venv\Scripts\activate
Mac/Linux:

Bash
python3 -m venv venv
source venv/bin/activate
3. Install dependencies

Bash
pip install -r requirements.txt
4. Run database migrations

Bash
python manage.py migrate
5. Start the development server

Bash
python manage.py runserver
6. Access the application
Open your web browser and navigate to http://127.0.0.1:8000/ to start compressing files!
