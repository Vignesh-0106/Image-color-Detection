# Color Detection Streamlit App

This project is a simple Streamlit application that allows users to upload an image, click anywhere on it, and get the pixel's RGB value plus the closest color name from a small dataset. It also displays a color reference box.

## Features
- Upload PNG/JPG images
- Click on the image to detect the clicked pixel color
- Shows RGB values, closest color name, hex code, and a color-filled reference box
- Simple and user-friendly UI

## Files
- `app.py` — Streamlit application
- `colors.csv` — Small dataset of colors and RGB values used to find closest match
- `requirements.txt` — Python dependencies
- `README.md` — This file

## How to run locally
1. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux / macOS
   venv\Scripts\activate    # Windows (PowerShell)
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deploying
You can deploy this app to Streamlit Cloud, Heroku, or any service that supports Python web apps. On Streamlit Cloud, just connect your GitHub repo and set the main file to `app.py`.

## Notes
- The app uses `streamlit-image-coordinates` to capture click coordinates on images.
- If you want a larger color dataset, replace `colors.csv` with an extended dataset (e.g., colors from `csv` or a public color list).

## License
MIT
