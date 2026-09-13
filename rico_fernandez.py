import json
import os
import re
import urllib.parse
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="CHIFA - Menú Digital",
    page_icon="🥢",
    layout="centered",
)

# Cambiamos la versión a v4 para forzar la actualización de la base de datos
ARCHIVO_MENU = "menu_chifa_v4.json"

# Nombres únicos para evitar duplicidad al buscar en el diccionario
DATOS_POR_DEFECTO = {
    "segundos": [
        {"nombre": "Caldo de Gallina Solo", "precio": 5.0},
        {"nombre": "Caldo de Gallina con Presa (S/ 7.00)", "precio": 7.0},
        {"nombre": "Caldo de Gallina con Presa (S/ 6.00)", "precio": 6.0},
        {"nombre": "Chaufa de Pollo", "precio": 9.0},
        {"nombre": "Chaufa con Alitas (S/ 12.00)", "precio": 12.0},
        {"nombre": "Chaufa con Alitas (S/ 9.00)", "precio": 9.0},
        {"nombre": "Chaufa con Tortilla", "precio": 13.0},
        {"nombre": "Chaufa Salvaje", "precio": 11.0},
        {"nombre": "Chaufa Salvaje con Alitas", "precio": 14.0},
        {"nombre": "Aeropuerto de Pollo", "precio": 9.0},
        {"nombre": "Aeropuerto con Alitas", "precio": 12.0},
        {"nombre": "Aeropuerto con Tortilla", "precio": 13.0},
        {"nombre": "Chaufa con Lomo", "precio": 9.0},
        {"nombre": "Chaufa con Lomo más Alitas", "precio": 12.0},
        {"nombre": "Combinado", "precio": 9.0},
        {"nombre": "Combinado con Alitas", "precio": 12.0},
        {"nombre": "Tallarín Saltado", "precio": 11.0},
        {"nombre": "Sopa de Pollo", "precio": 9.0},
        {"nombre": "Sopa de Kion", "precio": 9.0},
        {"nombre": "Gaseosa de Litro", "precio": 7.0},
        {"nombre": "Gaseosa Gordita", "precio": 5.0},
        {"nombre": "Gaseosa Personal", "precio": 2.50},
    ]
}


