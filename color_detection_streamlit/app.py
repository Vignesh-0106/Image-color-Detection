import streamlit as st
from PIL import Image
import pandas as pd
import math
from streamlit_image_coordinates import streamlit_image_coordinates

st.set_page_config(page_title="Color Detector", layout="centered")

st.title("🎨 Color Detection from Images — Level 2")

st.markdown("""
Upload an image, click anywhere on the image and the app will show the RGB value, the closest color name from a dataset, and a color-filled reference box.
""")

# Load color dataset
@st.cache_data
def load_colors(path="colors.csv"):
    df = pd.read_csv(path)
    # Ensure integer RGB columns
    df[["R","G","B"]] = df[["R","G","B"]].astype(int)
    return df

colors_df = load_colors("colors.csv")

uploaded = st.file_uploader("Upload an image (PNG/JPG)", type=["png","jpg","jpeg"])

if uploaded is not None:
    image = Image.open(uploaded).convert("RGBA")
    st.write("**Image preview — click on the image to pick a color**")
    # Use streamlit_image_coordinates to capture clicks
    coords = streamlit_image_coordinates(image, key="img1", return_value="coordinates")

    if coords is not None and "x" in coords and "y" in coords:
        x, y = int(coords["x"]), int(coords["y"])
        # convert to RGB (ignore alpha)
        try:
            r, g, b, *rest = image.getpixel((x, y))
        except Exception:
            # some formats may return 3-tuple
            r, g, b = image.getpixel((x, y))
        r, g, b = int(r), int(g), int(b)

        st.write(f"**Clicked coordinates:** ({x}, {y})")
        st.write(f"**RGB value:** ({r}, {g}, {b})")

        # Find closest color by Euclidean distance in RGB space
        def closest_color_name(rgb_tuple, df):
            r0,g0,b0 = rgb_tuple
            diffs = (df["R"] - r0)**2 + (df["G"] - g0)**2 + (df["B"] - b0)**2
            idx = diffs.idxmin()
            row = df.loc[idx]
            return row["color_name"], row["hex"], int(row["R"]), int(row["G"]), int(row["B"])

        name, hexv, rr, gg, bb = closest_color_name((r,g,b), colors_df)

        st.write(f"**Closest color name:** {name}")
        st.write(f"**Hex:** {hexv}")

        # Show color box
        box_html = f"""
        <div style="width:120px;height:80px;border-radius:8px;border:1px solid #444;background:{hexv};"></div>
        """
        st.markdown(box_html, unsafe_allow_html=True)

        # Show a small palette: clicked color and matched color
        palette_html = f"""
        <div style="display:flex; gap:12px; align-items:center;">
          <div style="text-align:center;">
            <div style="width:120px;height:60px;border-radius:6px;border:1px solid #444;background:rgb({r},{g},{b});"></div>
            <div>Clicked color<br>rgb({r},{g},{b})</div>
          </div>
          <div style="text-align:center;">
            <div style="width:120px;height:60px;border-radius:6px;border:1px solid #444;background:{hexv};"></div>
            <div>Closest match<br>{name}</div>
          </div>
        </div>
        """
        st.markdown(palette_html, unsafe_allow_html=True)
    else:
        st.info("Click anywhere on the image to detect the color.")
else:
    st.info("Upload an image to start. (PNG/JPG)")

st.markdown("""---
**Notes & tips**:
- If you deploy this on Streamlit Cloud or other platforms, make sure to add `streamlit_image_coordinates` to requirements.
- The dataset `colors.csv` contains a list of common color names and RGB values used to find the closest named color.
""")
