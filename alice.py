import socket
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes

# Step 1: Key Generation
def generate_keys():
    print("Generating RSA keys...")
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    d = inverse(e, phi_n)
    print(f"Generated public key: (e={e}, n={n})")
    print(f"Generated private key: (d={d}, n={n})")
    return (e, n), (d, n)

# Alice Server
def alice_server():
    print("Starting Alice's server...")
    public_key, private_key = generate_keys()
    e, n = public_key
    d, n = private_key
    
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(1)
    print("Alice is waiting for Bob to connect...")
    
    # Accept connection from Bob
    client_socket, address = server_socket.accept()
    print(f"Bob connected from {address}")
    
    # Send public key to Bob
    client_socket.sendall(f"{e},{n}".encode())
    print("Public key sent to Bob.")
    
    # Receive ciphertext from Bob
    ciphertext = int(client_socket.recv(4096).decode())
    print(f"Received ciphertext from Bob: {ciphertext}")
    
    # Decrypt the ciphertext
    plaintext = pow(ciphertext, d, n)
    decrypted_message = long_to_bytes(plaintext).decode()
    print(f"Decrypted message: {decrypted_message}")
    
    # Close the connection
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    try:
        alice_server()
    except Exception as e:
        print(f"An error occurred in Alice's server: {e}")