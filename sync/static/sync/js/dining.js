const n = window.PHIL_N;
$(function() {
  const phils    = Array(n).fill(0);         // 0=thinking,1=hungry,2=eating
  const forks    = Array(n).fill(true);      // true=free, false=used
  let   current  = 0;                        // apuntador para step()

  // 1) Coloca filós y tenedores alrededor de la mesa
  function positionElements() {
    const center   = 250,
          radiusP  = 200,
          radiusF  = 170,
          sizeP    = 60,
          sizeF    = 30;
    for (let i = 0; i < n; i++) {
      // Filósofos
      const ang  = 2 * Math.PI / n * i,
            px   = center + radiusP * Math.cos(ang) - sizeP/2,
            py   = center + radiusP * Math.sin(ang) - sizeP/2;
      $('#phil-' + i).css({ left: px + 'px', top: py + 'px' });

      // Tenedores
      const ang2 = ang + Math.PI / n,
            fx   = center + radiusF * Math.cos(ang2) - sizeF/2,
            fy   = center + radiusF * Math.sin(ang2) - sizeF/2;
      $('#fork-' + i).css({ left: fx + 'px', top: fy + 'px' });
    }
  }

  // 2) Refresca colores según estados
  function updateDisplay() {
    for (let i = 0; i < n; i++) {
      $('#phil-' + i)
        .removeClass('thinking hungry eating')
        .addClass(
          phils[i] === 0 ? 'thinking' :
          phils[i] === 1 ? 'hungry'   :
                           'eating'
        );
      $('#fork-' + i)
        .removeClass('free used')
        .addClass(forks[i] ? 'free' : 'used');
    }
  }

  // 3) Un paso de la simulación
  function step() {
    const i = current;
    if (phils[i] === 0) {
      // thinking → hungry
      phils[i] = 1;
    } else if (phils[i] === 1) {
      // hungry → try take forks
      const left  = i,
            right = (i + 1) % n;
      if (forks[left] && forks[right]) {
        forks[left]  = false;
        forks[right] = false;
        phils[i]     = 2; // eating
      }
    } else {
      // eating → thinking + release forks
      const left  = i,
            right = (i + 1) % n;
      forks[left]  = true;
      forks[right] = true;
      phils[i]     = 0;
    }
    updateDisplay();
    current = (current + 1) % n;
  }

  // 4) Setup inicial + binds
  positionElements();
  updateDisplay();
  $('#next-step').on('click', step);
  $('#rnd').on('click', () => {
    const r = Math.floor(Math.random() * n) + 1;
    $('#rnd-output').text(`Philosopher ${r}`);
  });
});