# 2. FUNCIONES DE LECTURA Y ESCRITURA EN DISCO
def cargar_menu():
    if not os.path.exists(ARCHIVO_MENU):
        guardar_menu(DATOS_POR_DEFECTO)
        return DATOS_POR_DEFECTO
    try:
        with open(ARCHIVO_MENU, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if not datos or "segundos" not in datos:
                return DATOS_POR_DEFECTO
            return datos
    except Exception:
        return DATOS_POR_DEFECTO


def guardar_menu(datos):
    with open(ARCHIVO_MENU, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


menu_actual = cargar_menu()

# 3. Estilos CSS Personalizados
st.markdown(
    """
    <style>
    .stApp {
        background-color: #120A05;
        color: #FFFFFF;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    header {visibility: hidden;}

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }

    .header-container {
        text-align: center;
        margin-bottom: 10px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }

    .sub-title {
        color: #FFB300;
        font-size: 1rem;
        margin-top: -5px;
        margin-bottom: 15px;
        font-weight: 300;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .food-banner-container {
        display: flex;
        justify-content: space-around;
        align-items: center;
        margin-top: 5px;
        margin-bottom: 25px;
        border-radius: 20px;
        padding: 12px 5px;
        background: linear-gradient(180deg, #331400 0%, #120A05 100%);
        border: 1px solid #FF6600;
        box-shadow: inset 0px 3px 5px rgba(255, 255, 255, 0.1), 0px 10px 20px rgba(0, 0, 0, 0.6);
    }

    .food-item {
        text-align: center;
        width: 30%;
    }

    .food-item img {
        width: 90px;
        height: 90px;
        object-fit: cover;
        border-radius: 50%;
        box-shadow: 0px 5px 15px rgba(255, 102, 0, 0.8), inset 0px 2px 4px rgba(255,255,255,0.4);
        border: 3px solid #FF6600;
    }

    h3 {
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        margin-top: 15px !important;
        margin-bottom: 10px !important;
        border-bottom: 2px solid #FF6600;
        display: inline-block;
        padding-bottom: 3px;
    }

    /* EFECTO 3D PARA SELECTBOX */
    div[data-baseweb="select"] > div {
        background-color: #2A1508 !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        border-top: 2px solid #FF8533 !important;
        border-left: 2px solid #FF8533 !important;
        border-bottom: 3px solid #1A0A00 !important;
        border-right: 3px solid #1A0A00 !important;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.6), inset 0px 3px 6px rgba(255, 255, 255, 0.15) !important;
        transition: transform 0.1s ease, box-shadow 0.1s ease;
    }

    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    /* EFECTO 3D PARA ENTRADA DE TEXTO Y CONTRASEÑA */
    .stTextArea textarea, .stTextInput input, .stNumberInput input {
        background-color: #2A1508 !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        border-top: 2px solid #FF8533 !important;
        border-left: 2px solid #FF8533 !important;
        border-bottom: 3px solid #1A0A00 !important;
        border-right: 3px solid #1A0A00 !important;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.6), inset 0px 3px 6px rgba(255, 255, 255, 0.15) !important;
    }

    /* DESPLEGABLE ADMIN */
    div[data-testid="stExpander"] {
        background-color: #2A1508 !important;
        border-radius: 14px !important;
        border: 2px solid #FF6600 !important;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.7) !important;
    }

    div[data-testid="stTextArea"]:has(textarea[aria-label*="Observaciones"]) textarea {
        text-transform: uppercase !important;
    }

    /* BOTÓN CENTRADO */
    div.stButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #FF6600 0%, #CC3300 100%) !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 22px !important;
        letter-spacing: 1.5px !important;
        border-radius: 16px !important;
        padding: 16px 28px !important;
        width: 100% !important;
        max-width: 500px !important;
        text-transform: uppercase;
        text-align: center !important;
        border-top: 2px solid #FFB380 !important;
        border-left: 2px solid #FFB380 !important;
        border-bottom: 5px solid #661100 !important;
        border-right: 5px solid #661100 !important;
        box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.7), inset 0px 4px 8px rgba(255, 255, 255, 0.3) !important;
        transition: all 0.1s ease;
    }
    
    div.stButton > button:active {
        transform: translateY(4px);
        box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.7), inset 0px 6px 12px rgba(0, 0, 0, 0.6) !important;
        border-top: 5px solid #661100 !important;
        border-left: 5px solid #661100 !important;
        border-bottom: 2px solid #FFB380 !important;
        border-right: 2px solid #FFB380 !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 4. Encabezado Curvado
NOMBRE_RESTAURANTE = "CHIFA MILAGRITOS"

st.markdown(
    f"""
    <div class="header-container">
        <svg width="100%" height="110" viewBox="0 0 600 110" xmlns="http://www.w3.org/2000/svg">
            <defs>
                <filter id="drop-shadow" x="-20%" y="-20%" width="140%" height="150%">
                    <feDropShadow dx="0" dy="7" stdDeviation="3.5" flood-color="#000000" flood-opacity="0.95"/>
                </filter>
            </defs>
            <path id="curve" d="M 30 95 Q 300 -10 570 95" fill="transparent"/>
            <text font-family="'Helvetica Neue', sans-serif" font-size="30" font-weight="900" fill="#FF6600" letter-spacing="2" filter="url(#drop-shadow)">
                <textPath href="#curve" startOffset="50%" text-anchor="middle">
                    🥢 {NOMBRE_RESTAURANTE} 🥢
                </textPath>
            </text>
        </svg>
        <p class="sub-title">Menú Digital & Pedidos</p>
    </div>
""",
    unsafe_allow_html=True,
)

# 5. Banner de fotos
REPO_USER = "RESTAURATEBEF"
REPO_NAME = "menu-polleria"

st.markdown(
    f"""
    <div class="food-banner-container">
        <div class="food-item">
            <img src="https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/pollo_brasa.jpg" alt="Chifa 1">
        </div>
        <div class="food-item">
            <img src="https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/papas.jpg" alt="Chifa 2">
        </div>
        <div class="food-item">
            <img src="https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/gaseosa.jpg" alt="Chifa 3">
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

st.divider()

# 6. Mapeo optimizado indexado directamente por la posición elegida
lista_items = menu_actual.get("segundos", [])
opciones_segundos = ["Ninguno"] + [
    f"{item['nombre']} - S/ {item['precio']:.2f}" for item in lista_items
]

mesas = [f"Mesa {i}" for i in range(1, 16)]

st.markdown("### 📍 Ubicación y Personas")
col_mesa, col_personas = st.columns(2)

with col_mesa:
    mesa = st.selectbox("Mesa:", mesas)

with col_personas:
    num_personas = st.selectbox(
        "¿Cuántos menús/personas son?",
        options=list(range(1, 11)),
        index=0,
    )

st.markdown("### 📋 Tu Orden")

pedidos_realizados = []
total_acumulado = 0.0


# Función ajustada para extraer el precio exactamente de la opción seleccionada
def extraer_precio(seleccion, lista_base):
    if seleccion == "Ninguno":
        return 0.0, seleccion

    # Extraemos el precio directamente del texto del Selectbox
    partes = seleccion.rsplit(" - S/ ", 1)
    nombre = partes[0]
    precio = float(partes[1]) if len(partes) > 1 else 0.0

    return precio, nombre


for i in range(num_personas):
    st.markdown(
        f"""
        <div style="
            color: #FF6600; 
            font-size: 1.1rem; 
            font-weight: 800; 
            letter-spacing: 1.5px; 
            margin-top: 15px; 
            margin-bottom: 8px;
            text-transform: uppercase;">
            👤 PERSONA {i+1}
        </div>
        """,
        unsafe_allow_html=True,
    )

    seg_sel = st.selectbox(
        "Selecciona el Plato / Bebida:", opciones_segundos, key=f"seg_{i}"
    )
    p_seg, n_seg = extraer_precio(seg_sel, lista_items)

    subtotal_persona = p_seg
    total_acumulado += subtotal_persona

    pedidos_realizados.append(
        {
            "segundo": n_seg,
            "p_segundo": p_seg,
            "subtotal": subtotal_persona,
        }
    )

# Visualización de Cuenta Total
st.markdown(
    f"""
    <div style="
        background-color: #2A1508;
        border: 2px solid #FF6600;
        border-radius: 12px;
        padding: 12px;
        margin-top: 15px;
        margin-bottom: 15px;
        text-align: right;">
        <span style="font-size: 1.1rem; color: #FFB300; font-weight: bold;">TOTAL ESTIMADO: </span>
        <span style="font-size: 1.4rem; color: #25D366; font-weight: 900;">S/ {total_acumulado:.2f}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Observaciones Generales
obs_input = st.text_area(
    "📝 Observaciones Generales (Opcional - Solo Letras):",
    placeholder="EJ: SIN CEBOLLITA CHINA, SIN SILLAO, CALDO BIEN CALIENTE...",
    height=80,
    key="txt_obs",
)

# JavaScript para restringir números sólo en Observaciones
st.components.v1.html(
    """
    <script>
    const parentDoc = window.parent.document;
    
    function aplicarBloqueoObservaciones() {
        const textareas = parentDoc.querySelectorAll('textarea');
        textareas.forEach(textarea => {
            const label = textarea.getAttribute('aria-label') || '';
            if (label.includes('Observaciones') && !textarea.dataset.bloqueado) {
                textarea.dataset.bloqueado = "true";
                
                textarea.addEventListener('keydown', function(e) {
                    if ((e.key >= '0' && e.key <= '9') || (e.keyCode >= 96 && e.keyCode <= 105)) {
                        e.preventDefault();
                    }
                });
                
                textarea.addEventListener('input', function(e) {
                    this.value = this.value.replace(/[0-9]/g, '');
                });
            }
        });
    }

    setInterval(aplicarBloqueoObservaciones, 400);
    </script>
    """,
    height=0,
)

observaciones = re.sub(r"[0-9]", "", obs_input).upper()

st.divider()

# 7. Confirmación y Enviar a WhatsApp
btn_enviar = st.button("🚀 CONFIRMAR Y ENVIAR PEDIDO")

if btn_enviar:
    hay_pedido = any(p["segundo"] != "Ninguno" for p in pedidos_realizados)

    if not hay_pedido:
        st.warning(
            "⚠️ Por favor, selecciona al menos un pedido para enviar la orden."
        )
    else:
        mensaje = f"*{NOMBRE_RESTAURANTE}*\n"
        mensaje += f"📍 *{mesa}* (Total personas: {num_personas})\n\n"

        for idx, p in enumerate(pedidos_realizados, 1):
            if p["segundo"] != "Ninguno":
                mensaje += f"*— PERSONA {idx} —*\n"
                mensaje += (
                    f"• *Item:* {p['segundo']} (S/ {p['p_segundo']:.2f})\n"
                )

        if observaciones.strip():
            mensaje += f"\n📝 *OBS:* {observaciones.strip()}\n"

        mensaje += f"\n💰 *TOTAL A PAGAR: S/ {total_acumulado:.2f}*"

        numero_whatsapp = "51918539634"
        mensaje_codificado = urllib.parse.quote(mensaje)
        url_whatsapp = (
            f"https://wa.me/{numero_whatsapp}?text={mensaje_codificado}"
        )

        st.success("✅ ¡Pedido generado con éxito!")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <a href="{url_whatsapp}" target="_blank" style="width: 100%; max-width: 500px; text-decoration: none;">
                    <button style="
                        background-color: #25D366;
                        color: white;
                        padding: 16px 20px;
                        border: none;
                        border-radius: 14px;
                        font-weight: 900;
                        width: 100%;
                        font-size: 20px;
                        cursor: pointer;
                        margin-top: 10px;
                        text-transform: uppercase;
                        text-align: center;
                        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.5);">
                        💬 Abrir WhatsApp para Enviar Pedido
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

# 8. PANEL DE ADMINISTRACIÓN
st.write("")
st.write("")
st.divider()

with st.expander("🔑 Acceso Administrador (Actualizar Menú y Precios)"):
    clave_admin = st.text_input(
        "Ingresa la clave:", type="password", key="pwd_admin"
    )

    if clave_admin == "1234":
        st.success("🔓 Acceso concedido")
        st.caption(
            "Escribe un elemento por línea en el formato: Nombre - Precio (Ej:"
            " Chaufa de Pollo - 9.00)"
        )

        txt_segundos_def = "\n".join(
            [
                f"{item['nombre']} - {item['precio']:.2f}"
                for item in menu_actual.get("segundos", [])
            ]
        )

        admin_seg_txt = st.text_area(
            "Lista de Platos/Bebidas y Precios:", value=txt_segundos_def, height=200
        )

        def parsear_area(texto):
            items = []
            for linea in texto.strip().split("\n"):
                if "-" in linea:
                    partes = linea.rsplit("-", 1)
                    nombre = partes[0].strip()
                    try:
                        precio = float(partes[1].strip())
                    except ValueError:
                        precio = 0.0
                    if nombre:
                        items.append({"nombre": nombre, "precio": precio})
                elif linea.strip():
                    items.append({"nombre": linea.strip(), "precio": 0.0})
            return items

        if st.button("💾 Guardar Menú y Precios", key="btn_guardar"):
            nuevo_menu = {
                "segundos": parsear_area(admin_seg_txt),
            }

            guardar_menu(nuevo_menu)

            st.success(
                "✅ ¡Menú y precios actualizados con éxito para todos los"
                " clientes!"
            )
            st.rerun()

    elif clave_admin != "":
        st.error("❌ Clave incorrecta")
