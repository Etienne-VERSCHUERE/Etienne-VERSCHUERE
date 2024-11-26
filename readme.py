import time
from rich.console import Console
from rich.panel import Panel
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as imageio
import os
from dotenv import load_dotenv

# Charger la clé IMGBB depuis le fichier .env
load_dotenv()
IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# Fonction pour simuler un terminal
def generate_terminal_gif(output_file="terminal.gif"):
    console = Console()
    frames = []
    width, height = 320, 240

    # Informations à afficher
    terminal_lines = [
        "💻 Welcome to Etienne-Verschuere's Terminal",
        "-----------------------------------",
        "👤 Name: Verschuere Etienne",
        "📧 Email: etienne.verschuere@laplateforme.io",
        "🌟 GitHub:https://github.com/Etienne-VERSCHUERE ",
        "🚀 Projects: Morpion AI, Terminal Fun, Pentesting",
        "🎯 Skills: Python, Hacking, Humor ",
    ]

    # Générer les cadres pour chaque ligne
    img = Image.new("RGB", (width, height), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    y_offset = 10
    for line in terminal_lines:
        draw.text((10, y_offset), line, font=font, fill=(255, 255, 255))
        y_offset += 15

        # Ajouter le cadre à la liste
        frames.append(img.copy())

    # Sauvegarder en GIF
    imageio.imwrite(output_file, frames, duration=0.5)
    console.print(Panel(f"[green]GIF créé avec succès : {output_file}"))

# Fonction pour héberger le GIF sur IMGBB
def upload_to_imgbb(file_path):
    import requests

    with open(file_path, "rb") as file:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": IMGBB_API_KEY},
            files={"image": file},
        )
    if response.status_code == 200:
        url = response.json()["data"]["url"]
        print(f"Lien de l'image : {url}")
        return url
    else:
        print("Erreur lors du téléchargement sur IMGBB")
        return None


# Générer le terminal et héberger
generate_terminal_gif("terminal.gif")
gif_url = upload_to_imgbb("terminal.gif")
print(f"Ajoutez cette URL dans votre README : ![Terminal](gif_url)")
