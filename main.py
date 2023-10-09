from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# Dimensions de la toile
TOILE_LARGEUR = 250
TOILE_HAUTEUR = 250

# Taille des pixels
PIXEL_TAILLE = 20

# Initialiser la toile avec des pixels blancs
toile = [[(255, 255, 255) for _ in range(TOILE_LARGEUR)] for _ in range(TOILE_HAUTEUR)]

# Charger le canvas au démarrage de l'application s'il existe
try:
    with open('canvas.json', 'r') as f:
        toile = json.load(f)
except FileNotFoundError:
    # Si le fichier "canvas.json" n'existe pas, on le crée avec un canvas vide
    with open('canvas.json', 'w') as f:
        json.dump(toile, f)

@app.route('/')
def index():
    return render_template('canvas.html', toile=toile, taille=PIXEL_TAILLE)

def sauvegarder_canvas():
    global toile
    with open('canvas.json', 'w') as f:
        json.dump(toile, f)

@app.route('/placer_pixel', methods=['POST'])
def placer_pixel():
    global toile
    data = request.get_json(force=True)
    x = int(data['x'])
    y = int(data['y'])
    couleur = (int(data['r']), int(data['g']), int(data['b']))

    if 0 <= x < TOILE_LARGEUR and 0 <= y < TOILE_HAUTEUR:
        toile[y][x] = couleur
        sauvegarder_canvas()  # Appel à la fonction de sauvegarde automatique
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Coordonnées de pixel invalides.'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=20009)
    