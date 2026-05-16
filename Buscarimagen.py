import streamlit as strl
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Configuración de la página web
strl.set_page_config(page_title="Buscador en la Nube", page_icon="☁️", layout="wide")
strl.title("☁️ Buscador de Imágenes Guardadas")

# =====================================================================
# 🛠️ CONFIGURACIÓN DE LA NUBE (Reemplaza con tus datos de Cloudinary)
# =====================================================================
cloudinary.config(
  cloud_name = "dgnjohqam",
  api_key = "484947388857898",
  api_secret = "G0DdrgNISEeeNODGc4Kmn1W85kI",
  secure = True
)
# =====================================================================

# 1. Zona de subida de archivos a la nube
imagenes_cargadas = strl.file_uploader(
    "📁 Sube imágenes directamente aqui:", 
    type=["png", "jpg", "jpeg", "bmp", "gif"], 
    accept_multiple_files=True
)

# Enviar los archivos al servidor en la nube inmediatamente al subirlos
if imagenes_cargadas:
    with strl.spinner("Subiendo archivos..."):
        for archivo in imagenes_cargadas:
            try:
                # Subir archivo usando el nombre original como identificador público
                cloudinary.uploader.upload(
                    archivo, 
                    public_id=archivo.name.split('.')[0],
                    unique_filename=False,
                    overwrite=False
                )
            except Exception as e:
                pass # Ignora si el archivo ya existe en la nube
    strl.success("¡Sincronización completada con éxito!")

# 2. Zona de la barra de búsqueda
palabra_clave = strl.text_input("🔍 Escribe una palabra para buscar:")
palabra_clave_min = palabra_clave.strip().lower()

# 3. Consultar las imágenes almacenadas en la nube
try:
    # Solicitar la lista de archivos guardados en el servidor de Cloudinary
    recursos_nube = cloudinary.api.resources(max_results=100)
    lista_imagenes_nube = recursos_nube.get('resources', [])
    
    # Filtrar las imágenes según la palabra clave introducida
    imagenes_filtradas = [
        img for img in lista_imagenes_nube
        if not palabra_clave_min or palabra_clave_min in img['public_id'].lower()
    ]
    
    # Desplegar la galería desde internet
    if imagenes_filtradas:
        strl.write(f"Mostrando {len(imagenes_filtradas)} imágenes alojadas en la nube:")
        columnas = strl.columns(3)
        
        for indice, datos_imagen in enumerate(imagenes_filtradas):
            columna_actual = columnas[indice % 3]
            with columna_actual:
                # Se renderiza directamente usando la URL de internet provista por la nube
                strl.image(
                    datos_imagen['secure_url'], 
                    caption=f"{datos_imagen['public_id']}.{datos_imagen['format']}", 
                    use_container_width=True
                )
    else:
        strl.info("No se encontraron imágenes en la nube con ese criterio.")

except Exception as e:
    strl.error(f"Error al conectar con la nube. Verifica tus credenciales: {str(e)}")
