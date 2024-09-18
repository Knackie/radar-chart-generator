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
    categories = ['Culture', 'Projet', 'Équipe']  # Noms des catégories
    category_bounds = [(0, 3), (3, 6), (6, 9)]  # Index des critères par catégorie
    criteria = [
        'Adhésion', 'Confiance', 'Prise de décision',  # Culture
        'Changement', 'Criticité', 'Livraison',  # Projet
        'Taille de l\'équipe', 'Expérience', 'Accès'  # Équipe
    ]
    
    # Valeurs saisies pour les critères
    values = [adhesion, confiance, prise_decision, changement, criticite, livraison, taille_equipe, experience, acces]
    values += values[:1]  # Boucler pour fermer le radar chart

    # Calcul des angles pour chaque critère
    n_criteria = len(criteria)
    angles = [n / float(n_criteria) * 2 * pi for n in range(n_criteria)]
    angles += angles[:1]

    # Définir des couleurs par catégorie
    colors_by_category = ['#FF9999', '#99CCFF', '#99FF99']  # Rouge, bleu, vert

    # Création du radar chart
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    # Couleurs dégradées pour les zones (Agile, Hybride, Prédictive)
    ax.fill_between(np.linspace(0, 2 * pi, 100), 0, 4, color='dimgray', alpha=0.6)  # Agile en gris foncé
    ax.fill_between(np.linspace(0, 2 * pi, 100), 4, 8, color='silver', alpha=0.4)  # Hybride en gris moyen
    ax.fill_between(np.linspace(0, 2 * pi, 100), 8, 10, color='white', alpha=0.4)  # Prédictive en blanc

    # Dessiner le radar chart avec les valeurs
    ax.fill(angles, values, color='b', alpha=0.25)
    ax.plot(angles, values, color='b', linewidth=2)

    # --- Ajustement pour que les couleurs suivent les traits ---
    # Déplacer les traits et les zones colorées des critères de 20°
    for idx, (start, end) in enumerate(category_bounds):
        color = colors_by_category[idx]
        for i in range(start, end):
            adjusted_angle_start = angles[i] + np.radians(20)  # Décalage de 20°
            adjusted_angle_end = angles[i + 1] + np.radians(20)  # Décalage de 20°
            ax.fill_between(np.linspace(adjusted_angle_start, adjusted_angle_end, 100), 10, 11, color=color, alpha=0.4)

        # Pour les catégories dans le cercle 12
        adjusted_angle_start = angles[start] + np.radians(20)  # Début de la section avec décalage
        adjusted_angle_end = angles[end] + np.radians(20)  # Fin de la section avec décalage
        ax.fill_between(np.linspace(adjusted_angle_start, adjusted_angle_end, 100), 11, 12, color=color, alpha=0.4)

    # Configuration des axes (échelle de 0 à 10)
    ax.set_ylim(0, 12)  # Ajustement pour inclure les cercles externes
    ax.set_yticks(range(1, 11))  # Afficher les cercles de 1 à 10 uniquement pour les valeurs
    ax.set_yticklabels([str(i) for i in range(1, 11)])  # Afficher les labels des cercles
    ax.set_xticks([])  # Retirer les labels du diagramme

    # --- Déplacer les traits des critères (cercle 11) de 20° ---
    for i, angle in enumerate(angles[:-1]):
        adjusted_angle = angle + np.radians(20)  # Décalage de 20° en radians
        ax.plot([adjusted_angle, adjusted_angle], [10, 11], color='black', linewidth=2)  # Lignes entre 10 et 11

    # --- Déplacer les traits des catégories (cercle 12) de 20° ---
    for start, end in category_bounds:
        mid_angle = np.mean(angles[start:end])
        adjusted_angle = mid_angle + np.radians(20)  # Décalage de 20° en radians
        ax.plot([adjusted_angle, adjusted_angle], [11, 12], color='black', linewidth=2)  # Lignes entre 11 et 12

    # --- Ajouter les valeurs des critères dans la zone 11 ---
    for i, angle in enumerate(angles[:-1]):
        rotation_angle = np.degrees(angle) + 90  # Tourner chaque critère de 90°

        # Appliquer une rotation spécifique pour le critère "Adhésion"
        if criteria[i] == 'Adhésion':
            rotation_angle += 180  # Tourner "Adhésion" de 270° au total (90° + 180°)

        ha = 'center'  # Centrer horizontalement

        # Ajuster la rotation pour les critères
        if 90 < rotation_angle < 270:  # Ajuster pour les textes au bas du cercle
            rotation_angle += 180

        # Ajouter le texte du critère avec l'angle correct
        ax.text(angle, 11, criteria[i], rotation=rotation_angle, ha=ha, va='center', size=10, weight='bold')

    # --- Ajouter les catégories dans la zone 12 ---
    for i, (start, end) in enumerate(category_bounds):
        mid_angle = np.mean(angles[start:end])
        rotation_angle = np.degrees(mid_angle) + 90  # Ajouter 90° de rotation pour chaque catégorie
        ha = 'center'  # Centrer horizontalement
        if 90 < rotation_angle < 270:  # Ajuster pour les textes au bas du cercle
            rotation_angle += 180
        ax.text(mid_angle, 12, categories[i], rotation=rotation_angle, ha=ha, va='center', size=12, weight='bold')

    # Sauvegarde de l'image dans un buffer
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Fermer la figure pour libérer la mémoire
    plt.close(fig)

    return send_file(img, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
