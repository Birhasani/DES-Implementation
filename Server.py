import socket
from DES_algorithm import DES_algorithm

def server_program():
    # Buat instance dari DES_algorithm untuk peran "Receiver"
    des = DES_algorithm(role="Receiver")
    
    # Konfigurasi alamat host dan port server
    host = socket.gethostname()  # Mendapatkan nama host dari mesin saat ini
    port = 5000  # Port yang digunakan server untuk mendengarkan

    # Membuat socket untuk server dan bind ke host serta port yang ditentukan
    server_socket = socket.socket() 
    server_socket.bind((host, port)) 

    # Server mulai mendengarkan koneksi
    server_socket.listen(2)
    conn, address = server_socket.accept()  # Menerima koneksi masuk dari client
    print("Connection from: " + str(address))
    
    while True:
        # Menerima data dari client
        data = conn.recv(1024)
        if not data:
            break  # Jika tidak ada data, keluar dari loop

        # Decode pesan dari bytes ke string
        raw_message = data.decode('utf-8')
        des.log_with_timestamp(f"Cipher text received: {raw_message}")

        if raw_message.lower() == 'stop':
            # Jika pesan adalah "stop", kirim kembali ke client sebagai sinyal berhenti
            print("Stop signal received from sender. Closing connection.")
            conn.sendall(bytes("stop", 'utf-8'))
            break  # Keluar dari loop

        # Dekripsi pesan yang diterima dan tampilkan
        plain_text = des.decryption_cbc(raw_message)
        des.log_with_timestamp(f"Plain text received: {plain_text}")
        print("Plain text received: " + str(plain_text))

        # Ambil input pesan dari server untuk dikirim kembali ke client
        message = input(' -> ')
        # Enkripsi pesan sebelum dikirim dan tampilkan log
        cipher_text = des.encryption_cbc(message, output_format="hex")
        des.log_with_timestamp(f"Cipher text sent: {cipher_text}")

        if message.lower() == 'stop':
            # Jika pesan yang dikirim adalah "stop", kirim sinyal berhenti ke client
            conn.sendall(bytes("stop", 'utf-8'))
            print("Stop signal sent to sender. Closing connection.")
            break  # Keluar dari loop

        # Kirim pesan terenkripsi ke client
        conn.sendall(bytes(cipher_text, 'utf-8'))

    # Menutup koneksi setelah keluar dari loop
    conn.close()
    print("Connection fully closed by both parties.")

# Menjalankan program server jika file ini dijalankan secara langsung
if __name__ == '__main__':
    server_program()
