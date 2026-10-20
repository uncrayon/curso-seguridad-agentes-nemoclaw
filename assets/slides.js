// Navegación: → (o espacio / Enter / clic) avanza, ← retrocede, Inicio/Fin, N = notas, F = pantalla completa.
// Si una diapositiva tiene pasos (elementos con data-paso="1", "2"…), cada avance muestra el siguiente
// paso antes de pasar a la siguiente diapositiva. Al volver atrás, la diapositiva aparece completa.
// La URL guarda la diapositiva actual (#5) para poder compartir un enlace directo.
(function () {
  const slides = [...document.querySelectorAll(".slide")];
  const counter = document.getElementById("counter");
  const bar = document.querySelector(".bar");
  let i = Math.min(Math.max((parseInt(location.hash.slice(1), 10) || 1) - 1, 0), slides.length - 1);
  let k = 0;   // pasos visibles en la diapositiva actual

  const pasosDe = (s) => [...new Set([...s.querySelectorAll("[data-paso]")].map((e) => +e.dataset.paso))].sort((a, b) => a - b);

  function pintaPasos() {
    const pasos = pasosDe(slides[i]);
    const hasta = pasos[k - 1] ?? 0;
    slides[i].querySelectorAll("[data-paso]").forEach((e) => {
      const p = +e.dataset.paso;
      e.classList.toggle("visto", p <= hasta);
      e.classList.toggle("actual", p === hasta);
    });
  }

  function show(n, completa = false) {
    i = Math.min(Math.max(n, 0), slides.length - 1);
    slides.forEach((s, j) => s.classList.toggle("on", j === i));
    k = completa ? pasosDe(slides[i]).length : 0;
    pintaPasos();
    if (counter) counter.textContent = `${i + 1} / ${slides.length}`;
    if (bar) bar.style.width = `${((i + 1) / slides.length) * 100}%`;
    history.replaceState(null, "", "#" + (i + 1));
  }

  function next() {
    if (k < pasosDe(slides[i]).length) { k++; pintaPasos(); }
    else if (i < slides.length - 1) show(i + 1);
  }

  function prev() {
    if (k > 0) { k--; pintaPasos(); }
    else if (i > 0) show(i - 1, true);
  }

  document.addEventListener("keydown", (e) => {
    if (e.metaKey || e.ctrlKey || e.altKey) return;
    const key = e.key;
    if (["ArrowRight", "PageDown", " ", "Enter"].includes(key)) { e.preventDefault(); next(); }
    else if (["ArrowLeft", "PageUp", "Backspace"].includes(key)) { e.preventDefault(); prev(); }
    else if (key === "Home") show(0);
    else if (key === "End") show(slides.length - 1, true);
    else if (key === "n" || key === "N") document.body.classList.toggle("show-notes");
    else if (key === "f" || key === "F") {
      if (document.fullscreenElement) document.exitFullscreen();
      else document.documentElement.requestFullscreen?.();
    }
  });
  document.addEventListener("click", (e) => {
    if (e.target.closest("a, pre, code, table, .notes")) return;
    if (e.clientX > innerWidth / 3) next(); else prev();
  });
  let x0 = null;
  document.addEventListener("touchstart", (e) => { x0 = e.touches[0].clientX; }, { passive: true });
  document.addEventListener("touchend", (e) => {
    if (x0 === null) return;
    const dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) { if (dx < 0) next(); else prev(); }
    x0 = null;
  });
  addEventListener("hashchange", () => {
    const n = parseInt(location.hash.slice(1), 10);
    if (n && n - 1 !== i) show(n - 1, true);
  });
  // Al imprimir, todos los pasos visibles
  addEventListener("beforeprint", () => document.querySelectorAll("[data-paso]").forEach((e) => e.classList.add("visto")));
  show(i, location.hash.length > 1);
})();
