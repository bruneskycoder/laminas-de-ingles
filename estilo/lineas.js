// Diagramas de línea de tiempo para el atlas de tiempos verbales.
// Un mismo código visual en todas las hojas:
//   ●            hecho completo (aspecto simple)
//   ● ● ●        hábito / repetición
//   banda azul   acción en curso, con duración (aspecto continuo)
//   arco ocre    conecta un hecho anterior con el momento de referencia (aspecto perfecto)
//   línea roja   AHORA
//   línea a trazos  ENTONCES: un momento de referencia pasado o futuro
//
// Uso en una hoja:
//   <svg class="linea" data-tiempo="present-perfect" style="width:70mm;height:16mm"></svg>
//   <script src="../../estilo/lineas.js"></script>
// El SVG usa un sistema de coordenadas de 100 × 24 unidades; la letra se calcula
// para que nunca quede por debajo de 8,5 pt, sea cual sea el ancho impreso.

(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const C = { negro: '#000000', azul: '#2458a6', ocre: '#9a5c16', rojo: '#d23c1e', gris: '#5f5f5f', grisClaro: '#bdbdbd' };
  const Y = 15;                     // altura del eje
  const P = 26, N = 55, F = 84;     // pasado de referencia, ahora, futuro de referencia

  // Con vector-effect non-scaling-stroke, stroke-width va en px CSS (1 mm = 3,78 px).
  function nuevo(svg, tag, attrs, texto) {
    const e = document.createElementNS(NS, tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (texto !== undefined) e.textContent = texto;
    svg.appendChild(e);
    return e;
  }

  function preparar(svg) {
    svg.setAttribute('viewBox', '0 0 100 24');
    svg.setAttribute('preserveAspectRatio', 'none');
    const anchoPx = svg.getBoundingClientRect().width || 300;
    const altoPx = svg.getBoundingClientRect().height || 72;
    // Unidades -> px en cada eje (preserveAspectRatio none: escalas distintas)
    const ex = anchoPx / 100, ey = altoPx / 24;
    const letraPx = (8.5 * 96) / 72;   // etiquetas de diagrama: metadato, 8,5 pt
    return { ex, ey, letra: letraPx / ey, achique: ey / ex };
  }

  // Texto que no se deforma aunque el SVG estire distinto en X e Y
  function texto(svg, m, x, y, contenido, opts = {}) {
    const t = nuevo(svg, 'text', {
      x: x / m.achique, y,
      'font-size': (opts.escala || 1) * m.letra,
      'text-anchor': opts.ancla || 'middle',
      fill: opts.color || C.negro,
      'font-weight': opts.peso || 400,
      transform: `scale(${m.achique},1)`,
    }, contenido);
    if (opts.cursiva) t.setAttribute('font-style', 'italic');
    return t;
  }

  function eje(svg, m, tenue) {
    nuevo(svg, 'line', { x1: 3, y1: Y, x2: 96, y2: Y, stroke: tenue ? C.grisClaro : C.negro, 'stroke-width': 1.2, 'vector-effect': 'non-scaling-stroke' });
    // punta de flecha hacia el futuro
    const ax = 97, ay = Y, l = 2.4 * m.achique, h = 1.3;
    nuevo(svg, 'path', { d: `M${ax - l} ${ay - h} L${ax} ${ay} L${ax - l} ${ay + h} Z`, fill: tenue ? C.grisClaro : C.negro });
  }

  function referencia(svg, m, x, tipo, etiqueta) {
    const esAhora = tipo === 'ahora';
    nuevo(svg, 'line', {
      x1: x, y1: 4.5, x2: x, y2: 21.5,
      stroke: esAhora ? C.rojo : C.negro,
      'stroke-width': esAhora ? 2.2 : 1.2,
      'stroke-dasharray': esAhora ? '' : '4 3',
      'vector-effect': 'non-scaling-stroke',
    });
    if (etiqueta !== '') texto(svg, m, x, 3.6, etiqueta || (esAhora ? 'ahora' : 'entonces'), { color: esAhora ? C.rojo : C.negro, peso: 700 });
  }

  function punto(svg, m, x, r = 1.5) {
    nuevo(svg, 'ellipse', { cx: x, cy: Y, rx: r * m.achique, ry: r, fill: C.negro });
  }

  function puntos(svg, m, desde, hasta, paso) {
    for (let x = desde; x <= hasta; x += paso) nuevo(svg, 'ellipse', { cx: x, cy: Y, rx: 0.95 * m.achique, ry: 0.95, fill: C.negro });
  }

  // Acción en curso: banda azul con ondas
  function banda(svg, m, x1, x2, abiertaIzq, abiertaDer) {
    nuevo(svg, 'rect', { x: x1, y: Y - 2.1, width: x2 - x1, height: 4.2, fill: '#bccde8', stroke: 'none' });
    let d = `M${x1} ${Y}`;
    const paso = 2.6;
    for (let x = x1; x < x2; x += paso) {
      const xm = Math.min(x + paso / 2, x2), xf = Math.min(x + paso, x2);
      d += ` Q${(x + xm) / 2} ${Y - 1.4} ${xm} ${Y} Q${(xm + xf) / 2} ${Y + 1.4} ${xf} ${Y}`;
    }
    nuevo(svg, 'path', { d, fill: 'none', stroke: C.azul, 'stroke-width': 1.1, 'vector-effect': 'non-scaling-stroke' });
    // extremos: cerrados (barra) o abiertos (degradé sugerido con trazos)
    if (!abiertaIzq) nuevo(svg, 'line', { x1, y1: Y - 2.1, x2: x1, y2: Y + 2.1, stroke: C.azul, 'stroke-width': 1.6, 'vector-effect': 'non-scaling-stroke' });
    if (!abiertaDer) nuevo(svg, 'line', { x1: x2, y1: Y - 2.1, x2, y2: Y + 2.1, stroke: C.azul, 'stroke-width': 1.6, 'vector-effect': 'non-scaling-stroke' });
  }

  // Conexión perfecta: arco ocre desde un hecho anterior hasta el momento de referencia
  function arco(svg, m, x1, x2, alto = 8) {
    const xm = (x1 + x2) / 2;
    nuevo(svg, 'path', { d: `M${x1} ${Y - 1.2} Q${xm} ${Y - alto * 2} ${x2 - 0.6} ${Y - 2.4}`, fill: 'none', stroke: C.ocre, 'stroke-width': 1.8, 'vector-effect': 'non-scaling-stroke' });
    const l = 2.2 * m.achique;
    nuevo(svg, 'path', { d: `M${x2 - l - 0.6} ${Y - 5.6} L${x2 - 0.4} ${Y - 2.2} L${x2 - l - 1.4} ${Y - 2.6} Z`, fill: C.ocre });
  }

  // Zona rayada: "cuándo, no importa" (tiempo no especificado)
  function zona(svg, m, x1, x2) {
    for (let x = x1; x < x2; x += 1.6) nuevo(svg, 'line', { x1: x, y1: Y + 3.6, x2: x + 1.2, y2: Y + 1.4, stroke: C.gris, 'stroke-width': 0.7, 'vector-effect': 'non-scaling-stroke' });
  }

  // Flecha recta (para going to: de la evidencia/plan de ahora al futuro)
  function flecha(svg, m, x1, x2, color = C.negro, y = Y - 5) {
    nuevo(svg, 'line', { x1, y1: y, x2: x2 - 1.5 * m.achique, y2: y, stroke: color, 'stroke-width': 1.2, 'stroke-dasharray': '3 2', 'vector-effect': 'non-scaling-stroke' });
    const l = 2 * m.achique;
    nuevo(svg, 'path', { d: `M${x2 - l} ${y - 1.2} L${x2} ${y} L${x2 - l} ${y + 1.2} Z`, fill: color });
  }

  // ---- Un dibujo por tiempo verbal ----
  const DIBUJOS = {
    'present-simple': (s, m) => { eje(s, m); puntos(s, m, 8, 92, 7); referencia(s, m, N, 'ahora'); },
    'present-continuous': (s, m) => { eje(s, m); banda(s, m, N - 11, N + 11, true, true); referencia(s, m, N, 'ahora'); },
    'present-perfect': (s, m) => { eje(s, m); zona(s, m, 8, N - 4); punto(s, m, 28); arco(s, m, 28, N); referencia(s, m, N, 'ahora'); },
    'present-perfect-continuous': (s, m) => { eje(s, m); banda(s, m, 22, N, false, false); arco(s, m, 22, N, 7); referencia(s, m, N, 'ahora'); },
    'past-simple': (s, m) => { eje(s, m); referencia(s, m, N, 'ahora'); punto(s, m, P + 4, 1.8); texto(s, m, P + 4, 22.5, 'terminado', { color: C.gris, cursiva: true }); },
    'past-continuous': (s, m) => { eje(s, m); referencia(s, m, N + 25, 'ahora'); banda(s, m, P - 12, P + 14, true, true); referencia(s, m, P + 2, 'entonces'); punto(s, m, P + 2, 1.5); },
    'past-perfect': (s, m) => { eje(s, m); referencia(s, m, N + 25, 'ahora'); punto(s, m, P - 12); arco(s, m, P - 12, P + 8); referencia(s, m, P + 8, 'entonces'); },
    'past-perfect-continuous': (s, m) => { eje(s, m); referencia(s, m, N + 25, 'ahora'); banda(s, m, P - 16, P + 8, false, false); arco(s, m, P - 16, P + 8, 7); referencia(s, m, P + 8, 'entonces'); },
    'future-simple': (s, m) => { eje(s, m); referencia(s, m, 30, 'ahora'); punto(s, m, F - 6, 1.8); texto(s, m, F - 6, 22.5, 'predicción', { color: C.gris, cursiva: true }); },
    'future-continuous': (s, m) => { eje(s, m); referencia(s, m, 22, 'ahora'); banda(s, m, F - 20, F + 8, true, true); referencia(s, m, F - 6, 'entonces'); },
    'future-perfect': (s, m) => { eje(s, m); referencia(s, m, 22, 'ahora'); punto(s, m, F - 26); arco(s, m, F - 26, F - 4); referencia(s, m, F - 4, 'entonces'); },
    'future-perfect-continuous': (s, m) => { eje(s, m); referencia(s, m, 22, 'ahora'); banda(s, m, 40, F - 4, false, false); arco(s, m, 40, F - 4, 7); referencia(s, m, F - 4, 'entonces'); },
    'going-to': (s, m) => { eje(s, m); referencia(s, m, 30, 'ahora'); flecha(s, m, 30, F - 6, C.negro, Y - 5.5); punto(s, m, F - 6, 1.8); texto(s, m, 30, 22.5, 'plan o evidencia', { color: C.gris, cursiva: true, ancla: 'start' }); },
    'present-for-future': (s, m) => { eje(s, m); referencia(s, m, 30, 'ahora'); flecha(s, m, 30, F - 6, C.azul, Y - 5.5); punto(s, m, F - 6, 1.8); texto(s, m, 30, 22.5, 'ya arreglado', { color: C.gris, cursiva: true, ancla: 'start' }); },
    'used-to': (s, m) => { eje(s, m); puntos(s, m, 8, 40, 5); referencia(s, m, N + 10, 'ahora'); texto(s, m, 72, 22.5, 'ya no', { color: C.gris, cursiva: true }); },
    // Para for / since / ago
    'for-since': (s, m) => { eje(s, m); banda(s, m, 22, N + 20, false, true); referencia(s, m, N + 20, 'ahora'); punto(s, m, 22, 1.6); texto(s, m, 22, 22.8, 'since March', { color: C.ocre, peso: 700 }); texto(s, m, (22 + N + 20) / 2, 8.3, 'for six months', { color: C.azul, peso: 700 }); },
    'ago': (s, m) => { eje(s, m); punto(s, m, 22, 1.6); referencia(s, m, N + 20, 'ahora'); flecha(s, m, N + 20 - 0.5, 23, C.negro, Y - 5.5); texto(s, m, (22 + N + 20) / 2, 4.5, 'two years ago', { peso: 700 }); },
  };

  function dibujar(svg) {
    const tipo = svg.dataset.tiempo;
    const f = DIBUJOS[tipo];
    if (!f) { console.error('lineas.js: tiempo desconocido', tipo); return; }
    const m = preparar(svg);
    f(svg, m);
  }

  // Leyenda de símbolos
  function leyenda(svg) {
    svg.setAttribute('viewBox', '0 0 100 24');
    svg.setAttribute('preserveAspectRatio', 'none');
    const m = preparar(svg);
    const L = m.letra;
    const fila = (y, dibujo, etiqueta) => { dibujo(y); texto(svg, m, 16, y + L * 0.35, etiqueta, { ancla: 'start' }); };
    const mini = (y, fn) => fn(y);
    fila(4, (y) => nuevo(svg, 'ellipse', { cx: 7, cy: y, rx: 1.4 * m.achique, ry: 1.4, fill: C.negro }), 'hecho completo');
    fila(10, (y) => { for (let i = 0; i < 3; i++) nuevo(svg, 'ellipse', { cx: 3 + i * 4, cy: y, rx: 0.9 * m.achique, ry: 0.9, fill: C.negro }); }, 'hábito, repetición');
    fila(16, (y) => nuevo(svg, 'rect', { x: 2, y: y - 1.8, width: 11, height: 3.6, fill: '#bccde8', stroke: C.azul, 'stroke-width': 1.1, 'vector-effect': 'non-scaling-stroke' }), 'en curso, con duración');
    fila(22, (y) => nuevo(svg, 'path', { d: `M2 ${y + 1} Q7.5 ${y - 4} 13 ${y + 1}`, fill: 'none', stroke: C.ocre, 'stroke-width': 1.8, 'vector-effect': 'non-scaling-stroke' }), 'conecta con un momento posterior');
  }

  function iniciar() {
    document.querySelectorAll('svg.linea[data-tiempo]').forEach(dibujar);
    document.querySelectorAll('svg.leyenda-lineas').forEach(leyenda);
  }
  window.Lineas = { iniciar, dibujar };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar);
  else iniciar();
})();
