(function () {
  // Toasts
  const container = document.getElementById("toast-container");
  function toast(msg, type="ok", timeout=3000) {
    if (!container) return;
    const el = document.createElement("div");
    el.className = `toast ${type}`;
    el.textContent = msg;
    container.appendChild(el);
    setTimeout(() => { el.style.opacity = "0"; el.style.transform = "translateY(6px)"; }, timeout - 300);
    setTimeout(() => el.remove(), timeout);
  }
  window.showToast = toast;

  // Tabelas com atributo data-table-sort (se existirem)
  function sortTable(table, colIndex, type, asc) {
    const tbody = table.tBodies[0];
    const rows = Array.from(tbody.querySelectorAll("tr"));
    const parse = (v) => {
      if (type === "number") {
        const n = parseFloat((v || "").toString().replace(",", "."));
        return isNaN(n) ? Number.NEGATIVE_INFINITY : n;
      }
      return (v || "").toString().toLowerCase();
    };
    rows.sort((a, b) => {
      const va = parse(a.children[colIndex]?.textContent);
      const vb = parse(b.children[colIndex]?.textContent);
      if (va < vb) return asc ? -1 : 1;
      if (va > vb) return asc ? 1 : -1;
      return 0;
    });
    rows.forEach(r => tbody.appendChild(r));
  }

  document.querySelectorAll("table[data-table-sort]").forEach(table => {
    const ths = table.querySelectorAll("thead th");
    ths.forEach((th, idx) => {
      let asc = true;
      th.addEventListener("click", () => {
        ths.forEach(t => t.classList.remove("sort-asc", "sort-desc"));
        sortTable(table, idx, th.dataset.sort || "string", asc);
        th.classList.add(asc ? "sort-asc" : "sort-desc");
        asc = !asc;
      });
    });
  });

  // Feedback ao enviar formulários
  document.querySelectorAll("form").forEach(f => {
    f.addEventListener("submit", () => toast("Enviando...", "ok", 1500));
  });

  // Lê 'msg' da URL e mostra toast (se usado)
  (function() {
    const params = new URLSearchParams(window.location.search);
    const msg = params.get('msg');
    if (msg) {
      const map = { 'onibus_ok': 'Ônibus criado com sucesso!', 'erro': 'Ocorreu um erro. Tente novamente.' };
      toast(map[msg] || msg, "ok", 2500);
      const url = new URL(window.location);
      url.searchParams.delete('msg');
      window.history.replaceState({}, '', url);
    }
  })();
})();
