import os
import socket
import threading

# Server configuration
HOST = socket.gethostname()
PORT = 9999
LOG_FILE = "server_log.txt"
clients = {}  # Dictionary to store client connections

def log_message(message):
    with open(LOG_FILE, "a") as log:
        log.write(message + "\n")
    print(message)

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    while True:
        try:
            request = client_socket.recv(1024).decode()
            if not request:
                break

            log_message(f"Received from {client_address}: {request}")
            response = process_request(request, client_socket)
            client_socket.send(response.encode())
        
        except Exception as e:
            print(f"Error handling client {client_address}: {e}")
            break
    
    client_socket.close()
    print(f"Connection closed for {client_address}")

def process_request(client_socket, data):
    parts = data.split()
    command = parts[0].upper()

    #1
    if command == "STORE" and len(parts) > 2:
        filename, data = parts[1], parts[2]
        with open(filename, "w") as f:
            f.write(data)
        return "File stored successfully."
        pass

    #2
    elif command == "RETRIEVE" and len(parts) == 2:
        filename = parts[1]
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = f.read()
            client_socket.sendall(data.encode())  # Send file data
            return f"File '{filename}' sent successfully."
        else:
            return "File not found."

    #3
    elif command in ["ADD", "MULTIPLY", "DIVIDE", "SUBTRACT"] and len(parts) == 3:
        try:
            num1, num2 = float(parts[1]), float(parts[2])
            if command == "ADD":
                return f"RESULT {num1 + num2}"
            elif command == "MULTIPLY":
                return f"RESULT {num1 * num2}"
            elif command == "DIVIDE":
                return f"RESULT {num1 / num2}" if num2 != 0 else "ERROR: Division by zero"
            elif command == "SUBTRACT":
                return f"RESULT {num1 - num2}"
        except ValueError:
            return "ERROR: Invalid numbers."

    #4
    elif command == "MESSAGE" and len(parts) > 2:
        pass

    return "ERROR: Invalid command."

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    startup_message = f"Server listening on port {PORT}"
    log_message(startup_message)
    print(startup_message)

    while True:
        client_socket, client_address = server.accept()
        username = client_socket.recv(1024).decode()
        clients[username] = client_socket
        
        connection_msg = f"{username} connected from {client_address}"
        log_message(connection_msg)
        print(connection_msg)

        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    start_server()
