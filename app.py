# Import packages
from dash import Dash, html, dash_table
import easyocr
import cv2
import pandas as pd

# Disable GPU
reader = easyocr.Reader(['en'], gpu=False)

# Image path
image_path = 'ADMIN1.jpg'

# Define regions of interest (ROI) using coordinates
roi_coordinates = [(258, 585, 578, 228),
                  (1488, 602, 476, 197),
                  (3461, 594, 700, 205),
                  (2755, 3159, 1360, 42),
                  (2748, 3258, 1388, 92),
                  (2741, 3378, 1381, 114)]
# Read text from the specified regions
result = []
image = cv2.imread(image_path)  # Load the image
for roi in roi_coordinates:
    x1, y1, w, h = roi
    x2 = x1 + w
    y2 = y1 + h
    cropped_image = image[y1:y2, x1:x2]  # Crop the image based on ROI
    text = reader.readtext(cropped_image, detail=0)  # Use detail=0 to extract only the text
    result.append(text)

# Convert the result to a dictionary
dictionary_result = {}
for res in result:
    for entry in res:
        key = entry
        value = res[res.index(entry) + 1] if res.index(entry) < len(res) - 1 else None
        if key and value:
            dictionary_result[key] = value

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame([dictionary_result])

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='Building Optimization Technologies Test by Jhoeel Luna'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=10)
])

server = app.server  # Assign the app.server to the variable 'server'

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)