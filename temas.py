# temas.py: los dos temas visuales principales (Navidad Noche y Navidad Día)

TEMAS = {
    "navidad_noche": {
        "clave": "navidad_noche",
        "nombre": "Navidad (Noche)",
        "fondo": "#040B16",          # Azul noche oscuro medianoche
        "canvas_fondo": "#040B16",
        "cielo_elemento": "luna",    # Luna creciente luminosa + estrellas
        "palo": "#C69214",           # Madera dorada iluminada
        "palo_activo": "#FFE600",    # Amarillo activo
        "base": "#DCEBFA",           # Nieve fría nocturna con brillo lunar
        "base_sombra": "#1E293B",
        "texto": "#FFFFFF",          # Texto blanco brillante
        "texto_hud": "#F8FAFC",
        "texto_base": "#0F172A",     # texto oscuro sobre la nieve
        "mensaje_normal": "#93C5FD", # Celeste luminoso
        "mensaje_error": "#FF6B6B",  # Rojo suave visible en noche
        "mensaje_victoria": "#FACC15",# Oro brillante
        "estrella": "#FACC15",       # Estrella dorada brillante
        "estrella_borde": "#CA8A04",
        "btn_tema_txt": "☀️ Cambiar a Modo Día",
        "btn_tema_bg": "#FBBF24",
        "btn_tema_fg": "#1E1B4B",
        "discos": [
            "#EF4444",  # 1: Rojo rubí brillante
            "#06B6D4",  # 2: Cian hielo
            "#10B981",  # 3: Verde esmeralda
            "#A855F7",  # 4: Violeta festivo
            "#F97316",  # 5: Naranja encendido
            "#CBD5E1",  # 6: Plata luna
            "#FACC15",  # 7: Oro brillante
            "#FEF3C7"   # 8: Crema nieve
        ],
        "texto_disco": ["#0F172A", "#0F172A", "#0F172A", "#0F172A", "#0F172A", "#0F172A", "#0F172A", "#0F172A"],
        "titulo": "Torre de Hanói: Navidad (Noche) 🌙",
        "victoria_titulo": "¡Felices fiestas!",
        "victoria": "¡Felices fiestas! Completaste el árbol bajo el cielo estrellado."
    },
    "navidad_dia": {
        "clave": "navidad_dia",
        "nombre": "Navidad (Día)",
        "fondo": "#BAE6FD",          # Celeste claro de ventana diurna
        "canvas_fondo": "#7DD3FC",   # Cielo azul radiante y soleado
        "cielo_elemento": "sol",     # Gran Sol dorado radiante + nubes blancas
        "palo": "#78350F",           # Madera oscura de pino
        "palo_activo": "#EA580C",    # Naranja activo
        "base": "#FFFFFF",           # Nieve blanca pura iluminada por el sol
        "base_sombra": "#94A3B8",
        "texto": "#0F172A",          # Azul marino oscuro muy legible
        "texto_hud": "#0F172A",
        "texto_base": "#0F172A",     # texto oscuro sobre la nieve
        "mensaje_normal": "#1E3A8A", # Azul marino
        "mensaje_error": "#DC2626",  # Rojo puro de advertencia
        "mensaje_victoria": "#15803D",# Verde pino diurno
        "estrella": "#F59E0B",       # Amarillo cálido
        "estrella_borde": "#92400E",
        "btn_tema_txt": "🌙 Cambiar a Modo Noche",
        "btn_tema_bg": "#0F172A",
        "btn_tema_fg": "#FFFFFF",
        "discos": [
            "#DC2626",  # 1: Rojo acebo
            "#0369A1",  # 2: Azul zafiro
            "#16A34A",  # 3: Verde pino festivo
            "#7C3AED",  # 4: Púrpura real
            "#EA580C",  # 5: Naranja mandarina
            "#475569",  # 6: Gris pizarra
            "#CA8A04",  # 7: Mostaza dorada
            "#FEF08A"   # 8: Amarillo pastel
        ],
        "texto_disco": ["#FFFFFF", "#FFFFFF", "#0F172A", "#FFFFFF", "#0F172A", "#FFFFFF", "#0F172A", "#0F172A"],
        "titulo": "Torre de Hanói: Navidad (Día) ☀️",
        "victoria_titulo": "¡Felices fiestas!",
        "victoria": "¡Felices fiestas! Completaste el árbol a la luz del día."
    }
}
