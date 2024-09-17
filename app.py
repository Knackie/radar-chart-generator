from flask import Flask, render_template, request
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # Collect values from the form (Culture, Projet, Équipe)
    
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

    # Combine all values and labels into a single form
    all_values = culture_values + projet_values + equipe_values
    all_labels = culture_labels + projet_labels + equipe_labels

    # Create radar chart with Plotly
    fig = go.Figure()

    # Add a single trace that connects all criteria from all categories
    fig.add_trace(go.Scatterpolar(
        r=all_values,
        theta=all_labels,
        fill='toself',
        name='Critères'
    ))

    # Add category names as annotations around the radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=True,
        annotations=[
            dict(
                x=0.5, y=1.2,  # Adjust positioning
                xref="paper", yref="paper",
                text="Catégorie 1 : Culture",
                showarrow=False
            ),
            dict(
                x=1.2, y=0.5,  # Adjust positioning
                xref="paper", yref="paper",
                text="Catégorie 2 : Projet",
                showarrow=False
            ),
            dict(
                x=0.5, y=-0.2,  # Adjust positioning
                xref="paper", yref="paper",
                text="Catégorie 3 : Équipe",
                showarrow=False
            )
        ]
    )

    # Save the chart as an image
    img_path = "static/images/radar_chart.png"
    pio.write_image(fig, img_path)

    return render_template('index.html', image_path=img_path, values=all_values)

if __name__ == '__main__':
    app.run(debug=True)
