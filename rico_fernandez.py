import json
import os
import re
import urllib.parse
import streamlit as st

# 1. Configuración de la página
st.set_page_config(
    page_title="POLLERÍA - Menú Digital",
    page_icon="🍗",
    layout="centered",
)

# ARCHIVO DE BASE DE DATOS LOCAL
ARCHIVO_MENU = "menu_polleria_db.json"

# Datos por defecto para Pollería
DATOS_POR_DEFECTO = {
    "entradas": [
        {"nombre": "Tequeños con Guacamole", "precio": 14.0},
        {"nombre": "Sopa de Pollo / Dieta", "precio": 12.0},
        {"nombre": "Porción de Anticuchos", "precio": 18.0},
    ],
    "segundos": [
        {"nombre": "1/4 de Pollo a la Brasa", "precio": 18.0},
        {"nombre": "1/2 Pollo a la Brasa", "precio": 34.0},
        {"nombre": "1 Pollo Entero a la Brasa", "precio": 65.0},
        {"nombre": "Mostrito (1/4 Pollo + Chaufa)", "precio": 22.0},
        {"nombre": "Parrilla Familiar", "precio": 85.0},
    ],
    "bebidas": [
        {"nombre": "Inca Kola 1.5L", "precio": 10.0},
        {"nombre": "Coca Cola 1.5L", "precio": 10.0},
        {"nombre": "Chicha Morada Jarra 1L", "precio": 12.0},
        {"nombre": "Limonada Jarra 1L", "precio": 10.0},
    ],
}


