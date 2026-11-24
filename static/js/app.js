// app.js: Motor interactivo en Canvas con animaciones originales de vista_grafica.py

// 1. ESTADO GLOBAL
let estadoJuego = {
  discos: 3,
  torres: [[], [], []],
  movimientos: 0,
  minimo: 7,
  victoria: false,
  tema: "navidad_noche"
};

let resolviendo = false;
let origenSeleccionado = null; // Torre seleccionada para modo clic
let efectoMovimiento = null;   // { origen, destino, disco, progreso }
let tiempoAnimacion = 0;       // Contador global para partículas, luces y confeti

// Variables de arrastre (Drag & Drop)
let arrastre = {
  activo: false,
  disco: null,
  torreOrigen: null,
  x: 0,
  y: 0
};

// Partículas de ambiente (copos de nieve y estrellas)
let copos = [
  { rx: 0.04, ry: 0.12, r: 2 }, { rx: 0.08, ry: 0.38, r: 3 }, { rx: 0.14, ry: 0.22, r: 2 },
  { rx: 0.19, ry: 0.58, r: 4 }, { rx: 0.25, ry: 0.14, r: 3 }, { rx: 0.29, ry: 0.35, r: 2 },
  { rx: 0.35, ry: 0.20, r: 3 }, { rx: 0.39, ry: 0.50, r: 4 }, { rx: 0.44, ry: 0.28, r: 2 },
  { rx: 0.49, ry: 0.15, r: 3 }, { rx: 0.54, ry: 0.42, r: 3 }, { rx: 0.59, ry: 0.22, r: 2 },
  { rx: 0.64, ry: 0.60, r: 4 }, { rx: 0.69, ry: 0.16, r: 2 }, { rx: 0.73, ry: 0.36, r: 3 },
  { rx: 0.78, ry: 0.25, r: 2 }, { rx: 0.83, ry: 0.54, r: 3 }, { rx: 0.87, ry: 0.18, r: 4 },
  { rx: 0.92, ry: 0.30, r: 2 }, { rx: 0.96, ry: 0.48, r: 3 }
];

// Paletas idénticas a temas.py
const TEMAS = {
  navidad_noche: {
    nombre: "Navidad (Noche)",
    cielo: "#040B16",
    palo: "#C69214",
    paloActivo: "#FFE600",
    base: "#DCEBFA",
    baseSombra: "#1E293B",
    textoBase: "#0F172A",
    estrella: "#FACC15",
    estrellaBorde: "#CA8A04",
    discos: ["#EF4444", "#06B6D4", "#10B981", "#A855F7", "#F97316", "#CBD5E1", "#FACC15", "#FEF3C7"],
    textoDisco: ["#0F172A", "#0F172A", "#0F172A", "#0F172A", "#0F172A", "#0F172A", "#0F172A", "#0F172A"],
    titulo: "Torre de Hanói: Navidad (Noche) 🌙",
    victoriaTitulo: "¡Felices fiestas!",
    btnTema: "☀️ Cambiar a Modo Día"
  },
  navidad_dia: {
    nombre: "Navidad (Día)",
    cielo: "#7DD3FC",
    palo: "#78350F",
    paloActivo: "#EA580C",
    base: "#FFFFFF",
    baseSombra: "#94A3B8",
    textoBase: "#0F172A",
    estrella: "#F59E0B",
    estrellaBorde: "#92400E",
    discos: ["#DC2626", "#0369A1", "#16A34A", "#7C3AED", "#EA580C", "#475569", "#CA8A04", "#FEF08A"],
    textoDisco: ["#FFFFFF", "#FFFFFF", "#0F172A", "#FFFFFF", "#0F172A", "#FFFFFF", "#0F172A", "#0F172A"],
    titulo: "Torre de Hanói: Navidad (Día) ☀️",
    victoriaTitulo: "¡Felices fiestas!",
    btnTema: "🌙 Cambiar a Modo Noche"
  }
};

