from Crypto.Cipher import DES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad
import socket

# Fungsi untuk mendekripsi menggunakan RSA
def decrypt_rsa(private_key, encrypted_data):
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_data)

# Fungsi untuk mendekripsi pesan menggunakan DES
def decrypt_message(des_key, encrypted_message):
    cipher = DES.new(des_key, DES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), 8)
    return decrypted_message.decode()

# Jalankan server
def start_server():
    try:
        # Buat kunci RSA
        key = RSA.generate(2048)
        private_key = key
        public_key = key.publickey()

        # Inisialisasi server socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 12345))
        server_socket.listen(1)
        print("Server berjalan dan menunggu koneksi...")

        while True:
            client_socket, addr = server_socket.accept()
            print(f"Terhubung dengan {addr}")

            # Kirim public key ke client
            client_socket.sendall(public_key.export_key())
            print("Public key RSA telah dikirim ke client.")

            # Terima kunci DES terenkripsi dari client
            encrypted_des_key = client_socket.recv(1024)
            des_key = decrypt_rsa(private_key, encrypted_des_key)
            print("Kunci DES berhasil diterima dan didekripsi.")

            # Terima pesan terenkripsi dari client
            encrypted_message = client_socket.recv(1024)
            message = decrypt_message(des_key, encrypted_message)
            print(f"Pesan dari client: {message}")

            client_socket.close()
            print("Koneksi ditutup.\n")
    
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    start_server()
