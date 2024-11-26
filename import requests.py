import requests
import time
from rich.console import Console
from rich.panel import Panel
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as imageio
import os

# Fonction pour récupérer les infos publiques de GitHub d'un utilisateur
def fetch_github_info(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur HTTP {response.status_code}: {response.text}")
        return None

# Fonction pour générer un GIF à partir des informations GitHub
def generate_terminal_gif(username, output_file="terminal.gif"):
    console = Console()
    frames = []
    width, height = 600, 240

    # Récupérer les infos GitHub publiques
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
        f"🔗 Profile: {github_info['html_url']}",
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
    imageio.imwrite(output_file, frames, duration=1)
    console.print(Panel(f"[green]GIF créé avec succès : {output_file}"))

# Demander le nom d'utilisateur GitHub
username = "Etienne-VERSCHUERE"

# Générer le GIF
generate_terminal_gif(username, "terminal.gif")
