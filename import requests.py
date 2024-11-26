import requests
from PIL import Image, ImageDraw, ImageFont
import imageio.v3 as imageio
from rich.console import Console
from rich.panel import Panel

# Fonction pour récupérer les infos publiques de GitHub
def fetch_github_info(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur HTTP {response.status_code}: {response.text}")
        return None

# Fonction pour générer un GIF avec des options personnalisables
def generate_terminal_gif(username, output_file="terminal.gif", width=400, height=300, font_size=16, text_colors=None):
    console = Console()
    frames = []

    # Récupérer les infos GitHub publiques
    github_info = fetch_github_info(username)
    if not github_info:
        console.print("[red]Erreur lors de la récupération des infos GitHub.")
        return

    # Informations à afficher
    terminal_lines = [
        f"💻 Welcome to {github_info['name']} 's Terminal",
        "-----------------------------------",
        f"👤 Name: {github_info['name']}",
        f"📖 Bio: {github_info['bio']}",
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

    # Créer chaque cadre (image) pour l'animation
    img = Image.new("RGB", (width, height), color=(0, 0, 0))  # Image de fond noire
    draw = ImageDraw.Draw(img)

    y_offset = 10
    for i, line in enumerate(terminal_lines):
        # Dessiner le texte ligne par ligne avec des couleurs personnalisées
        color = text_colors[i] if i < len(text_colors) else "white"  # Utiliser la couleur correspondante ou blanc
        draw.text((10, y_offset), line, font=font, fill=color)
        y_offset += font_size + 7  # Ajuster l'espacement vertical

        # Ajouter une copie de l'image dans les frames
        frames.append(img.copy())

    # Sauvegarder en GIF
    imageio.imwrite(output_file, frames, duration=0.5)
    console.print(Panel(f"[green]GIF créé avec succès : {output_file}"))

# Demander le nom d'utilisateur GitHub
username = "Etienne-VERSCHUERE"
# Personnalisation de la taille, des couleurs et du fichier de sortie
generate_terminal_gif(
    username=username,
    output_file="terminal.gif",
    width=600,                # Largeur de l'image
    height=400,               # Hauteur de l'image
    font_size=20,             # Taille de la police
    text_colors=["cyan", "yellow", "green", "magenta", "blue", "red", "white", "orange"]  # Couleurs personnalisées
)

