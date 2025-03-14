import streamlit as st
import cv2
import numpy as np
import plotly.graph_objects as go
import os  # Required for file handling
from depth_model import estimate_depth
from point_cloud import depth_to_3d, visualize_3d_point_cloud

st.title("IMU-Based 3D Depth Mapping (Interactive)")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png"])

if uploaded_file is not None:
    # ✅ Ensure the "images/" directory exists
    file_dir = "images"
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    file_path = os.path.join(file_dir, uploaded_file.name)

    # ✅ Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # ✅ Display the uploaded image
    st.image(file_path, caption="Uploaded Image", use_column_width=True)

    st.write("### Generating Depth Map...")

    # ✅ Ensure the "output/" directory exists before generating depth map
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # ✅ Call the function to estimate depth (Ensure it returns a valid depth map)
    depth_map = estimate_depth(file_path)

    # ✅ Ensure the depth map is saved in the correct location
    depth_map_path = os.path.join(output_dir, "depth_map.jpg")

    # ✅ Check if the file is actually created before displaying
    if not os.path.exists(depth_map_path):
        st.error("Error: Depth map was not generated successfully. Please check estimate_depth() function.")
    else:
        st.image(depth_map_path, caption="Depth Map", use_column_width=True)

        st.write("### Converting to 3D Point Cloud...")
        x, y, z = depth_to_3d(depth_map)

        # ✅ Display interactive 3D plot using Plotly
        fig = visualize_3d_point_cloud(x, y, z)
        st.plotly_chart(fig, use_container_width=True)

        st.success("Interactive 3D Point Cloud Generated! ✅")
