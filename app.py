from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import numpy as np
from math import pi, cos, sin
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
    
    # Catégories pour le cercle externe
    category_labels = ['Culture', 'Projet', 'Équipe']
    category_boundaries = [0, 3, 6, 9]  # Limites des catégories

    n_categories = len(categories)

    # Valeurs saisies pour les critères
    values = [adhesion, confiance, prise_decision, changement, criticite, livraison, taille_equipe, experience, acces]
    values += values[:1]  # Boucler pour fermer le radar chart

    # Calcul des angles pour chaque critère
    angles = [n / float(n_categories) * 2 * pi for n in range(n_categories)]
    angles += angles[:1]

    # Création du radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Dessiner le radar chart
    ax.fill(angles, values, color='b', alpha=0.25)
    ax.plot(angles, values, color='b', linewidth=2)

    # Configuration des axes
    ax.set_yticklabels([])  # Masquer les étiquettes radiales
    ax.set_xticks([])  # Masquer les labels dans le diagramme

    # Ajouter les labels des critères dans le cercle externe des critères
    criteria_radius = 1.2
    for i, angle in enumerate(angles[:-1]):
        x = 0.5 + criteria_radius * cos(angle) / 2  # Calcul dans les coordonnées de la figure
        y = 0.5 + criteria_radius * sin(angle) / 2
        ax.annotate(categories[i], (x, y), xycoords='figure fraction', ha='center', va='center', size=12)

    # Ajouter les labels des catégories dans le cercle externe des catégories
    category_radius = 1.4
    for i in range(len(category_labels)):
        start_idx = category_boundaries[i]
        end_idx = category_boundaries[i + 1] if i + 1 < len(category_boundaries) else len(categories)

        # Calcul de l'angle moyen pour positionner les labels des catégories
        mid_angle = np.mean([angles[start_idx], angles[end_idx - 1]])
        x = 0.5 + category_radius * cos(mid_angle) / 2  # Calcul dans les coordonnées de la figure
        y = 0.5 + category_radius * sin(mid_angle) / 2
        ax.annotate(category_labels[i], (x, y), xycoords='figure fraction', ha='center', va='center', size=14,
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
