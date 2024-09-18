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
            radialaxis=dict(visible=True, range=[0, 10]),
            angularaxis=dict(rotation=90)  # Start from the top of the chart
        ),
        showlegend=False,
    )

    # Variables for the circle external radius and divisions
    outer_radius = 1.2  # Slightly larger than the radar chart
    n_criteria = len(all_labels)
    angle_step = 360 / n_criteria

    # Add shapes for the external circle divided into 9 segments
    shapes = []
    for i in range(n_criteria):
        start_angle = i * angle_step - 90  # Adjust to start from the top
        end_angle = start_angle + angle_step
        
        # Convert angles to radians for the trigonometric functions
        start_angle_rad = math.radians(start_angle)
        end_angle_rad = math.radians(end_angle)
        
        # Draw each segment of the outer circle using line shapes
        shapes.append(dict(
            type="path",
            path=f"M {0.5 + outer_radius * math.cos(start_angle_rad)} {0.5 + outer_radius * math.sin(start_angle_rad)} "
                 f"A {outer_radius} {outer_radius} 0 0,1 {0.5 + outer_radius * math.cos(end_angle_rad)} {0.5 + outer_radius * math.sin(end_angle_rad)}",
            line=dict(color="Black", width=2),
            xref="paper", yref="paper"
        ))

    # Add the labels for each criterion in the corresponding section
    annotations = []
    for i, label in enumerate(all_labels):
        angle = (i * angle_step) - 90  # Adjust starting from top
        angle_rad = math.radians(angle)

        x = 0.5 + (outer_radius + 0.05) * math.cos(angle_rad)  # Move the label slightly outside the circle
        y = 0.5 + (outer_radius + 0.05) * math.sin(angle_rad)

        # Rotate the text for better readability
        textangle = angle if angle >= -90 and angle <= 90 else angle + 180

        annotations.append(
            dict(
                x=x, y=y,
                xref="paper", yref="paper",
                text=label,
                showarrow=False,
                font=dict(size=12),
                align="center",
                textangle=textangle
            )
        )

    # Update the layout with the external circle and labels
    fig.update_layout(
        shapes=shapes,
        annotations=annotations
    )

    # Save the chart as an image
    img_path = "static/images/radar_chart.png"
    pio.write_image(fig, img_path)

    return render_template('index.html', image_path=img_path, values=all_values)

if __name__ == '__main__':
    app.run(debug=True)