// Elementos del DOM
const canvas = document.getElementById("canvas-hanoi");
const ctx = canvas.getContext("2d");
const lblTitulo = document.getElementById("titulo-juego");
const valMovimientos = document.getElementById("valor-movimientos");
const valMinimo = document.getElementById("valor-minimo");
const badgeEstado = document.getElementById("badge-estado");
const hudMensaje = document.getElementById("hud-mensaje");
const selectDiscos = document.getElementById("select-discos");
const btnFullscreen = document.getElementById("btn-fullscreen");
const btnReiniciar = document.getElementById("btn-reiniciar");
const btnResolver = document.getElementById("btn-resolver");
const btnTema = document.getElementById("btn-tema");

// 2. COMUNICACIÓN CON EL SERVIDOR FLASK

async function cargarEstado() {
  try {
    const res = await fetch("/api/estado");
    const data = await res.json();
    estadoJuego = data;
    selectDiscos.value = data.discos;
    actualizarHUD();
  } catch (e) {
    console.error("Error al cargar estado:", e);
  }
}

async function reiniciarPartida(numDiscos) {
  resolviendo = false;
  origenSeleccionado = null;
  efectoMovimiento = null;
  const res = await fetch("/api/iniciar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ discos: numDiscos })
  });
  const data = await res.json();
  estadoJuego.discos = data.discos;
  estadoJuego.torres = data.torres;
  estadoJuego.movimientos = data.movimientos;
  estadoJuego.minimo = data.minimo;
  estadoJuego.victoria = false;

  mostrarMensaje("Juego reiniciado. Arrastra los discos o haz clic para mover.", "normal");
  actualizarHUD();
}

async function ejecutarMovimiento(origen, destino, animarParabola = true) {
  try {
    // Si la torre origen tiene disco, preparamos la animación parabólica original
    const pilaOrigen = estadoJuego.torres[origen];
    const discoAMover = (pilaOrigen && pilaOrigen.length > 0) ? pilaOrigen[pilaOrigen.length - 1] : null;

    const res = await fetch("/api/mover", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        origen,
        destino,
        juego: {
          discos: estadoJuego.discos,
          torres: estadoJuego.torres,
          movimientos: estadoJuego.movimientos
        }
      })
    });
    const data = await res.json();

    if (data.valido) {
      if (animarParabola && discoAMover !== null) {
        // Dispara la animación idéntica a vista_grafica.py (curva Math.sin)
        efectoMovimiento = {
          origen,
          destino,
          disco: discoAMover,
          progreso: 0.0
        };
      }

      estadoJuego.torres = data.torres;
      estadoJuego.movimientos = data.movimientos;
      estadoJuego.victoria = data.victoria;

      if (data.victoria) {
        mostrarMensaje(`¡Felices fiestas! Completaste el árbol en ${data.movimientos} movimientos.`, "victoria");
      } else {
        mostrarMensaje("Movimiento válido.", "normal");
      }
      actualizarHUD();
      return true;
    } else {
      mostrarMensaje(data.motivo, "error");
      return false;
    }
  } catch (e) {
    console.error("Error en movimiento:", e);
    return false;
  }
}

async function resolverAutomatico() {
  if (resolviendo) return;
  resolviendo = true;
  btnResolver.disabled = true;

  if (estadoJuego.movimientos > 0) {
    await reiniciarPartida(estadoJuego.discos);
  }

  mostrarMensaje("Resolviendo automáticamente mediante recursión...", "normal");

  const res = await fetch("/api/resolver", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ discos: estadoJuego.discos })
  });
  const data = await res.json();

  for (const paso of data.pasos) {
    if (!resolviendo) break;
    await ejecutarMovimiento(paso[0], paso[1], true);
    // Esperamos a que la animación de la parábola complete su salto
    await new Promise(r => setTimeout(r, 460));
  }

  resolviendo = false;
  btnResolver.disabled = false;
}

// 3. ACTUALIZACIÓN DEL HUD Y MENSAJES

function actualizarHUD() {
  valMovimientos.textContent = estadoJuego.movimientos;
  valMinimo.textContent = estadoJuego.minimo;

  if (estadoJuego.victoria) {
    badgeEstado.textContent = "ESTADO: ¡VICTORIA!";
    badgeEstado.className = "badge badge-estado victoria";
  } else if (resolviendo) {
    badgeEstado.textContent = "ESTADO: RESOLVIENDO";
    badgeEstado.className = "badge badge-estado jugando";
  } else {
    badgeEstado.textContent = "ESTADO: JUGANDO";
    badgeEstado.className = "badge badge-estado jugando";
  }
}

