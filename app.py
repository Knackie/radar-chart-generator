from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import numpy as np
from math import pi
import io

app = Flask(__name__)

# Route principale pour afficher le formulaire
@app.route('/')
def index():
    return render_template('index.html')

# Route pour générer le radar chart
@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # Récupérer les valeurs des critères via le formulaire
    adhesion = float(request.form['adhesion'])
    confiance = float(request.form['confiance'])
    prise_decision = float(request.form['prise_decision'])

    changement = float(request.form['changement'])
    criticite = float(request.form['criticite'])
    livraison = float(request.form['livraison'])

    taille_equipe = float(request.form['taille_equipe'])
    experience = float(request.form['experience'])
    acces = float(request.form['acces'])

    # Les catégories et leurs critères
    categories = [
        'Adhésion', 'Confiance', 'Prise de décision',  # Culture
        'Changement', 'Criticité', 'Livraison',  # Projet
        'Taille de l\'équipe', 'Expérience', 'Accès'  # Équipe
    ]
    
    # Diviser en catégories pour le cercle externe
    category_labels = ['Culture', 'Projet', 'Équipe']
    category_boundaries = [0, 3, 6, 9]  # Les limites des catégories

    n_categories = len(categories)

    # Valeurs saisies pour les critères
    values = [adhesion, confiance, prise_decision, changement, criticite, livraison, taille_equipe, experience, acces]
    values += values[:1]  # Boucler pour fermer le radar chart

    # Calcul des angles pour chaque critère
    angles = [n / float(n_categories) * 2 * pi for n in range(n_categories)]
    angles += angles[:1]

    # Création du radar chart
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Dessiner le radar chart
    ax.fill(angles, values, color='b', alpha=0.25)
    ax.plot(angles, values, color='b', linewidth=2)

    # Configuration des axes
    ax.set_yticklabels([])  # Masquer les étiquettes radiales
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=10)

    # Ajout d'un cercle externe segmenté avec des labels de catégories
    circle_radius = 1.2
    for i, angle in enumerate(angles[:-1]):
        x = circle_radius * np.cos(angle)
        y = circle_radius * np.sin(angle)

        rotation = np.degrees(angle) if np.degrees(angle) < 180 else np.degrees(angle) + 180
        ha = 'left' if np.degrees(angle) < 180 else 'right'

        ax.text(x, y, categories[i], horizontalalignment=ha, size=12, verticalalignment='center', 
                rotation=rotation, rotation_mode='anchor')

    # Dessiner le cercle externe segmenté pour les catégories
    for i in range(len(category_labels)):
        start_idx = category_boundaries[i]
        end_idx = category_boundaries[i + 1] if i + 1 < len(category_boundaries) else len(categories)

        mid_angle = np.mean([angles[start_idx], angles[end_idx - 1]])
        x = (circle_radius + 0.2) * np.cos(mid_angle)
        y = (circle_radius + 0.2) * np.sin(mid_angle)

        ax.text(x, y, category_labels[i], horizontalalignment='center', size=14, verticalalignment='center', 
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

    # Sauvegarde de l'image dans un buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Fermer la figure pour libérer la mémoire
    plt.close(fig)

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
