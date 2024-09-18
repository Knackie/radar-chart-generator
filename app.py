import matplotlib.pyplot as plt
import numpy as np
import io
from flask import Flask, render_template, request, send_file
import matplotlib.colors as mcolors

app = Flask(__name__)

# Helper function to create radar chart
def radar_chart(values, categories, criteria, angles, category_bounds):
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

    # Set the background color for the entire plot
    ax.set_facecolor('white')

    # Draw one axe per variable and add labels
    ax.plot(angles, values, linewidth=2, linestyle='solid')
    ax.fill(angles, values, color='blue', alpha=0.25)

    # Draw the colored zones
    ax.fill_between(angles, 0, 4, color='lightgray', alpha=0.4)
    ax.fill_between(angles, 4, 8, color='darkgray', alpha=0.4)
    ax.fill_between(angles, 8, 10, color='lightgray', alpha=0.4)

    # Zone 11-12 for criteria
    for i, angle in enumerate(angles[:-1]):
        ax.plot([angle, angle], [10, 11], color='black', linewidth=2)

    # Zone 12 for categories
    for start, end in category_bounds:
        mid_angle = np.mean(angles[start:end])
        ax.plot([mid_angle, mid_angle], [11, 12], color='black', linewidth=2)

    # Draw circle 12 for outermost categories
    ax.set_ylim(0, 12)

    # Hide the frame
    ax.spines['polar'].set_visible(False)

    # Hide grid lines
    ax.grid(False)

    # Remove labels
    ax.set_xticks([])
    ax.set_yticks([])

    # --- Add the values of the criteria in zone 11 ---
    for i, angle in enumerate(angles[:-1]):
        rotation_angle = np.degrees(angle) - 90  # Incline towards the center
        ha = 'center'

        # Adjust rotation for bottom texts
        if rotation_angle < -90 or rotation_angle > 90:
            rotation_angle += 180

        ax.text(angle, 10.5, criteria[i], rotation=rotation_angle, ha=ha, va='center', size=10, weight='bold')

    # --- Add the category names in zone 12 ---
    for i, (start, end) in enumerate(category_bounds):
        mid_angle = np.mean(angles[start:end])
        rotation_angle = np.degrees(mid_angle) - 90

        ha = 'center'
        if rotation_angle < -90 or rotation_angle > 90:
            rotation_angle += 180

        ax.text(mid_angle, 11.5, categories[i], rotation=rotation_angle, ha=ha, va='center', size=12, weight='bold')

    return fig, ax

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    # Get values from the form
    values = list(map(float, request.form.getlist('values[]')))
    criteria = request.form.getlist('criteria[]')
    categories = request.form.getlist('categories[]')

    # Number of criteria and angles
    num_vars = len(criteria)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    # Define the bounds for each category (start and end index for criteria)
    category_bounds = [(0, 3), (3, 6), (6, 9)]

    # Vérification de la longueur de la liste 'categories'
    if len(categories) != len(category_bounds):
        return "Error: The number of categories does not match the expected number."

    # Generate radar chart
    fig, ax = radar_chart(values, categories, criteria, angles, category_bounds)

    # Save chart to a BytesIO object and send as response
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close(fig)

    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)
