// Renglones vectoriales para escribir a mano.
// <div class="escribir" data-renglones="5"></div> se llena con 5 renglones de 9 mm,
// cada uno con su casilla de corrección a la derecha. Se usan bordes reales
// (no degradés) para que todas las líneas salgan iguales en la impresión.
(function () {
  document.querySelectorAll('.escribir[data-renglones]').forEach((caja) => {
    const n = Number(caja.dataset.renglones) || 1;
    for (let i = 0; i < n; i++) {
      const r = document.createElement('div');
      r.className = 'renglon';
      r.appendChild(document.createElement('span'));
      r.appendChild(document.createElement('span'));
      caja.appendChild(r);
    }
  });
})();