function mostrarMensaje(texto, tipo) {
  hudMensaje.textContent = texto;
  hudMensaje.className = "mensaje " + tipo;
}

function alternarTema() {
  if (estadoJuego.tema === "navidad_noche") {
    estadoJuego.tema = "navidad_dia";
    document.body.className = "tema-dia";
  } else {
    estadoJuego.tema = "navidad_noche";
    document.body.className = "tema-noche";
  }

  const t = TEMAS[estadoJuego.tema];
  lblTitulo.textContent = t.titulo;
  btnTema.textContent = t.btnTema;
}

// 4. MOTOR DE RENDERIZADO VISUAL (CANVAS)

function redimensionarCanvas() {
  const contenedor = document.getElementById("lienzo-contenedor");
  const dpr = window.devicePixelRatio || 1;
  const ancho = contenedor.clientWidth;
  const alto = contenedor.clientHeight;

  canvas.width = ancho * dpr;
  canvas.height = alto * dpr;
  ctx.scale(dpr, dpr);
}

function obtenerGeometria() {
  const w = canvas.clientWidth;
  const h = canvas.clientHeight;
  const yBase = h * 0.80;
  const yTope = h * 0.22;
  const postesX = [w * 0.22, w * 0.50, w * 0.78];
  return { w, h, yBase, yTope, postesX };
}

