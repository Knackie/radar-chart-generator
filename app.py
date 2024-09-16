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

    # Récupérer les titres des critères
    labels = [
        request.form['title1'],
        request.form['title2'],
        request.form['title3'],
        request.form['title4'],
        request.form['title5'],
        request.form['title6'],
        request.form['title7'],
        request.form['title8'],
        request.form['title9']
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
    app.run(debug=True)
