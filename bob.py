import socket
from Crypto.Util.number import bytes_to_long

# Bob Client
def bob_client():
    print("Starting Bob's client...")
    
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to Alice...")
    client_socket.connect(('localhost', 12345))
    print("Connected to Alice.")
    
    # Receive public key from Alice
    public_key_data = client_socket.recv(4096).decode()
    e, n = map(int, public_key_data.split(','))
    print(f"Received public key from Alice: (e={e}, n={n})")
    
    # Input plaintext message
    plaintext = input("Enter a message to encrypt: ")
    print(f"Encrypting message: {plaintext}")
    plaintext_int = bytes_to_long(plaintext.encode())
    
    # Encrypt the plaintext
    ciphertext = pow(plaintext_int, e, n)
    print(f"Ciphertext: {ciphertext}")
    
    # Send ciphertext to Alice
    client_socket.sendall(str(ciphertext).encode())
    print("Ciphertext sent to Alice.")
    
    # Close the connection
    client_socket.close()

if __name__ == "__main__":
    try:
        bob_client()
    except Exception as e:
        print(f"An error occurred in Bob's client: {e}")