# Radar Chart Generator

This is a simple web application built with Flask that generates radar charts based on user-defined values. Users can adjust values via sliders and customize the titles for each criterion. If no title is provided, default titles (e.g., "Criterion 1", "Criterion 2") are used.

## Features

- 9 sliders for input values (0-10) for each criterion.
- Customizable titles for each criterion.
- Default titles are applied if no custom title is provided.
- Dynamic radar chart generation using Plotly.
- Chart image export functionality.

## Requirements

- **Python 3.7+**
- Python libraries:
  - Flask
  - Plotly
  - Gunicorn
  - Kaleido

## Installation

1. **Clone the repo:**

   ```bash
   git clone https://github.com/your-username/radar-chart-generator.git
   cd radar-chart-generator
   ```

2.	**Create and activate a virtual environment:**

```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3.	**Install dependencies:**

`pip install -r requirements.txt`



Running Locally

1.	**Start the application:**
For development (Flask):

`python app.py`

For production (Gunicorn):

`gunicorn app:app`


2.	**Access the app:**
Open your browser and go to:

http://127.0.0.1:5000/



Deployment

Deploying to Railway

	1.	Connect your GitHub repository to Railway.
	2.	Ensure your project has the following files:
	•	Procfile:

`web: gunicorn app:app`


	•	requirements.txt with all dependencies listed.

	3.	Railway will handle the rest and provide a public URL for your app.

Project Structure

radar-chart-generator/
├── app.py                   # Main Flask app code
├── Procfile                 # Instructions for running on Railway/Heroku
├── requirements.txt         # Python dependencies
├── static/
│   └── images/              # Folder for radar chart images
├── templates/
│   └── index.html           # HTML interface
├── README.md                # This file

Customization

	•	Criterion Titles: Users can customize the titles. Default titles (e.g., “Criterion 1”) are applied if left blank.
	•	Default Values: Sliders default to a value of 5, which can be changed in the index.html file.

License

This project is licensed under the MIT License. See the LICENSE file for details.

### Summary

This README provides the necessary information for installing, running, and deploying the project, with a brief overview of its features and structure. It's concise but includes all important details for getting started.