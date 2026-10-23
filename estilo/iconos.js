// Pictogramas de línea, dibujados a mano en una grilla de 24 × 24.
// Uso: <svg class="icono" data-icono="avion"></svg>
// Trazo negro de grosor fijo; el acento (data-acento="rojo|azul|ocre") pinta
// solo las partes marcadas como "acento" de cada ícono.
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const COLOR = { rojo: '#d23c1e', azul: '#2458a6', ocre: '#9a5c16' };

  // Cada ícono: lista de [elemento, atributos, esAcento]
  const I = {
    avion: [
      ['path', { d: 'M3 11.2 H18.5 a1.6 0.8 0 0 1 0 1.6 H3 Z' }],
      ['path', { d: 'M10 11.2 L7 4 H8.8 L14.5 11.2' }],
      ['path', { d: 'M10 12.8 L7 20 H8.8 L14.5 12.8' }],
      ['path', { d: 'M4.5 11.2 L3 8 H4.3 L6.5 11.2 M4.5 12.8 L3 16 H4.3 L6.5 12.8' }],
    ],
    pasaporte: [
      ['rect', { x: 5.5, y: 3, width: 13, height: 18, rx: 1.4 }],
      ['circle', { cx: 12, cy: 10.5, r: 3.2 }, true],
      ['path', { d: 'M8.8 10.5 H15.2 M12 7.3 C10.6 9.2 10.6 11.8 12 13.7 C13.4 11.8 13.4 9.2 12 7.3' }, true],
      ['path', { d: 'M8.5 17 H15.5' }],
    ],
    valija: [
      ['rect', { x: 4, y: 8, width: 16, height: 12, rx: 1.5 }],
      ['path', { d: 'M9 8 V5.2 H15 V8 M8 8 V20 M16 8 V20' }],
    ],
    manzana: [
      ['path', { d: 'M12 8 C9 5.6 4.6 7 4.6 12 C4.6 16.5 7.6 20.5 9.8 20.5 C10.9 20.5 11.2 20 12 20 C12.8 20 13.1 20.5 14.2 20.5 C16.4 20.5 19.4 16.5 19.4 12 C19.4 7 15 5.6 12 8 Z' }, true],
      ['path', { d: 'M12 8 C12 6 12.8 4.2 14.5 3.5' }],
    ],
    salida: [
      ['path', { d: 'M13 4 H5 V20 H13' }],
      ['path', { d: 'M10 12 H21 M17.5 8.5 L21 12 L17.5 15.5' }, true],
    ],
    cama: [
      ['path', { d: 'M3 19 V7 M3 15 H21 V19 M21 15 V11.5 H11 V15' }],
      ['rect', { x: 4.6, y: 10.2, width: 4.4, height: 3 , rx: 0.8 }, true],
    ],
    llave: [
      ['circle', { cx: 7.5, cy: 12, r: 3.8 }],
      ['path', { d: 'M11.3 12 H21 M18 12 V15 M21 12 V14.5' }, true],
    ],
    casa: [
      ['path', { d: 'M3 11.5 L12 4 L21 11.5 M5.5 9.5 V20 H18.5 V9.5' }],
      ['rect', { x: 10, y: 14, width: 4, height: 6 }, true],
    ],
    taza: [
      ['path', { d: 'M5 9 H16 V14.5 A4.5 4.5 0 0 1 11.5 19 H9.5 A4.5 4.5 0 0 1 5 14.5 Z' }],
      ['path', { d: 'M16 10.5 H17.5 A2.2 2.2 0 0 1 17.5 14.9 H16' }],
      ['path', { d: 'M8.5 3.5 C7.5 4.5 9.5 5.5 8.5 6.8 M12 3.5 C11 4.5 13 5.5 12 6.8' }, true],
    ],
    carrito: [
      ['path', { d: 'M2.5 4 H5.5 L8 15.5 H18.5 L20.5 7.5 H6.6' }],
      ['circle', { cx: 9.5, cy: 19, r: 1.5 }, true],
      ['circle', { cx: 17, cy: 19, r: 1.5 }, true],
    ],
    etiqueta: [
      ['path', { d: 'M3.5 12 V4 H11.5 L20.5 13 L12.5 21 Z' }],
      ['circle', { cx: 7.5, cy: 8, r: 1.4 }, true],
    ],
    tarjeta: [
      ['rect', { x: 3, y: 6, width: 18, height: 12, rx: 1.5 }],
      ['path', { d: 'M3 9.8 H21' }, true],
      ['path', { d: 'M6 15 H11' }],
    ],
    banco: [
      ['path', { d: 'M3 9 L12 4 L21 9 Z' }, true],
      ['path', { d: 'M5.5 9.5 V17.5 M10 9.5 V17.5 M14 9.5 V17.5 M18.5 9.5 V17.5 M3 20 H21 M4 17.5 H20' }],
    ],
    documento: [
      ['path', { d: 'M6 3 H14 L18 7 V21 H6 Z M14 3 V7 H18' }],
      ['path', { d: 'M9 12 H15 M9 15 H15 M9 18 H13' }, true],
    ],
    salud: [
      ['path', { d: 'M9.5 3.5 H14.5 V9.5 H20.5 V14.5 H14.5 V20.5 H9.5 V14.5 H3.5 V9.5 H9.5 Z' }, true],
    ],
    telefono: [
      ['rect', { x: 7, y: 2.5, width: 10, height: 19, rx: 2 }],
      ['path', { d: 'M10.8 18.3 H13.2' }, true],
    ],
    bus: [
      ['rect', { x: 4, y: 4, width: 16, height: 13.5, rx: 2 }],
      ['path', { d: 'M4 11 H20 M8 14.5 H8.1 M16 14.5 H16.1' }],
      ['path', { d: 'M7 17.5 V20 M17 17.5 V20' }, true],
    ],
    charla: [
      ['path', { d: 'M3.5 5 H20.5 V15 H10.5 L6.5 19 V15 H3.5 Z' }],
      ['path', { d: 'M7.5 10 H7.6 M12 10 H12.1 M16.5 10 H16.6' }, true],
    ],
    reloj: [
      ['circle', { cx: 12, cy: 12, r: 8.5 }],
      ['path', { d: 'M12 7 V12 L15.5 14' }, true],
    ],
    remera: [
      ['path', { d: 'M8.5 3.5 L4 6.5 L6 10.5 L8 9.5 V20.5 H16 V9.5 L18 10.5 L20 6.5 L15.5 3.5 C14.5 5.5 9.5 5.5 8.5 3.5 Z' }],
      ['path', { d: 'M10.5 13 H13.5' }, true],
    ],
    pildora: [
      ['path', { d: 'M8.3 19.4 L19.4 8.3 A3.6 3.6 0 0 0 14.3 3.2 L3.2 14.3 A3.6 3.6 0 0 0 8.3 19.4 Z' }],
      ['path', { d: 'M8.75 8.75 L14.3 14.3' }, true],
    ],
    lupa: [
      ['circle', { cx: 10.5, cy: 10.5, r: 6 }],
      ['path', { d: 'M15 15 L20.5 20.5' }, true],
    ],
  };

  function dibujar(svg) {
    const nombre = svg.dataset.icono;
    const partes = I[nombre];
    if (!partes) { console.error('iconos.js: ícono desconocido', nombre); return; }
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('aria-hidden', 'true');
    const acento = COLOR[svg.dataset.acento] || '#000';
    for (const [tag, attrs, esAcento] of partes) {
      const e = document.createElementNS(NS, tag);
      for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
      e.setAttribute('fill', 'none');
      e.setAttribute('stroke', esAcento ? acento : '#000');
      e.setAttribute('stroke-width', '1.6');
      e.setAttribute('stroke-linecap', 'round');
      e.setAttribute('stroke-linejoin', 'round');
      svg.appendChild(e);
    }
  }
  document.querySelectorAll('svg.icono[data-icono]').forEach(dibujar);
})();
