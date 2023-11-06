from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

def send_to_printer(ip, port, zpl_command):
    try:
        # Création d'un socket TCP/IP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((ip, port))
            sock.sendall(zpl_command.encode('utf-8'))
            # Fermeture du socket se fait automatiquement en sortant du bloc with
    except ConnectionError as e:
        return False, str(e)
    return True, "Commande envoyée avec succès."

@app.route('/print_label', methods=['POST'])
def print_label():
    # Récupération de l'adresse IP de l'imprimante et du ZPL depuis la requête
    data = request.json
    ip = data.get('ip')
    port = data.get('port', 9100)  # Port par défaut pour les imprimantes Zebra
    zpl_command = data.get('zpl')

    if not ip or not zpl_command:
        return jsonify({'error': 'IP et commande ZPL sont requis'}), 400

    # Envoi de la commande ZPL à l'imprimante
    success, message = send_to_printer(ip, port, zpl_command)

    if success:
        return jsonify({'message': message}), 200
    else:
        return jsonify({'error': message}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5698, debug=True)  
