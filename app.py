from flask import Flask, render_template, request
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # Category 1: Culture
    culture_values = [
        float(request.form['adhesion']),
        float(request.form['confiance']),
        float(request.form['prise_decision'])
    ]
    culture_labels = ['Adhésion', 'Confiance', 'Prise de décision']

    # Category 2: Projet
    projet_values = [
        float(request.form['changement']),
        float(request.form['criticite']),
        float(request.form['livraison'])
    ]
    projet_labels = ['Changement', 'Criticité', 'Livraison']

    # Category 3: Équipe
    equipe_values = [
        float(request.form['taille_equipe']),
        float(request.form['experience']),
        float(request.form['acces'])
    ]
    equipe_labels = ['Taille de l\'équipe', 'Expérience', 'Accès']

    # Create radar chart with Plotly
    fig = go.Figure()

    # Add Culture category data
    fig.add_trace(go.Scatterpolar(
        r=culture_values,
        theta=culture_labels,
        fill='toself',
        name='Culture'
    ))

    # Add Projet category data
    fig.add_trace(go.Scatterpolar(
        r=projet_values,
        theta=projet_labels,
        fill='toself',
        name='Projet'
    ))

    # Add Équipe category data
    fig.add_trace(go.Scatterpolar(
        r=equipe_values,
        theta=equipe_labels,
        fill='toself',
        name='Équipe'
    ))

    # Configure the layout of the chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=True
    )

    # Save the chart as an image
    img_path = "static/images/radar_chart.png"
    pio.write_image(fig, img_path)

    return render_template('index.html', image_path=img_path, values=culture_values + projet_values + equipe_values)

if __name__ == '__main__':
    app.run(debug=True)
