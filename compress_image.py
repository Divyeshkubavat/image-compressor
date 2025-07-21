import streamlit as st
from PIL import Image
import io
import zipfile
import os

st.title("Image Compression App")

upload_type = st.radio("Upload Type", ["Single Image", "Multiple Images (Zip)"])

quality = st.slider("Compression Quality (Lower = More Compression)", 10, 100, 75)
resize_option = st.checkbox("Resize Images?")
if resize_option:
    width = st.number_input("Width", min_value=1, value=800)
    height = st.number_input("Height", min_value=1, value=600)
else:
    width, height = None, None

compressed_images = []

if upload_type == "Single Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        if resize_option:
            img = img.resize((width, height))
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", optimize=True, quality=quality)
        buffer.seek(0)
        compressed_images.append((uploaded_file.name, buffer))
elif upload_type == "Multiple Images (Zip)":
    uploaded_zip = st.file_uploader("Upload a ZIP file containing images", type="zip")
    if uploaded_zip:
        with zipfile.ZipFile(uploaded_zip) as z:
            for file in z.namelist():
                with z.open(file) as f:
                    try:
                        img = Image.open(f)
                        if resize_option:
                            img = img.resize((width, height))
                        buffer = io.BytesIO()
                        img.save(buffer, format="JPEG", optimize=True, quality=quality)
                        buffer.seek(0)
                        compressed_images.append((file, buffer))
                    except:
                        continue

if compressed_images:
    if len(compressed_images) == 1:
        file_name, img_data = compressed_images[0]
        st.download_button("Download Compressed Image", img_data, file_name="compressed_" + file_name, mime="image/jpeg")
    else:
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for file_name, img_data in compressed_images:
                zipf.writestr("compressed_" + file_name, img_data.getvalue())
        zip_buffer.seek(0)
        st.download_button("Download All as ZIP", zip_buffer, file_name="compressed_images.zip", mime="application/zip")
