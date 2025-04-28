import streamlit as st
from supabase import create_client, Client
import uuid

def main():
    st.set_page_config(page_title="Sticker App", page_icon="🖼️", layout="centered")
    st.header("Sticker Goat gotta catch em all 🖼️🥳")
    st.write("Du kannst Sticker entweder fotografieren oder aus deiner Galerie hochladen")
    # Kamera
    st.subheader("📷 Aktivie die Kamera")
    kamera_aktiv = st.toggle("📷 Kamera aktivieren")
    camera_image = None
    file_name = None  
    file_bytes = None  
    if kamera_aktiv:
        camera_image = st.camera_input("Fotografie den Sticker")
    # File Upload
    st.subheader("📤 Bild hochladen")
    uploaded_file = st.file_uploader("Wähle ein Bild aus", type=["jpg", "png", "jpeg"])
    if camera_image is not None:
        st.image(camera_image, caption="Fotografiertes Bild", use_column_width=True)
        file_bytes = camera_image.getvalue()  
        file_name = f"{uuid.uuid4()}.png"  
    elif uploaded_file is not None:
        st.image(uploaded_file, caption="Hochgeladenes Bild", use_column_width=True)
        file_bytes = uploaded_file.read()  
        file_name = f"{uuid.uuid4()}.png"  #eindeutiger Name
        st.write(file_name)
    if file_name is None or file_bytes is None:
        st.error("❌ Kein Bild zum Hochladen ausgewählt.")
        return
    # Datenbank Verbindung
    if st.button("Eingaben bestätigen"):
        try:
            supabase_url = st.secrets["credentials"]["SUPABASE_URL"]
            supabase_key = st.secrets["credentials"]["SUPABASE_KEY"]
            supabase_client: Client = create_client(supabase_url, supabase_key)
            st.success("✅ Verbindung mit der Datenbank erfolgreich hergestellt!")
            bucket_name = "stickergoat"
            file_path = f"{bucket_name}/{file_name}"
            response = supabase_client.storage.from_(bucket_name).upload(file_path, file_bytes)
        except Exception as e:
            st.error(f"❌ Es kann keine Verbindung zur Datenbank hergestellt werden: {e}")

if __name__ == "__main__":
    main()
