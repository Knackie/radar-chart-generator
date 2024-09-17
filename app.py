from flask import Flask, render_template, request
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # Catégorie 1: Culture
    culture_values = [
        float(request.form['adhesion']),
        float(request.form['confiance']),
        float(request.form['prise_decision'])
    ]
    culture_labels = ['Adhésion', 'Confiance', 'Prise de décision']

    # Créer le radar chart avec Plotly
    fig = go.Figure()

    # Ajouter les données de la catégorie Culture
    fig.add_trace(go.Scatterpolar(
        r=culture_values,
        theta=culture_labels,
        fill='toself',
        name='Culture'
    ))

    # Configurer le layout du graphique
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=True
    )

    # Sauvegarder le graphique sous forme d'image
    img_path = "static/images/radar_chart.png"
    pio.write_image(fig, img_path)

    return render_template('index.html', image_path=img_path, values=culture_values)

if __name__ == '__main__':
    app.run(debug=True)
