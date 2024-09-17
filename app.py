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

    # Configure the layout of the chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=False,  # Hide the legend since we are adding custom annotations
    )

    # Add category names as annotations to simulate a surrounding circle
    fig.update_layout(
        annotations=[
            dict(
                x=0.5, y=1.3,  # Adjust positioning at the top of the chart
                xref="paper", yref="paper",
                text="Catégorie 1 : Culture",
                showarrow=False,
                font=dict(size=14)
            ),
            dict(
                x=1.3, y=0.5,  # Adjust positioning at the right of the chart
                xref="paper", yref="paper",
                text="Catégorie 2 : Projet",
                showarrow=False,
                font=dict(size=14)
            ),
            dict(
                x=0.5, y=-0.3,  # Adjust positioning at the bottom of the chart
                xref="paper", yref="paper",
                text="Catégorie 3 : Équipe",
                showarrow=False,
                font=dict(size=14)
            ),
        ]
    )

    # Save the chart as an image
    img_path = "static/images/radar_chart.png"
    pio.write_image(fig, img_path)

    return render_template('index.html', image_path=img_path, values=all_values)

if __name__ == '__main__':
    app.run(debug=True)
