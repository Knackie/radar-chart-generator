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
    ax.set_ylim(0, 10)  # Échelle du radar chart de 0 à 10
    ax.set_yticks(range(1, 11))  # Cercles de 1 à 10
    ax.set_yticklabels([str(i) for i in range(1, 11)])  # Affichage des unités 1 à 10
    ax.set_xticks([])  # Masquer les labels dans le diagramme

    # --- Ajout des labels pour les zones "Agile", "Hybride" et "Prédictive" ---
    ax.text(0, 2, 'Agile', horizontalalignment='center', verticalalignment='center', size=14, bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(0, 6, 'Hybride', horizontalalignment='center', verticalalignment='center', size=14, bbox=dict(facecolor='white', edgecolor='black'))
    ax.text(0, 9, 'Prédictive', horizontalalignment='center', verticalalignment='center', size=14, bbox=dict(facecolor='white', edgecolor='black'))

    # Ajustement du rayon des cercles externes
    criteria_radius = 11  # Rayon pour placer les critères en dehors du radar chart
    category_radius = 13  # Rayon pour placer les catégories en dehors du radar chart

    # Ajouter les labels des critères dans le cercle externe des critères
    for i, angle in enumerate(angles[:-1]):
        # Calcul des positions en coordonnées polaires
        x = criteria_radius * np.cos(angle)
        y = criteria_radius * np.sin(angle)

        ax.text(x, y, categories[i], horizontalalignment='center', verticalalignment='center', size=12)

    # Ajouter les labels des catégories dans le cercle externe des catégories
    for i in range(len(category_labels)):
        start_idx = category_boundaries[i]
        end_idx = category_boundaries[i + 1] if i + 1 < len(category_boundaries) else len(categories)

        # Calculer l'angle moyen pour les catégories
        mid_angle = np.mean([angles[start_idx], angles[end_idx - 1]])

        # Calcul des positions en coordonnées polaires pour les catégories
        x = category_radius * np.cos(mid_angle)
        y = category_radius * np.sin(mid_angle)

        ax.text(x, y, category_labels[i], horizontalalignment='center', verticalalignment='center', size=14, 
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
