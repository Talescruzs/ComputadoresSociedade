(function () {
  const API = (window.API_BASE || "http://localhost:5000/api").replace(/\/+$/,'');

  async function getJSON(path) {
    try {
      const r = await fetch(API + path, { cache: "no-store" });
      if (!r.ok) return null;
      return await r.json();
    } catch {
      return null;
    }
  }

  function pearson(xs, ys) {
    const n = Math.min(xs.length, ys.length);
    if (n === 0) return NaN;
    let sx=0, sy=0, sxx=0, syy=0, sxy=0;
    for (let i=0;i<n;i++){
      const x=Number(xs[i]); const y=Number(ys[i]);
      if (!isFinite(x) || !isFinite(y)) continue;
      sx+=x; sy+=y; sxx+=x*x; syy+=y*y; sxy+=x*y;
    }
    const cov = sxy - (sx*sy/n);
    const vx = sxx - (sx*sx/n);
    const vy = syy - (sy*sy/n);
    const denom = Math.sqrt(vx*vy);
    return denom === 0 ? 0 : cov/denom;
  }

  function corrLabel(r) {
    if (!isFinite(r)) return "n/a";
    const a = Math.abs(r);
    const force = a > 0.8 ? "forte" : a > 0.5 ? "moderada" : a > 0.3 ? "fraca" : "muito fraca";
    const dir = r > 0 ? "positiva" : r < 0 ? "negativa" : "nula";
    return `${dir} ${force}`;
  }

  function renderCorrRow(name, r) {
    const tr = document.createElement("tr");
    tr.innerHTML = `<td>${name}</td><td>${(isFinite(r)? r.toFixed(3):'n/a')}</td><td>${corrLabel(r)}</td>`;
    const tb = document.getElementById("cor-table");
    if (tb) tb.appendChild(tr);
  }

  function renderHeatmap(matrix, horas, linhas) {
    const root = document.getElementById("heatmap");
    if (!root) return;
    const max = Math.max(...matrix.flat().map(v => +v || 0), 1);
    const table = document.createElement("table");
    table.className = "table";
    const thead = document.createElement("thead");
    const htr = document.createElement("tr");
    htr.innerHTML = `<th>Hora</th>` + linhas.map(l => `<th>${l}</th>`).join("");
    thead.appendChild(htr);
    table.appendChild(thead);
    const tbody = document.createElement("tbody");
    horas.forEach((h, i) => {
      const tr = document.createElement("tr");
      const tds = matrix[i].map(v => {
        const val = Number(v) || 0;
        const p = val / max;
        const color = `rgba(56,189,248,${0.15 + p * 0.6})`;
        return `<td style="background:${color}">${val.toFixed(1)}</td>`;
      }).join("");
      tr.innerHTML = `<td>${String(h).padStart(2,"0")}h</td>` + tds;
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    root.innerHTML = "";
    root.appendChild(table);
  }

  function makeChart(ctx, type, data, options) {
    return new Chart(ctx, { type, data, options });
  }

  (async function init() {
    const porLinha = await getJSON("/analytics/lotacao-por-linha");
    const porHora = await getJSON("/analytics/lotacao-horaria");

    // Gráfico: média por linha
    const ctxLinha = document.getElementById("chartLinha");
    if (Array.isArray(porLinha) && ctxLinha) {
      const labels = porLinha.map(x => x.linha_nome);
      const values = porLinha.map(x => Number(x.media_pessoas));
      makeChart(ctxLinha, "bar", {
        labels,
        datasets: [{ label: "Média de pessoas", data: values, borderColor: "#38bdf8", backgroundColor: "rgba(56,189,248,0.35)" }]
      }, {
        plugins: { legend: { labels: { color: "#111827" } } }
      });
    }

    // Gráfico: média por hora
    const ctxHora = document.getElementById("chartHora");
    if (Array.isArray(porHora) && ctxHora) {
      const labelsH = porHora.map(x => x.hora);
      const valuesH = porHora.map(x => Number(x.media_pessoas));
      makeChart(ctxHora, "line", {
        labels: labelsH.map(h => String(h).padStart(2,"0")+"h"),
        datasets: [{
          label: "Média de pessoas",
          data: valuesH,
          fill: false, tension: 0.25,
          borderColor: "#60a5fa", backgroundColor: "rgba(96,165,250,0.35)", pointRadius: 3
        }]
      }, { plugins: { legend: { labels: { color: "#111827" } } } });

      // Correlação: hora vs média
      const rHora = pearson(labelsH.map(Number), valuesH);
      renderCorrRow("Hora do dia × Lotação média", rHora);
    }

    // Heatmap Hora × Linha (aproximação com dados agregados)
    if (Array.isArray(porLinha) && Array.isArray(porHora)) {
      const horas = porHora.map(x => x.hora);
      const linhas = porLinha.map(x => x.linha_nome);
      const baseHora = porHora.map(x => Number(x.media_pessoas));
      const baseLinha = porLinha.map(x => Number(x.media_pessoas));
      const maxH = Math.max(...baseHora, 1);
      const maxL = Math.max(...baseLinha, 1);
      const matrix = horas.map((_, i) =>
        linhas.map((_, j) => (baseHora[i] / maxH) * (baseLinha[j] / maxL) * maxH)
      );
      renderHeatmap(matrix, horas, linhas);
    }

    window.showToast && window.showToast("Insights carregados", "ok", 1800);
  })();
})();
