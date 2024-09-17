from flask import Flask, render_template, request
import plotly.graph_objs as go
import plotly.io as pio

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_chart', methods=['POST'])
def generate_chart():
    criteria_count = int(request.form['criteria_count'])
    categories = []
    values_by_category = []
    labels_by_category = []
    all_values = []

    # Iterate through possible categories (up to 10)
    for i in range(1, 11):
        category_name = request.form[f'category{i}']
        num_criteria = int(request.form[f'num_criteria{i}']) if request.form[f'num_criteria{i}'] else 0

        # If a category is defined and has at least 1 criterion
        if category_name and num_criteria > 0:
            category_values = []
            category_labels = []

            # Collect the criteria values and labels for this category
            for j in range(sum(len(v) for v in values_by_category) + 1, sum(len(v) for v in values_by_category) + num_criteria + 1):
                if j > criteria_count:  # Ensure we don't exceed the number of criteria
                    break
                value = float(request.form[f'slider{j}'])
                label = request.form[f'title{j}'] if request.form[f'title{j}'] else f'Criterion {j}'

                category_values.append(value)
                category_labels.append(label)
                all_values.append(value)
            
            # Store the values and labels for this category
            categories.append(category_name)
            values_by_category.append(category_values)
            labels_by_category.append(category_labels)

    # Create radar chart with Plotly
    fig = go.Figure()

    # Add data for each category to the radar chart
    for idx, category in enumerate(categories):
        fig.add_trace(go.Scatterpolar(
            r=values_by_category[idx],
            theta=labels_by_category[idx],
            fill='toself',
            name=category
        ))

    # Configure the chart layout
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10])
        ),
        showlegend=True
    )

    # Save the chart as an image
    img_path = "static/images/radar_chart.png"
    pio.write_image(fig, img_path)

    return render_template('index.html', image_path=img_path, values=all_values)

if __name__ == '__main__':
    app.run(debug=True)
