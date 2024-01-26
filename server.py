import socket
import threading

HOST = "127.0.0.1"
PORT = 1234  # we can use any number port between 0 and 65535
LISTENER_LIMIT = 5
active_clients = []  # list of all currently connected users.


# Function to listen to upcoming messages from a client
def listen_for_messages(client, username):
    while 1:
        message = client.recv(2048).decode("utf-8")
        if message != "":
            final_msg = f"{username}~{message}"
            send_message_to_all(final_msg)
        else:
            print(f"The message from the client {username} is empty")


# Function to send a message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())


# Function to send any new message to all the clients who are connected to this server.
def send_message_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)


# Function to handle client
def client_handler(client):
    # Server will listen for client message that will contain the username
    while 1:
        username = client.recv(2048).decode("utf-8")
        if username != "":
            active_clients.append((username, client))
            break
        else:
            print("Client user name is empty")
    threading.Thread(target=listen_for_messages, args=(client, username,)).start()


# main function
def main():
    # Creating the socket class object
    # AF_INET : we are going to use IPv4 adresses
    # SOCK_STREAM : we are going to use TCP - Transmission Control Protocol
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, PORT))
        print("Successfully connected to server")
    except:
        print(f"Unable to connect to host  {HOST} and to port {PORT}")

    # Set server limit
    server.listen(LISTENER_LIMIT)

    # This while loop will keep listening to client connections
    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")
        threading.Thread(target=client_handler, args=(client,)).start()


if __name__ == "__main__":
    main()
