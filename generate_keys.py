from Crypto.PublicKey import RSA

# Fungsi untuk menghasilkan pasangan kunci RSA
def generate_rsa_keys():
    key = RSA.generate(2048)  # Membuat kunci RSA 2048-bit
    private_key = key.export_key()  # Mendapatkan private key
    public_key = key.publickey().export_key()  # Mendapatkan public key
    
    # Menyimpan kunci ke dalam file
    with open("private.pem", "wb") as private_file:
        private_file.write(private_key)
    
    with open("public.pem", "wb") as public_file:
        public_file.write(public_key)
    
    print("RSA Keys Generated and Saved to 'private.pem' and 'public.pem'")

# Memanggil fungsi untuk menghasilkan kunci RSA
if __name__ == "__main__":
    generate_rsa_keys()
