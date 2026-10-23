// Flechas entre cajas HTML (diagramas de flujo).
// Uso:
//   <div class="flujo"> ... cajas con id ... </div>
//   <script src="../../estilo/conectores.js"></script>
//   <script>Conectores.dibujar('.flujo', [['a', 'b', 'sí'], ['a', 'c', 'no', 'h']]);</script>
// Modo 'v' (por defecto): sale por abajo y entra por arriba.
// Modo 'h': sale por la derecha y entra por la izquierda.
// Los tramos son rectos (como en un plano) y la etiqueta va junto al tramo final.
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const MM = 96 / 25.4;

  function dibujar(selector, conexiones, opciones = {}) {
    const cont = document.querySelector(selector);
    if (!cont) return;
    if (getComputedStyle(cont).position === 'static') cont.style.position = 'relative';
    const caja = cont.getBoundingClientRect();
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('width', caja.width);
    svg.setAttribute('height', caja.height);
    svg.style.position = 'absolute';
    svg.style.left = '0';
    svg.style.top = '0';
    svg.style.pointerEvents = 'none';
    svg.style.overflow = 'visible';
    cont.insertBefore(svg, cont.firstChild);
    const color = opciones.color || '#000';
    const grosor = (opciones.grosorMm || 0.3) * MM;

    const defs = document.createElementNS(NS, 'defs');
    defs.innerHTML = `<marker id="punta-flujo" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="${color}"/></marker>`;
    svg.appendChild(defs);

    const rel = (el) => {
      const r = el.getBoundingClientRect();
      return { x: r.left - caja.left, y: r.top - caja.top, w: r.width, h: r.height };
    };

    for (const [desde, hasta, etiqueta, modo = 'v'] of conexiones) {
      const a = document.getElementById(desde), b = document.getElementById(hasta);
      if (!a || !b) { console.error('conectores.js: falta', desde, hasta); continue; }
      const ra = rel(a), rb = rel(b);
      let d, tx, ty;
      if (modo === 'h') {
        const x1 = ra.x + ra.w, y1 = ra.y + ra.h / 2;
        const x2 = rb.x, y2 = rb.y + rb.h / 2;
        const xm = x1 + Math.max(4, (x2 - x1) * 0.4);
        d = Math.abs(y1 - y2) < 1 ? `M${x1} ${y1} L${x2 - 1} ${y2}` : `M${x1} ${y1} L${xm} ${y1} L${xm} ${y2} L${x2 - 1} ${y2}`;
        tx = Math.abs(y1 - y2) < 1 ? x1 + 0.8 * MM : xm + 0.8 * MM; ty = y2 - 1.2 * MM;
      } else {
        const x1 = ra.x + ra.w / 2, y1 = ra.y + ra.h;
        const x2 = rb.x + rb.w / 2, y2 = rb.y;
        const ym = y1 + Math.max(6, (y2 - y1) * 0.45);
        d = Math.abs(x1 - x2) < 1 ? `M${x1} ${y1} L${x2} ${y2 - 1}` : `M${x1} ${y1} L${x1} ${ym} L${x2} ${ym} L${x2} ${y2 - 1}`;
        tx = x2 + 1.2 * MM; ty = (ym + y2) / 2 + 3.5;
      }
      const p = document.createElementNS(NS, 'path');
      p.setAttribute('d', d);
      p.setAttribute('fill', 'none');
      p.setAttribute('stroke', color);
      p.setAttribute('stroke-width', grosor);
      p.setAttribute('marker-end', 'url(#punta-flujo)');
      svg.appendChild(p);
      if (etiqueta) {
        const t = document.createElementNS(NS, 'text');
        t.setAttribute('x', tx);
        t.setAttribute('y', ty);
        t.setAttribute('font-size', (9.5 * 96) / 72);
        t.setAttribute('font-weight', '700');
        t.setAttribute('fill', color);
        t.textContent = etiqueta;
        svg.appendChild(t);
      }
    }
  }
  window.Conectores = { dibujar };
})();
