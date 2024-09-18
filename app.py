from flask import Flask, render_template, request
import plotly.graph_objs as go
import plotly.io as pio
import math

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

    # Configure the layout of the radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=False,
    )

    # Divide the outer circle into 9 segments and position the labels
    n_criteria = 9
    angle_step = 360 / n_criteria
    radius = 1.15  # Adjust the radius for the outer circle (1.0 is the edge of the chart)

    # Create a list of positions around the outer circle for the criteria labels
    annotations = []
    for i, label in enumerate(all_labels):
        angle = angle_step * i
        angle_rad = math.radians(angle - 90)  # Adjust for correct start angle (start from top)

        # Calculate the x and y positions based on the angle and radius
        x = 0.5 + radius * math.cos(angle_rad)
        y = 0.5 + radius * math.sin(angle_rad)

        # Adjust text rotation for better alignment in each segment
        if 0 <= angle < 180:
            textangle = angle - 90
        else:
            textangle = angle + 90

        # Add the annotation for each criterion
        annotations.append(
            dict(
                x=x, y=y,
                xref="paper", yref="paper",
                text=label,
                showarrow=False,
                font=dict(size=12),
                align="center",
                textangle=textangle  # Rotate text to align with the circle
            )
        )

    # Add the criteria labels as annotations in the external circle
    fig.update_layout(annotations=annotations)

    # Save the chart as an image
    img_path = "static/images/radar_chart.png"
    pio.write_image(fig, img_path)

    return render_template('index.html', image_path=img_path, values=all_values)

if __name__ == '__main__':
    app.run(debug=True)