function dibujar() {
  tiempoAnimacion++;
  const { w, h, yBase, yTope, postesX } = obtenerGeometria();
  const tema = TEMAS[estadoJuego.tema];

  ctx.clearRect(0, 0, w, h);

  // A. Fondo del Cielo
  ctx.fillStyle = tema.cielo;
  ctx.fillRect(0, 0, w, h);

  // B. Elementos celestes (Sol / Luna y nieve/estrellas)
  if (estadoJuego.tema === "navidad_noche") {
    dibujarLuna(w * 0.10, h * 0.16);

    // Copos y estrellas nocturnas
    ctx.fillStyle = "#FFFFFF";
    copos.forEach((c, idx) => {
      const brillo = 0.5 + 0.5 * Math.sin((tiempoAnimacion + idx * 30) * 0.08);
      ctx.globalAlpha = brillo;
      ctx.beginPath();
      ctx.arc(c.rx * w, c.ry * h, c.r, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.globalAlpha = 1.0;
  } else {
    dibujarSol(w * 0.10, h * 0.16);
    dibujarNube(w * 0.40, h * 0.14, 1.1);
    dibujarNube(w * 0.88, h * 0.16, 0.9);

    // Copos suaves diurnos
    ctx.fillStyle = "#FFFFFF";
    ctx.globalAlpha = 0.7;
    copos.forEach((c) => {
      ctx.beginPath();
      ctx.arc(c.rx * w, c.ry * h, c.r * 0.8, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.globalAlpha = 1.0;
  }

  // C. Guirnalda de luces navideñas colgantes idéntica a vista_grafica.py
  dibujarGuirnaldaLuces(w);

  // D. Base de Nieve Ondulada
  dibujarBaseNieve(w, h, yBase, tema);

  // E. Postes de las tres torres con flecha indicadora
  const anchoPalo = 12;
  postesX.forEach((x, i) => {
    const esActivo = (origenSeleccionado === i);
    ctx.fillStyle = esActivo ? tema.paloActivo : tema.palo;
    ctx.strokeStyle = "#381D0B";
    ctx.lineWidth = 1.5;

    ctx.beginPath();
    ctx.roundRect(x - anchoPalo / 2, yTope, anchoPalo, yBase - yTope + 4, [6, 6, 0, 0]);
    ctx.fill();
    ctx.stroke();

    // Flecha roja indicadora sobre la torre seleccionada
    if (esActivo) {
      ctx.fillStyle = "#EF4444";
      ctx.strokeStyle = "#B91C1C";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(x, yTope - 8);
      ctx.lineTo(x - 10, yTope - 22);
      ctx.lineTo(x + 10, yTope - 22);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }
  });

  // F. Nombres de las torres
  const nombres = ["1 Origen", "2 Auxiliar", "3 Destino"];
  ctx.fillStyle = tema.textoBase;
  ctx.font = "bold 13px 'Segoe UI', sans-serif";
  ctx.textAlign = "center";
  postesX.forEach((x, i) => {
    ctx.fillText(nombres[i], x, yBase + 30);
  });

  // G. Cálculo de dimensiones de los discos
  const nDiscos = estadoJuego.discos;
  const altoDisco = Math.min(26, Math.max(16, (yBase - yTope) / (nDiscos + 2.5)));
  const separacion = altoDisco + 2;
  const anchoMax = Math.min(260, w * 0.25);
  const anchoMin = 64;
  const pasoAncho = (anchoMax - anchoMin) / Math.max(1, (nDiscos - 1));

  // H. Dibujar los discos en cada torre
  estadoJuego.torres.forEach((torre, torreIdx) => {
    const centroX = postesX[torreIdx];
    torre.forEach((disco, nivel) => {
      // Si se está arrastrando el tope de esta torre, no lo dibujamos fijo
      if (arrastre.activo && arrastre.torreOrigen === torreIdx && nivel === torre.length - 1) {
        return;
      }

      // Si está en plena animación parabólica hacia el destino, omitimos el tope destino
      if (efectoMovimiento !== null) {
        if (torreIdx === efectoMovimiento.destino && nivel === torre.length - 1 && disco === efectoMovimiento.disco) {
          return;
        }
      }

      const anchoD = anchoMin + (disco - 1) * pasoAncho;
      let y2 = yBase - (nivel * separacion);
      let y1 = y2 - altoDisco;

      // Si la torre está seleccionada, el disco de arriba se eleva 16px (detalle original)
      if (origenSeleccionado === torreIdx && nivel === torre.length - 1) {
        y1 -= 16;
        y2 -= 16;
      }

      const color = tema.discos[(disco - 1) % tema.discos.length];
      const colorTexto = tema.textoDisco[(disco - 1) % tema.textoDisco.length];
      dibujarCapsula(centroX - anchoD / 2, y1, centroX + anchoD / 2, y2, color, disco, colorTexto);
    });
  });

  // I. Animación Parabólica de Salto (Movimiento fluido entre torres)
  if (efectoMovimiento !== null) {
    const { origen, destino, disco, progreso } = efectoMovimiento;
    const xOrigen = postesX[origen];
    const xDestino = postesX[destino];
    const xMov = xOrigen + (xDestino - xOrigen) * progreso;
    const alturaSalto = Math.sin(progreso * Math.PI) * 90; // Curva idéntica a vista_grafica.py
    const yMov = yBase - 40 - alturaSalto;

    const anchoMov = anchoMin + (disco - 1) * pasoAncho;
    const colorMov = tema.discos[(disco - 1) % tema.discos.length];
    const colorTxt = tema.textoDisco[(disco - 1) % tema.textoDisco.length];

    dibujarCapsula(
      xMov - anchoMov / 2, yMov - altoDisco / 2,
      xMov + anchoMov / 2, yMov + altoDisco / 2,
      colorMov, disco, colorTxt, true
    );

    // Avanzar la animación paso a paso
    efectoMovimiento.progreso += 0.08;
    if (efectoMovimiento.progreso >= 1.0) {
      efectoMovimiento = null;
    }
  }

  // J. Disco Flotante arrastrado con el ratón
  if (arrastre.activo && arrastre.disco !== null) {
    const anchoDrag = anchoMin + (arrastre.disco - 1) * pasoAncho;
    const colorDrag = tema.discos[(arrastre.disco - 1) % tema.discos.length];
    const colorTxt = tema.textoDisco[(arrastre.disco - 1) % tema.textoDisco.length];
    dibujarCapsula(
      arrastre.x - anchoDrag / 2, arrastre.y - altoDisco / 2,
      arrastre.x + anchoDrag / 2, arrastre.y + altoDisco / 2,
      colorDrag, arrastre.disco, colorTxt, true
    );
  }

  // K. Animación de Victoria: Estrella Dorada Pulsante y Tormenta de Confeti
  if (estadoJuego.victoria) {
    const alturaArbol = estadoJuego.torres[2].length * separacion;
    const xEstrella = postesX[2];
    const yEstrella = yBase - alturaArbol - 38;

    // Halo pulsante
    const radioHalo = 30 + Math.sin(tiempoAnimacion * 0.1) * 6;
    ctx.strokeStyle = "#FACC15";
    ctx.lineWidth = 2.5;
    ctx.beginPath();
    ctx.arc(xEstrella, yEstrella, radioHalo, 0, Math.PI * 2);
    ctx.stroke();

    // Gran Estrella Navideña
    dibujarEstrellaNavidad(xEstrella, yEstrella, 24, 10, tema.estrella, tema.estrellaBorde);

    // Título de Victoria centrado
    ctx.fillStyle = tema.estrella;
    ctx.font = "bold 24px 'Segoe UI', sans-serif";
    ctx.textAlign = "center";
    ctx.fillText(tema.victoriaTitulo, w / 2, 85);

    // Lluvia de Confeti multicolor sobre la Torre 3 (círculos, cintas, estrellas, rectángulos)
    dibujarConfeti(xEstrella, yBase);
  }

  requestAnimationFrame(dibujar);
}

// 5. DETALLES GRÁFICOS Y ADORNOS DE DISCOS (DIBUJAR CÁPSULA ORIGINAL)

function dibujarCapsula(x1, y1, x2, y2, color, texto, colorTexto, flotando = false) {
  const ancho = x2 - x1;
  const alto = y2 - y1;
  const radio = Math.min(alto / 2, 8);
  const centroX = (x1 + x2) / 2;

  ctx.save();

  // Sombra proyectada inferior
  ctx.fillStyle = flotando ? "rgba(0,0,0,0.45)" : "rgba(0,0,0,0.25)";
  ctx.beginPath();
  ctx.ellipse(centroX, y2 + (flotando ? 8 : 2), ancho / 2 - 4, flotando ? 7 : 4, 0, 0, Math.PI * 2);
  ctx.fill();

  // Cuerpo redondeado de la cápsula
  ctx.fillStyle = color;
  ctx.strokeStyle = "#1F2937";
  ctx.lineWidth = 1.8;
  ctx.beginPath();
  ctx.roundRect(x1, y1, ancho, alto, radio);
  ctx.fill();
  ctx.stroke();

  // Reflejo blanco superior
  ctx.strokeStyle = "rgba(255, 255, 255, 0.75)";
  ctx.lineWidth = 1.8;
  ctx.beginPath();
  ctx.moveTo(x1 + radio + 6, y1 + 3);
  ctx.lineTo(x2 - radio - 6, y1 + 3);
  ctx.stroke();

  // Aro dorado superior de adorno navideño
  ctx.strokeStyle = "#FACC15";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(centroX, y1 - 4);
  ctx.lineTo(centroX, y1);
  ctx.stroke();

  // Pequeña medalla con símbolo navideño en el lado derecho
  const simbolos = ["●", "✦", "✿", "◆", "✹", "❄", "★", "✧"];
  const xAdorno = x2 - 14;
  const yAdorno = (y1 + y2) / 2;

  ctx.fillStyle = (texto % 2 === 0) ? "#FDE68A" : "#FFFFFF";
  ctx.strokeStyle = "#FACC15";
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.arc(xAdorno, yAdorno, 7, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = "#0F172A";
  ctx.font = "bold 9px 'Segoe UI Symbol', sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(simbolos[(texto - 1) % simbolos.length], xAdorno, yAdorno);

  // Número central del disco
  ctx.fillStyle = colorTexto;
  ctx.font = "bold 11px 'Segoe UI', sans-serif";
  ctx.textAlign = "center";
  ctx.textBaseline = "middle";
  ctx.fillText(texto, centroX, (y1 + y2) / 2);

  ctx.restore();
}

function dibujarBaseNieve(w, h, yBase, tema) {
  ctx.fillStyle = tema.base;
  ctx.strokeStyle = tema.baseSombra;
  ctx.lineWidth = 2;

  ctx.beginPath();
  ctx.moveTo(0, yBase + 6);
  ctx.bezierCurveTo(w * 0.25, yBase + 2, w * 0.50, yBase + 8, w, yBase + 6);
  ctx.lineTo(w, h);
  ctx.lineTo(0, h);
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
}

function dibujarGuirnaldaLuces(w) {
  const luces = ["#EF4444", "#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#EC4899", "#FFFFFF"];
  const numTramos = 12;
  const anchoTramo = w / numTramos;

  for (let i = 0; i < numTramos; i++) {
    const xInicio = i * anchoTramo;
    const xFin = (i + 1) * anchoTramo;
    const xMedio = (xInicio + xFin) / 2;
    const yCable = 16;
    const yCurva = 28;

    // Cable negro curvado
    ctx.strokeStyle = "#1E293B";
    ctx.lineWidth = 1.8;
    ctx.beginPath();
    ctx.moveTo(xInicio, yCable);
    ctx.quadraticCurveTo(xMedio, yCurva, xFin, yCable);
    ctx.stroke();

    // Foquito de color brillante
    const focoColor = luces[(i + Math.floor(tiempoAnimacion / 35)) % luces.length];
    ctx.fillStyle = focoColor;
    ctx.strokeStyle = "#FFFFFF";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.ellipse(xMedio, yCurva + 3, 4, 7, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }
}

function dibujarLuna(cx, cy) {
  ctx.save();
  ctx.fillStyle = "#FEF08A";
  ctx.shadowColor = "rgba(254, 240, 138, 0.6)";
  ctx.shadowBlur = 20;
  ctx.beginPath();
  ctx.arc(cx, cy, 26, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = "#040B16";
  ctx.shadowBlur = 0;
  ctx.beginPath();
  ctx.arc(cx + 8, cy - 5, 22, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function dibujarSol(cx, cy) {
  ctx.save();
  ctx.fillStyle = "#FBBF24";
  ctx.shadowColor = "rgba(251, 191, 36, 0.8)";
  ctx.shadowBlur = 24;
  ctx.beginPath();
  ctx.arc(cx, cy, 32, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function dibujarNube(cx, cy, escala = 1.0) {
  ctx.save();
  ctx.fillStyle = "rgba(255, 255, 255, 0.85)";
  ctx.beginPath();
  ctx.arc(cx, cy, 20 * escala, 0, Math.PI * 2);
  ctx.arc(cx + 20 * escala, cy - 8 * escala, 26 * escala, 0, Math.PI * 2);
  ctx.arc(cx + 45 * escala, cy, 22 * escala, 0, Math.PI * 2);
  ctx.fill();
  ctx.restore();
}

function dibujarEstrellaNavidad(cx, cy, rExt, rInt, colorRelleno, colorBorde) {
  ctx.save();
  ctx.fillStyle = colorRelleno;
  ctx.strokeStyle = colorBorde;
  ctx.lineWidth = 1.5;
  ctx.beginPath();
  for (let i = 0; i < 5; i++) {
    ctx.lineTo(
      Math.cos((18 + i * 72) * Math.PI / 180) * rExt + cx,
      -Math.sin((18 + i * 72) * Math.PI / 180) * rExt + cy
    );
    ctx.lineTo(
      Math.cos((54 + i * 72) * Math.PI / 180) * rInt + cx,
      -Math.sin((54 + i * 72) * Math.PI / 180) * rInt + cy
    );
  }
  ctx.closePath();
  ctx.fill();
  ctx.stroke();
  ctx.restore();
}

function dibujarConfeti(centroX, yBase) {
  const colores = ["#EF4444", "#FACC15", "#22C55E", "#38BDF8", "#A855F7"];
  const formas = ["rectangulo", "circulo", "estrella", "cinta"];

  for (let i = 0; i < 26; i++) {
    const x = centroX - 250 + ((i * 83 + tiempoAnimacion * 2) % 500);
    const y = 60 + ((i * 47 + tiempoAnimacion * 3) % Math.max(80, yBase - 100));
    const color = colores[i % colores.length];
    const forma = formas[i % formas.length];

    ctx.fillStyle = color;
    ctx.strokeStyle = color;

    if (forma === "circulo") {
      ctx.beginPath();
      ctx.arc(x, y, 3.5, 0, Math.PI * 2);
      ctx.fill();
    } else if (forma === "estrella") {
      dibujarEstrellaNavidad(x, y, 5, 2, color, color);
    } else if (forma === "cinta") {
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x + 8, y + 6);
      ctx.stroke();
    } else {
      ctx.fillRect(x, y, 8, 4);
    }
  }
}

// 6. EVENTOS DE INTERACCIÓN (ARRASTRE Y CLICS)

function obtenerTorreCercana(px) {
  const { postesX } = obtenerGeometria();
  let indice = -1;
  let distMinima = 9999;
  postesX.forEach((x, i) => {
    const dist = Math.abs(px - x);
    if (dist < 110 && dist < distMinima) {
      distMinima = dist;
      indice = i;
    }
  });
  return indice;
}

canvas.addEventListener("pointerdown", (e) => {
  if (resolviendo || estadoJuego.victoria) return;

  const rect = canvas.getBoundingClientRect();
  const px = e.clientX - rect.left;
  const py = e.clientY - rect.top;
  const torreIdx = obtenerTorreCercana(px);

  if (torreIdx !== -1 && estadoJuego.torres[torreIdx].length > 0) {
    const torre = estadoJuego.torres[torreIdx];
    const discoTope = torre[torre.length - 1];

    arrastre.activo = true;
    arrastre.disco = discoTope;
    arrastre.torreOrigen = torreIdx;
    arrastre.x = px;
    arrastre.y = py;
    canvas.classList.add("arrastrando");
  }
});

window.addEventListener("pointermove", (e) => {
  if (!arrastre.activo) return;
  const rect = canvas.getBoundingClientRect();
  arrastre.x = e.clientX - rect.left;
  arrastre.y = e.clientY - rect.top;
});

window.addEventListener("pointerup", async (e) => {
  if (!arrastre.activo) return;
  const rect = canvas.getBoundingClientRect();
  const px = e.clientX - rect.left;
  const torreDestino = obtenerTorreCercana(px);

  canvas.classList.remove("arrastrando");
  const origen = arrastre.torreOrigen;
  arrastre.activo = false;
  arrastre.disco = null;
  arrastre.torreOrigen = null;

  if (torreDestino !== -1 && torreDestino !== origen) {
    // Al soltar en destino válido, no necesita parábola porque ya fue arrastrado
    await ejecutarMovimiento(origen, torreDestino, false);
  }
});

// Clics directos: clic origen (se eleva el disco) -> clic destino (salta en parábola)
canvas.addEventListener("click", async (e) => {
  if (resolviendo || arrastre.activo || estadoJuego.victoria) return;

  const rect = canvas.getBoundingClientRect();
  const px = e.clientX - rect.left;
  const torreIdx = obtenerTorreCercana(px);
  if (torreIdx === -1) return;

  if (origenSeleccionado === null) {
    if (estadoJuego.torres[torreIdx].length > 0) {
      origenSeleccionado = torreIdx;
      mostrarMensaje(`Torre ${torreIdx + 1} seleccionada. Elige la torre destino.`, "normal");
    }
  } else {
    const origen = origenSeleccionado;
    origenSeleccionado = null;
    if (origen !== torreIdx) {
      await ejecutarMovimiento(origen, torreIdx, true);
    }
  }
});

// 7. LISTENERS DE CONTROLES
selectDiscos.addEventListener("change", (e) => {
  reiniciarPartida(parseInt(e.target.value));
});

btnReiniciar.addEventListener("click", () => {
  reiniciarPartida(parseInt(selectDiscos.value));
});

btnResolver.addEventListener("click", resolverAutomatico);
btnTema.addEventListener("click", alternarTema);

btnFullscreen.addEventListener("click", () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen();
    btnFullscreen.textContent = "✕ Salir Pantalla Completa (Esc)";
  } else {
    document.exitFullscreen();
    btnFullscreen.textContent = "⛶ Pantalla Completa (F11)";
  }
});

window.addEventListener("resize", redimensionarCanvas);

// INICIALIZACIÓN
window.addEventListener("DOMContentLoaded", async () => {
  redimensionarCanvas();
  await cargarEstado();
  requestAnimationFrame(dibujar);
});
