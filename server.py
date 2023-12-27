import socket
from os import environ, path, walk
from urllib.parse import quote
from flask import Flask, redirect, send_from_directory, request
import threading

GAMES_PATH = environ.get("GAMES", "/games")
IP = environ.get("IP", socket.gethostbyname(socket.gethostname()))
PUBLIC_PORT = int(environ.get("PUBLIC_PORT", "9997"))

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def ui():
        return '<form action="/send" method="POST"><input name="ip" placeholder="Switch\'s IP"/><button>Send!</button></form>'

    @app.route("/send", methods=["POST"])
    def send_to_ip():
        address = request.form.get("ip", "127.0.0.1")
        threading.Thread(target=lambda: do_thing(address)).start()
        return redirect("/")

    @app.route("/game/<path:game_path>")
    def game(game_path):
        return send_from_directory(GAMES_PATH, game_path)

    return app

def send_games(address_list, address):
    to_send = "\n".join(address_list) + "\n"
    length = len(to_send).to_bytes(4, "big")
    if to_send[:-1]:
        with socket.create_connection((address, 2000)) as client_socket:
            client_socket.send(length)
            client_socket.send(to_send.encode())

def discover_games(games_path):
    found_games = []
    for root, _, files in walk(games_path):
        found_games.extend([
            path.relpath(
                path.join(root, file),
                games_path
            )
            for file in files
            if file.split(".")[-1] in [
                "nsp",
                "nsz",
                "xci"
            ]
        ])
    return found_games

def do_thing(address):
    try:
        game_list = [f"{IP}:{PUBLIC_PORT}/game/{quote(game, safe='')}" for game in discover_games(GAMES_PATH)]
        send_games(game_list, address)
    except Exception as e:
        print(e)

def inf_loop():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 7777))

    while True:
        try:
            message, address = server_socket.recvfrom(1024)
            if message.strip().lower() == b"awoo-discovery":
                do_thing(address[0])
        except Exception as e:
            print(e)
