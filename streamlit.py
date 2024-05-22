import streamlit as st
import requests
from PIL import Image
import io
url = "https://482d-185-213-230-167.ngrok-free.app/predict"



def send_image(image):
    # Convert the image to binary format
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    # Create a dictionary of files to send with the POST request
    files = {"file": ("uploaded_image.jpg", img_byte_arr, "image/jpeg")}

    try:
        # Send the POST request with the image file
        response = requests.post(url, files=files)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"HTTP request failed: {e}")
        return None
    except ValueError as e:
        st.error(f"Failed to decode JSON response: {e}")
        st.text(response.text)  # Show the raw response text for debugging
        return None

st.title("Ekinlarning kasalliklarni va ularga tushgan zararkunanda hashoratlarni aniqlaydi!")

st.markdown('''
    Bu sizning ekinlaringizni kasalliklarini aniqlaydi 
    Ishlatish uchun rasm yuklang natijalarini ko'ring.
''')

uploaded_file = st.file_uploader('Rasm yuklash', type=['png', 'jpeg', 'wpeg','jpg'])


if uploaded_file is not None:
    image = Image.open(uploaded_file)

    # Read the uploaded image as a PIL image
    st.image(image, caption="Uploaded Image", use_column_width=True)

    natija = send_image(image)

    st.success(f"Kasallik: {natija['bashorat']}")
    st.info(f"ehtimolligi: {natija['ehtimolligi']}")
    st.write(f"maslahat : {natija['maslahat']}")

    st.video(natija['urll'])

    delete = st.button("rasmni o'chirish")
    if delete:
        st.info("Rasm va natijalar muvaffaqiyatli o'chirildi.")
