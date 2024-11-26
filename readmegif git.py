


import time
from rich.console import Console
from rich.panel import Panel
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as imageio
import os
from dotenv import load_dotenv
import requests
# Charger les variables d'environnement
load_dotenv()

# Fonction pour récupérer les informations GitHub
def fetch_github_info(username):
    """Récupère les informations du profil GitHub."""
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # Chargez le token depuis .env
    print("GitHub Token:", os.getenv("GITHUB_TOKEN"))

    headers = {"Authorization": f"token {'GITHUB_TOKEN'}"}
    url = f"https://api.github.com/users/{username}"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return {
            "name": data.get("name", "N/A"),
            "bio": data.get("bio", "N/A"),
            "public_repos": data.get("public_repos", 0),
            "followers": data.get("followers", 0),
            "following": data.get("following", 0),
            "profile_url": data.get("html_url", ""),
        }
    else:
        print(f"Erreur : {response.status_code} - {response.text}")
        return None

# Fonction pour générer le GIF simulant un terminal
def generate_terminal_gif(username, output_file="terminal.gif"):
    console = Console()
    frames = []
    width, height = 320, 240

    # Récupérer les infos GitHub
    github_info = fetch_github_info(username)
    if not github_info:
        console.print("[red]Erreur lors de la récupération des infos GitHub.")
        return

    # Informations à afficher
    terminal_lines = [
        f"💻 Welcome to {github_info['name']}'s Terminal",
        "-----------------------------------",
        f"👤 Name: {github_info['name']}",
        f"📖 Bio: {github_info['bio']}",
        f"📚 Public Repos: {github_info['public_repos']}",
        f"👥 Followers: {github_info['followers']}",
        f"➡️ Following: {github_info['following']}",
        f"🔗 Profile: {github_info['profile_url']}",
    ]

    # Générer les cadres pour chaque ligne progressivement
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    y_offset = 10
    for line in terminal_lines:
        draw.text((10, y_offset), line, font=font, fill=(255, 255, 255))
        y_offset += 15
        frames.append(img.copy())  # Ajouter chaque étape à l'animation

    # Sauvegarder en GIF
    imageio.imwrite(output_file, frames, duration=0.5)
    console.print(Panel(f"[green]GIF créé avec succès : {output_file}"))

# Hébergement sur IMGBB (optionnel)
def upload_to_imgbb(file_path):
    """Héberge une image ou un GIF sur IMGBB."""
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")  # Chargez la clé API depuis .env
    if not IMGBB_API_KEY:
        print("Erreur : clé API IMGBB manquante.")
        return None

    with open(file_path, "rb") as file:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": 'IMGBB_API_KEY'},
            files={"image": file},
        )
    if response.status_code == 200:
        url = response.json()["data"]["url"]
        print(f"Lien de l'image : {url}")
        return url
    else:
        print("Erreur lors du téléchargement sur IMGBB")
        return None

# Exécution
USERNAME = "Etienne-VERSCHUERE"  # Remplacez par votre nom d'utilisateur GitHub
generate_terminal_gif(USERNAME, "terminal.gif")
gif_url = upload_to_imgbb("terminal.gif")
if gif_url:
    print(f"Ajoutez cette URL dans votre README : ![Terminal]({gif_url})")
