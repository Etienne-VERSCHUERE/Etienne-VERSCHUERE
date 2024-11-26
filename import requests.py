import requests
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as imageio
import os
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

# Récupérer le token depuis les variables d'environnement
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

if not IMGBB_API_KEY:
    raise ValueError("Token API ImgBB non trouvé. Vérifie le fichier .env.")

# Clé API ImgBB (remplace-la par ta propre clé API)
IMGBB_API_KEY = "fd156800917f5e737974881bebfa0fb1"

# Fonction pour récupérer les infos publiques de GitHub
def fetch_github_info(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur HTTP {response.status_code}: {response.text}")
        return None

# Fonction pour générer un GIF
def generate_terminal_gif(username, output_file="terminal.gif", width=400, height=300, font_size=16, text_colors=None):
    github_info = fetch_github_info(username)
    if not github_info:
        raise ValueError("Erreur lors de la récupération des infos GitHub.")

    boot_messages = [
        "[OK] Initializing system services...",
        "[OK] Starting network configuration...",
        "[OK] Mounting filesystems...",
        "[OK] Loading kernel modules...",
        "[OK] Starting SSH daemon...",
        "[OK] Syncing system clock...",
        "[OK] Checking disk space...",
        "[OK] System ready."]
    terminal_lines = [
        f"💻 Welcome to {github_info['name']} 's Terminal",
        "-----------------------------------",
        f"👤 Name: {github_info['name']}",
        f"📖 Bio: {github_info.get('bio', 'N/A')}",
        f"📚 Public Repos: {github_info['public_repos']}",
        f"👥 Followers: {github_info['followers']}",
        f"➡️ Following: {github_info['following']}",
        f"🔗 Profile: {github_info['html_url']}",
    ]

    # Couleurs par défaut si aucune couleur n'est spécifiée
    if not text_colors:
        text_colors = ["white"] * len(terminal_lines)

    # Charger une police de texte
    try:
        font = ImageFont.truetype("SourceCodePro-Regular.ttf", font_size)
    except:
        font = ImageFont.load_default()

    frames = []
    img = Image.new("RGB", (width, height), color=(0, 0, 0))  # Fond noir
    draw = ImageDraw.Draw(img)

    y_offset = 10
    for i, line in enumerate(terminal_lines):
        color = text_colors[i] if i < len(text_colors) else "white"
        draw.text((10, y_offset), line, font=font, fill=color)
        y_offset += font_size + 7  # Espacement entre les lignes
        frames.append(img.copy())  # Ajout du cadre à l'animation

    imageio.imwrite(output_file, frames, duration=0.5)  # Sauvegarder en GIF
# Simuler le démarrage Unix
    y_offset = 10
    for i, message in enumerate(boot_messages):
        draw.text((10, y_offset), message, font=font, fill="green")
        y_offset += font_size + 5
        frames.append(img.copy())
          # Simuler un délai pour chaque message

    # Ajouter une pause après le démarrage
    for _ in range(5):
        frames.append(img.copy())

# Fonction pour envoyer le GIF à ImgBB
def upload_to_imgbb(file_path):
    with open(file_path, "rb") as file:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": IMGBB_API_KEY},
            files={"image": file},
        )
    if response.status_code == 200:
        return response.json()["data"]["url"]
    else:
        print(f"Erreur ImgBB {response.status_code}: {response.text}")
        return None


# Programme principal
if __name__ == "__main__":
    # Nom d'utilisateur GitHub à récupérer
    username = "Etienne-VERSCHUERE"  # Remplace par un autre nom si nécessaire

    try:
        # Générer le GIF
        print("Génération du GIF...")
        generate_terminal_gif(
            username=username,
            output_file="terminal.gif",
            width=850,                # Largeur du GIF
            height=400,               # Hauteur du GIF
            font_size=20,             # Taille de la police
            text_colors=["cyan", "yellow", "green", "magenta", "blue", "red", "white", "orange"]
        )
        print("GIF généré avec succès : terminal.gif")

        # Envoyer le GIF sur ImgBB
        print("Envoi sur ImgBB...")
        gif_url = upload_to_imgbb("terminal.gif")
        if gif_url:
            print(f"GIF hébergé sur ImgBB : {gif_url}")
        else:
            print("Erreur lors de l'envoi du GIF sur ImgBB.")
    except ValueError as e:
        print(f"Erreur : {e}")