# 2. FUNCIONES DE LECTURA Y ESCRITURA EN DISCO
def cargar_menu():
    if not os.path.exists(ARCHIVO_MENU):
        guardar_menu(DATOS_POR_DEFECTO)
        return DATOS_POR_DEFECTO
    try:
        with open(ARCHIVO_MENU, "r", encoding="utf-8") as f:
            datos = json.load(f)
            if datos and isinstance(datos.get("entradas", [])[0], str):
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

    div[data-baseweb="select"] > div {
        background-color: #2A1508 !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        border-top: 2px solid #FF8533 !important;
        border-left: 2px solid #FF8533 !important;
        border-bottom: 3px solid #1A0A00 !important;
        border-right: 3px solid #1A0A00 !important;
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.6), inset 0px 3px 6px rgba(255, 255, 255, 0.15) !important;
    }

    div[data-baseweb="select"] * { color: #FFFFFF !important; }

    .stTextArea textarea, .stTextInput input, .stNumberInput input {
        background-color: #2A1508 !important;
        border-radius: 12px !important;
        color: #FFFFFF !important;
        border-top: 2px solid #FF8533 !important;
        border-left: 2px solid #FF8533 !important;
        border-bottom: 3px solid #1A0A00 !important;
        border-right: 3px solid #1A0A00 !important;
    }

    div[data-testid="stExpander"] {
        background-color: #2A1508 !important;
        border-radius: 14px !important;
        border: 2px solid #FF6600 !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #FF6600 0%, #CC3300 100%) !important;
        color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 22px !important;
        border-radius: 16px !important;
        padding: 16px 28px !important;
        width: 100% !important;
        max-width: 500px !important;
        text-transform: uppercase;
        border-top: 2px solid #FFB380 !important;
        border-bottom: 5px solid #661100 !important;
        box-shadow: 0px 12px 20px rgba(0, 0, 0, 0.7) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 4. Encabezado Curvado (CAMBIA AQUÍ EL NOMBRE DE TU POLLERÍA)
NOMBRE_POLLERIA = "POLLERÍA MI GRAN SABOR"

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
                    🍗 {NOMBRE_POLLERIA} 🍗
                </textPath>
            </text>
        </svg>
        <p class="sub-title">Menú Digital & Pedidos</p>
    </div>
""",
    unsafe_allow_html=True,
)

# 5. Banner de fotos (Reemplaza con los nombres de tus imágenes)
REPO_USER = "RESTAURATEBEF"  # Tu usuario de GitHub
REPO_NAME = "menu-polleria"  # Nombre de este nuevo repo

st.markdown(
    f"""
    <div class="food-banner-container">
        <div class="food-item">
            <img src="https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/pollo_brasa.jpg" alt="Pollo">
        </div>
        <div class="food-item">
            <img src="https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/papas.jpg" alt="Papas">
        </div>
        <div class="food-item">
            <img src="https://raw.githubusercontent.com/{REPO_USER}/{REPO_NAME}/main/ensalada.jpg" alt="Ensalada">
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

st.divider()

# 6. Lógica de Pedidos
opciones_entradas = ["Ninguna"] + [
    f"{item['nombre']} - S/ {item['precio']:.2f}"
    for item in menu_actual.get("entradas", [])
]
opciones_segundos = ["Ninguno"] + [
    f"{item['nombre']} - S/ {item['precio']:.2f}"
    for item in menu_actual.get("segundos", [])
]
opciones_bebidas = ["Ninguna"] + [
    f"{item['nombre']} - S/ {item['precio']:.2f}"
    for item in menu_actual.get("bebidas", [])
]

mesas = [f"Mesa {i}" for i in range(1, 16)]

st.markdown("### 📍 Ubicación y Personas")
col_mesa, col_personas = st.columns(2)

with col_mesa:
    mesa = st.selectbox("Mesa:", mesas)

with col_personas:
    num_personas = st.selectbox(
        "¿Cuántos menús/personas son?", options=list(range(1, 11)), index=0
    )

st.markdown("### 📋 Tu Orden")

pedidos_realizados = []
total_acumulado = 0.0


def extraer_precio(seleccion, lista_base):
    if seleccion in ["Ninguna", "Ninguno"]:
        return 0.0, seleccion
    nombre = seleccion.split(" - S/")[0]
    for item in lista_base:
        if item["nombre"] == nombre:
            return item["precio"], nombre
    return 0.0, nombre


for i in range(num_personas):
    st.markdown(
        f"<div style='color: #FF6600; font-weight: 800; margin-top: 10px;'>👤"
        f" PERSONA {i+1}</div>",
        unsafe_allow_html=True,
    )
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        ent_sel = st.selectbox(f"Entrada:", opciones_entradas, key=f"ent_{i}")
        p_ent, n_ent = extraer_precio(
            ent_sel, menu_actual.get("entradas", [])
        )

    with col2:
        seg_sel = st.selectbox(f"Plato:", opciones_segundos, key=f"seg_{i}")
        p_seg, n_seg = extraer_precio(
            seg_sel, menu_actual.get("segundos", [])
        )

    with col3:
        beb_sel = st.selectbox(f"Bebida:", opciones_bebidas, key=f"beb_{i}")
        p_beb, n_beb = extraer_precio(beb_sel, menu_actual.get("bebidas", []))

    subtotal = p_ent + p_seg + p_beb
    total_acumulado += subtotal
    pedidos_realizados.append(
        {
            "entrada": n_ent,
            "p_entrada": p_ent,
            "segundo": n_seg,
            "p_segundo": p_seg,
            "bebida": n_beb,
            "p_bebida": p_beb,
            "subtotal": subtotal,
        }
    )

st.markdown(
    f"""
    <div style="background-color: #2A1508; border: 2px solid #FF6600; border-radius: 12px; padding: 12px; margin: 15px 0; text-align: right;">
        <span style="font-size: 1.1rem; color: #FFB300; font-weight: bold;">TOTAL ESTIMADO: </span>
        <span style="font-size: 1.4rem; color: #25D366; font-weight: 900;">S/ {total_acumulado:.2f}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

obs_input = st.text_area(
    "📝 Observaciones (Opcional):",
    placeholder="EJ: BIEN DORADO, CREMAS APARTE...",
    height=80,
    key="txt_obs",
)
observaciones = re.sub(r"[0-9]", "", obs_input).upper()

st.divider()

# 7. Enviar Pedido por WhatsApp
if st.button("🚀 CONFIRMAR Y ENVIAR PEDIDO"):
    hay_pedido = any(
        p["entrada"] != "Ninguna"
        or p["segundo"] != "Ninguno"
        or p["bebida"] != "Ninguna"
        for p in pedidos_realizados
    )

    if not hay_pedido:
        st.warning("⚠️ Selecciona al menos un producto.")
    else:
        mensaje = f"*{NOMBRE_POLLERIA}*\n"
        mensaje += f"📍 *{mesa}* (Total personas: {num_personas})\n\n"

        for idx, p in enumerate(pedidos_realizados, 1):
            if (
                p["entrada"] != "Ninguna"
                or p["segundo"] != "Ninguno"
                or p["bebida"] != "Ninguna"
            ):
                mensaje += f"*— PERSONA {idx} —*\n"
                if p["entrada"] != "Ninguna":
                    mensaje += (
                        f"• *Entrada:* {p['entrada']} (S/"
                        f" {p['p_entrada']:.2f})\n"
                    )
                if p["segundo"] != "Ninguno":
                    mensaje += (
                        f"• *Plato:* {p['segundo']} (S/ {p['p_segundo']:.2f})\n"
                    )
                if p["bebida"] != "Ninguna":
                    mensaje += (
                        f"• *Bebida:* {p['bebida']} (S/ {p['p_bebida']:.2f})\n"
                    )

        if observaciones.strip():
            mensaje += f"\n📝 *OBS:* {observaciones.strip()}\n"

        mensaje += f"\n💰 *TOTAL A PAGAR: S/ {total_acumulado:.2f}*"

        numero_whatsapp = "51918539634"  # Cambiar número si es distinto
        url_whatsapp = f"https://wa.me/{numero_whatsapp}?text={urllib.parse.quote(mensaje)}"

        st.success("✅ ¡Pedido generado!")
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center;">
                <a href="{url_whatsapp}" target="_blank" style="width: 100%; max-width: 500px; text-decoration: none;">
                    <button style="background-color: #25D366; color: white; padding: 16px; border: none; border-radius: 14px; font-weight: 900; width: 100%; font-size: 20px; cursor: pointer; text-transform: uppercase;">
                        💬 Abrir WhatsApp para Enviar Pedido
                    </button>
                </a>
            </div>
            """,
            unsafe_allow_html=True,
        )

# 8. Panel Admin
st.write("")
st.divider()
with st.expander("🔑 Acceso Administrador (Actualizar Menú y Precios)"):
    clave_admin = st.text_input(
        "Ingresa la clave:", type="password", key="pwd_admin"
    )
    if clave_admin == "1234":
        st.success("🔓 Acceso concedido")
        txt_ent = "\n".join(
            [
                f"{i['nombre']} - {i['precio']:.2f}"
                for i in menu_actual.get("entradas", [])
            ]
        )
        txt_seg = "\n".join(
            [
                f"{i['nombre']} - {i['precio']:.2f}"
                for i in menu_actual.get("segundos", [])
            ]
        )
        txt_beb = "\n".join(
            [
                f"{i['nombre']} - {i['precio']:.2f}"
                for i in menu_actual.get("bebidas", [])
            ]
        )

        admin_ent_txt = st.text_area("Entradas:", value=txt_ent, height=100)
        admin_seg_txt = st.text_area(
            "Platos Principales:", value=txt_seg, height=120
        )
        admin_beb_txt = st.text_area("Bebidas:", value=txt_beb, height=100)


        def parsear(texto):
            items = []
            for l in texto.strip().split("\n"):
                if "-" in l:
                    p = l.rsplit("-", 1)
                    try:
                        precio = float(p[1].strip())
                    except:
                        precio = 0.0
                    items.append({"nombre": p[0].strip(), "precio": precio})
            return items


        if st.button("💾 Guardar Menú y Precios"):
            guardar_menu(
                {
                    "entradas": parsear(admin_ent_txt),
                    "segundos": parsear(admin_seg_txt),
                    "bebidas": parsear(admin_beb_txt),
                }
            )
            st.success("✅ Guardado correctamente")
            st.rerun()
