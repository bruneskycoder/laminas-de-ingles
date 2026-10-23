// Esquemas espaciales de las partículas (sentido literal), en una grilla de 48 × 32.
// Uso: <svg class="esquema" data-particula="up"></svg>
// Convención (la misma en todas las hojas ING-PV):
// - negro: la referencia (el piso, la caja, la superficie, el obstáculo);
// - azul: la cosa que se mueve (bola llena) y su recorrido (flecha);
// - gris punteado: dónde estaba la cosa antes de moverse.
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const AZUL = '#2458a6', GRIS = '#8a8a8a', NEGRO = '#000';
  const R = 3.2;

  const piso = (x1, x2, y) => ['path', { d: `M${x1} ${y} H${x2}`, stroke: NEGRO, 'stroke-width': 1.1 }];
  const bola = (cx, cy) => ['circle', { cx, cy, r: R, fill: AZUL }];
  const antes = (cx, cy) => ['circle', { cx, cy, r: R, fill: 'none', stroke: GRIS, 'stroke-width': 0.8, 'stroke-dasharray': '1.4 1' }];
  const flecha = (d) => ['path', { d, fill: 'none', stroke: AZUL, 'stroke-width': 1.3, 'marker-end': 'url(#punta-esquema)' }];

  const E = {
    up: [
      piso(8, 40, 29),
      ['path', { d: 'M12 3.5 H36', stroke: GRIS, 'stroke-width': 0.8, 'stroke-dasharray': '1.6 1.2' }],
      antes(24, 25.6), flecha('M24 21 V12.5'), bola(24, 7.6),
    ],
    down: [
      piso(8, 40, 29),
      antes(24, 6), flecha('M24 10.5 V19'), bola(24, 25.6),
    ],
    in: [
      ['path', { d: 'M22 6 H42 V28 H22', fill: 'none', stroke: NEGRO, 'stroke-width': 1.1 }],
      antes(7, 17), flecha('M11.5 17 H25.5'), bola(33, 17),
    ],
    out: [
      ['path', { d: 'M26 6 H6 V28 H26', fill: 'none', stroke: NEGRO, 'stroke-width': 1.1 }],
      antes(15, 17), flecha('M19.5 17 H33.5'), bola(41, 17),
    ],
    on: [
      ['rect', { x: 8, y: 21, width: 32, height: 5, fill: '#e6e6e6', stroke: NEGRO, 'stroke-width': 1.1 }],
      antes(9, 5.5), flecha('M12.4 8.2 L18.6 13.2'), bola(24, 17.7),
    ],
    off: [
      ['rect', { x: 8, y: 21, width: 32, height: 5, fill: '#e6e6e6', stroke: NEGRO, 'stroke-width': 1.1 }],
      antes(18, 17.7), flecha('M21.5 14.6 L31.2 8.4'), bola(38, 5.5),
    ],
    back: [
      piso(5, 43, 29),
      ['path', { d: 'M9 29 V24.5', stroke: NEGRO, 'stroke-width': 1.1 }],
      antes(9, 9), flecha('M13.5 9 H33 A6 6 0 0 1 33 21 H18'), bola(12.5, 21),
    ],
    over: [
      piso(4, 44, 29),
      ['rect', { x: 20, y: 15, width: 8, height: 14, fill: '#e6e6e6', stroke: NEGRO, 'stroke-width': 1.1 }],
      antes(8, 25.6), flecha('M10.5 21.5 Q24 -3 36.8 20.6'), bola(40, 25.6),
    ],
    away: [
      piso(4, 44, 29),
      ['path', { d: 'M8 29 V22', stroke: NEGRO, 'stroke-width': 1.1 }],
      antes(8, 17), flecha('M12.5 17 H33.5'), bola(41, 17),
      ['path', { d: 'M16 23.5 H19 M23 23.5 H26 M30 23.5 H33', stroke: GRIS, 'stroke-width': 0.8 }],
    ],
  };

  document.querySelectorAll('svg.esquema[data-particula]').forEach((svg) => {
    const partes = E[svg.dataset.particula];
    if (!partes) { console.error('particulas.js: no existe', svg.dataset.particula); return; }
    svg.setAttribute('viewBox', '0 0 48 32');
    svg.setAttribute('aria-hidden', 'true');
    const defs = document.createElementNS(NS, 'defs');
    defs.innerHTML = `<marker id="punta-esquema" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.6" markerHeight="3.6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="${AZUL}"/></marker>`;
    svg.appendChild(defs);
    for (const [tag, atr] of partes) {
      const el = document.createElementNS(NS, tag);
      for (const [k, v] of Object.entries(atr)) el.setAttribute(k, v);
      if (!atr.fill && tag === 'path') el.setAttribute('fill', 'none');
      el.setAttribute('stroke-linecap', 'round');
      el.setAttribute('stroke-linejoin', 'round');
      svg.appendChild(el);
    }
  });
})();
