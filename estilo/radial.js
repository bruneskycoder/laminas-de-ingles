// Rayos del mapa radial (hojas ING-PV): une el núcleo con cada rama.
// Uso: <div class="radial"> … <div class="nucleo"> … <div class="rama"> … </div>
// Cada rayo sale del borde del círculo y llega al borde de la rama que mira
// al núcleo, a un cuarto de su ancho desde la esquina interior (así queda en
// diagonal, como un abanico). Se dibuja por debajo de las ramas.
(function () {
  const NS = 'http://www.w3.org/2000/svg';
  const MM = 96 / 25.4;
  const entre = (v, a, b) => Math.min(Math.max(v, a), b);

  document.querySelectorAll('.radial').forEach((cont) => {
    const nucleo = cont.querySelector('.nucleo');
    if (!nucleo) return;
    const caja = cont.getBoundingClientRect();
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('class', 'rayos');
    svg.setAttribute('width', caja.width);
    svg.setAttribute('height', caja.height);
    cont.insertBefore(svg, cont.firstChild);

    const rn = nucleo.getBoundingClientRect();
    const cx = rn.left + rn.width / 2 - caja.left, cy = rn.top + rn.height / 2 - caja.top;
    const radio = rn.width / 2;
    cont.querySelectorAll('.rama').forEach((rama) => {
      const r = rama.getBoundingClientRect();
      const izq = r.left - caja.left, der = r.right - caja.left;
      const x = der < cx ? der - r.width * 0.25 : izq > cx ? izq + r.width * 0.25 : entre(cx, izq, der);
      const y = entre(cy, r.top - caja.top, r.bottom - caja.top);
      const dx = x - cx, dy = y - cy, d = Math.hypot(dx, dy) || 1;
      const linea = document.createElementNS(NS, 'path');
      linea.setAttribute('d', `M${cx + (dx / d) * radio} ${cy + (dy / d) * radio} L${x} ${y}`);
      linea.setAttribute('stroke', '#000');
      linea.setAttribute('stroke-width', 0.45 * MM);
      svg.appendChild(linea);
      const punto = document.createElementNS(NS, 'circle');
      punto.setAttribute('cx', x);
      punto.setAttribute('cy', y);
      punto.setAttribute('r', 1.1 * MM);
      punto.setAttribute('fill', '#000');
      svg.appendChild(punto);
    });
  });
})();
