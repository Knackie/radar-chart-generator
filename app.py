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
    
    n_categories = len(categories)

    # Valeurs saisies pour les critères
    values = [adhesion, confiance, prise_decision, changement, criticite, livraison, taille_equipe, experience, acces]
    values += values[:1]  # Boucler pour fermer le radar chart

    # Calcul des angles pour chaque critère
    angles = [n / float(n_categories) * 2 * pi for n in range(n_categories)]
    angles += angles[:1]

    # Création du radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Couleurs dégradées plus marquantes pour les zones
    # Zone Agile (0-4) en gris très foncé
    ax.fill_between(np.linspace(0, 2 * pi, 100), 0, 4, color='dimgray', alpha=0.6)
    # Zone Hybride (4-8) en gris moyen
    ax.fill_between(np.linspace(0, 2 * pi, 100), 4, 8, color='silver', alpha=0.4)
    # Zone Prédictive (8-10) en blanc
    ax.fill_between(np.linspace(0, 2 * pi, 100), 8, 10, color='white', alpha=0.4)

    # Dessiner le radar chart avec les valeurs
    ax.fill(angles, values, color='b', alpha=0.25)
    ax.plot(angles, values, color='b', linewidth=2)

    # Configuration des axes (échelle de 0 à 10)
    ax.set_ylim(0, 10)
    ax.set_yticks(range(1, 11))  # Afficher les cercles de 1 à 10
    ax.set_yticklabels([str(i) for i in range(1, 11)])  # Afficher les labels des cercles
    ax.set_xticks([])  # Retirer les labels du diagramme

    # Ajouter les titres "Agile", "Hybride", "Prédictive" au bord du cercle
    ax.text(np.radians(45), 4.2, 'Agile', horizontalalignment='center', verticalalignment='center', size=14)
    ax.text(np.radians(45), 8.2, 'Hybride', horizontalalignment='center', verticalalignment='center', size=14)
    ax.text(np.radians(45), 10.2, 'Prédictive', horizontalalignment='center', verticalalignment='center', size=14)

    # Sauvegarde de l'image dans un buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Fermer la figure pour libérer la mémoire
    plt.close(fig)

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
