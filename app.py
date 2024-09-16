from flask import Flask, render_template, request
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # Récupérer les valeurs des sliders
    values = [
        float(request.form['slider1']),
        float(request.form['slider2']),
        float(request.form['slider3']),
        float(request.form['slider4']),
        float(request.form['slider5']),
        float(request.form['slider6']),
        float(request.form['slider7']),
        float(request.form['slider8']),
        float(request.form['slider9'])
    ]

    # Récupérer les titres des critères, avec une valeur par défaut si non fourni
    labels = [
        request.form['title1'] if request.form['title1'] else 'Critère 1',
        request.form['title2'] if request.form['title2'] else 'Critère 2',
        request.form['title3'] if request.form['title3'] else 'Critère 3',
        request.form['title4'] if request.form['title4'] else 'Critère 4',
        request.form['title5'] if request.form['title5'] else 'Critère 5',
        request.form['title6'] if request.form['title6'] else 'Critère 6',
        request.form['title7'] if request.form['title7'] else 'Critère 7',
        request.form['title8'] if request.form['title8'] else 'Critère 8',
        request.form['title9'] if request.form['title9'] else 'Critère 9'
    ]
    
    # Création du radar chart avec Plotly
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=labels,
                fill='toself',
                name='Évaluation'
            )
        ]
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=False
    )
    
    # Enregistrer le graphique en tant qu'image
    img_path = "static/images/radar_chart.png"
    pio.write_image(fig, img_path)

    return render_template('index.html', image_path=img_path, values=values)

if __name__ == '__main__':
    app.run()
