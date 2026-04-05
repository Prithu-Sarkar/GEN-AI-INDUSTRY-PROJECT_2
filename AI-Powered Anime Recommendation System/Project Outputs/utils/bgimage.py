import base64


def set_background(image_file):
    """
    Sets the background of a Streamlit app to an image.

    Parameters:
        image_file (str): The path to the image file.
    Returns:
        None
    """
    try:
        import streamlit as st
        with open(image_file, "rb") as f:
            img_data = f.read()
        b64_encoded = base64.b64encode(img_data).decode()
        style = f"""
            <style>
            .stApp {{
                background-image: url(data:image/png;base64,{b64_encoded});
                background-size: cover;
            }}
            </style>
        """
        st.markdown(style, unsafe_allow_html=True)
    except Exception:
        pass  # No-op in non-Streamlit context
