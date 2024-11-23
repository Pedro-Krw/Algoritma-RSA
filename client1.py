from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad
import socket

# Fungsi untuk mengenkripsi menggunakan RSA
def encrypt_rsa(public_key, data):
    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

# Fungsi untuk mengenkripsi pesan menggunakan DES
def encrypt_message(des_key, message):
    cipher = DES.new(des_key, DES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode(), 8))
    return encrypted_message

# Jalankan client
def start_client():
    try:
        # Buat koneksi ke server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 12345))
        print("Terhubung ke server.")

        # Terima public key dari server
        public_key_data = client_socket.recv(1024)
        public_key = RSA.import_key(public_key_data)
        print("Public key RSA diterima dari server.")

        # Generate DES key (8 byte)
        des_key = b'secret_k'  # Harus tepat 8 byte

        # Enkripsi DES key menggunakan RSA
        encrypted_des_key = encrypt_rsa(public_key, des_key)
        client_socket.sendall(encrypted_des_key)
        print("Kunci DES terenkripsi telah dikirim ke server.")

        # Masukkan pesan untuk dikirim
        message = input("Masukkan pesan untuk dienkripsi: ")

        # Enkripsi pesan menggunakan DES
        encrypted_message = encrypt_message(des_key, message)
        client_socket.sendall(encrypted_message)
        print("Pesan terenkripsi telah dikirim.")

        client_socket.close()

    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    start_client()
