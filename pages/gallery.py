import streamlit as st
from supabase import create_client, Client

st.title("Gallery")

try:
    supabase_url = st.secrets["credentials"]["SUPABASE_URL"]
    supabase_key = st.secrets["credentials"]["SUPABASE_KEY"]
    supabase_client: Client = create_client(supabase_url, supabase_key)

    st.success("✅ Verbindung mit der Datenbank erfolgreich hergestellt!")

    bucket_name = "stickergoat"
    response = supabase_client.storage.from_(bucket_name).list("stickergoat")
    response = response[:-1]
    if response:
        for image in response:
            image_path = image['name']
            image_path = f"stickergoat/{image_path}"  
            image_url = supabase_client.storage.from_(bucket_name).get_public_url(image_path)
            st.image(image_url,  use_container_width =True)
    else:
        st.error("❌ Keine Bilder im Bucket gefunden.")
except Exception as e:
    st.error(f"❌ Es kann keine Verbindung zur Datenbank hergestellt werden: {e}")
