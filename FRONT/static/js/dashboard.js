// Configuração da API (usa variável injetada ou fallback)
const API_URL = (window.API_BASE || `${location.protocol}//${location.hostname}:${(window.API_PORT || 5000)}/api`).replace(/\/+$/,'');

// Variáveis globais para os gráficos
let chartLotacaoPorLinha = null;
let chartLotacaoHoraria = null;
let chartLinhaHoraria = null;
let chartLinhaTrechos = null;

function updateTimestamp() {
  const now = new Date();
  const el = document.getElementById('lastUpdate');
  if (el) el.textContent = `Última atualização: ${now.toLocaleTimeString('pt-BR')}`;
}

async function fetchData(endpoint) {
  try {
    const response = await fetch(`${API_URL}${endpoint}`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error(`Erro ao buscar ${endpoint}:`, error);
    return null;
  }
}

// Tenta obter a rota ordenada da linha
async function fetchRouteForLine(idLinha) {
  try {
    const data = await fetchData(`/linhas/${idLinha}/rota`);
    if (Array.isArray(data) && data.length) {
      return data
        .map(x => {
          const ordem = (x.ordem != null ? Number(x.ordem) : null);
          const avg = (x.avg_minutos != null ? Number(x.avg_minutos) : null);
          return {
            id_parada: x.id_parada ?? null,
            nome: x.parada_nome ?? '',
            ordem,
            avg_minutos: (!isNaN(avg) ? avg : null)
          };
        })
        .sort((a, b) => {
          if (a.ordem == null || b.ordem == null) return 0;
          return a.ordem - b.ordem;
        });
    }
  } catch (e) {
    console.warn('Falha ao buscar rota da linha', idLinha, e);
  }
  return [];
}

// Preenche a tabela "Paradas na ordem da rota"
async function updateLinhaRotaTable(idLinha) {
  const tbody = document.getElementById('tabelaRotaLinha');
  if (!tbody) return;
  tbody.innerHTML = '<tr><td colspan="3" class="text-center">Carregando...</td></tr>';
  const rota = await fetchRouteForLine(idLinha);
  if (!rota || rota.length === 0) {
    tbody.innerHTML = '<tr><td colspan="3" class="text-center">Rota não encontrada para esta linha</td></tr>';
    return;
  }
  tbody.innerHTML = rota.map(r => {
    const ordemVis = (typeof r.ordem === 'number' ? r.ordem + 1 : '');
    // Usa média vinda da API; se ausente, aplica fallback ordem*5
    const minutosCalculados = (r.avg_minutos != null && !isNaN(r.avg_minutos))
      ? r.avg_minutos
      : (typeof r.ordem === 'number' ? r.ordem * 5 : null);
    const tempoTxt = (minutosCalculados != null ? `${minutosCalculados} min` : '—');
    return `
      <tr>
        <td>${ordemVis}</td>
        <td>${r.nome}</td>
        <td>${tempoTxt}</td>
      </tr>
    `;
  }).join('');
}

// --- Bloco: análise por linha selecionada ---

async function populateLinhasSelect() {
  const sel = document.getElementById('selectLinha');
  if (!sel) return;
  const linhas = await fetchData('/linhas') || [];
  sel.innerHTML = linhas.map(l => `<option value="${l.id_linha}">${l.nome}</option>`).join('');
  if (linhas.length > 0) {
    sel.value = linhas[0].id_linha;
    await updateLinhaCharts(linhas[0].id_linha);
    await updateLinhaRotaTable(linhas[0].id_linha); // novo: preenche tabela da rota
  }
  sel.addEventListener('change', async () => {
    await updateLinhaCharts(sel.value);
    await updateLinhaRotaTable(sel.value); // novo: atualiza tabela da rota
  });
}

async function updateLinhaCharts(idLinha) {
  idLinha = Number(idLinha);
  const [horaria, trechos] = await Promise.all([
    fetchData(`/analytics/linha/${idLinha}/horaria`),
    fetchData(`/analytics/linha/${idLinha}/trechos`)
  ]);

  // Gráfico: lotação por hora para a linha
  const ctxH = document.getElementById('chartLinhaHoraria')?.getContext('2d');
  if (ctxH) {
    if (chartLinhaHoraria) chartLinhaHoraria.destroy();
    const labels = (horaria || []).map(d => `${d.hora}:00`);
    const values = (horaria || []).map(d => Number(d.media_pessoas));
    chartLinhaHoraria = new Chart(ctxH, {
      type: 'line',
      data: { labels, datasets: [{
        label: 'Média por hora (linha selecionada)',
        data: values, borderColor: '#0ea5e9', backgroundColor: 'rgba(14,165,233,.2)',
        borderWidth: 3, fill: true, tension: .35
      }]},
      options: {
        responsive: true, maintainAspectRatio: false,
        scales: {
          y: { beginAtZero: true, title: { display: true, text: 'Pessoas' } },
          x: { title: { display: true, text: 'Hora' } }
        },
        plugins: { legend: { display: true, position: 'top' } }
      }
    });
  }

  // Gráfico: trechos da linha (ordenado pela rota da linha)
  const ctxT = document.getElementById('chartLinhaTrechos')?.getContext('2d');
  if (ctxT) {
    if (chartLinhaTrechos) chartLinhaTrechos.destroy();

    let labels = [];
    let values = [];
    let usedRouteOrder = false;

    // Busca a rota e ordena os trechos conforme parada[i] -> parada[i+1]
    const rota = await fetchRouteForLine(idLinha);
    if (rota && rota.length >= 2 && Array.isArray(trechos)) {
      // Indexa o analytics por par NomeOrigem>>>NomeDestino
      const mapTrechos = new Map(
        trechos.map(t => [`${t.parada_origem}>>>${t.parada_destino}`, Number(t.media_pessoas)])
      );
      for (let i = 0; i < rota.length - 1; i++) {
        const o = rota[i]?.nome || '';
        const d = rota[i + 1]?.nome || '';
        const key = `${o}>>>${d}`;
        const v = mapTrechos.has(key) ? mapTrechos.get(key) : 0;
        labels.push(`${o} → ${d}`);
        values.push(v);
      }
      usedRouteOrder = true;
    } else if (Array.isArray(trechos)) {
      // Fallback: top 10 por média (comportamento anterior)
      const top = trechos.slice(0, 10);
      labels = top.map(t => `${t.parada_origem} → ${t.parada_destino}`);
      values = top.map(t => Number(t.media_pessoas));
    }

    chartLinhaTrechos = new Chart(ctxT, {
      type: 'bar',
      data: { labels, datasets: [{
        label: usedRouteOrder ? 'Média de Pessoas (ordem da rota)' : 'Média de Pessoas (top trechos)',
        data: values, backgroundColor: 'rgba(234,179,8,.6)', borderColor: 'rgba(234,179,8,1)', borderWidth: 2
      }]},
      options: {
        indexAxis: 'y', responsive: true, maintainAspectRatio: false,
        scales: { x: { beginAtZero: true, title: { display: true, text: 'Pessoas' } } },
        plugins: { legend: { display: false } }
      }
    });
  }

  // Destaque: trecho mais lotado
  const highlight = document.getElementById('linhaHighlight');
  if (highlight) {
    if (trechos && trechos.length) {
      // escolher pelo maior max_pessoas (prioriza picos)
      const best = [...trechos].sort((a,b) => Number(b.max_pessoas) - Number(a.max_pessoas))[0];
      highlight.style.display = '';
      highlight.className = 'alert alert-warning mb-3';
      highlight.innerHTML = `
        <strong>Trecho mais lotado:</strong> ${best.parada_origem} → ${best.parada_destino || 'Fim'}
        &nbsp;|&nbsp; <strong>Média:</strong> ${Number(best.media_pessoas).toFixed(1)}
        &nbsp;|&nbsp; <strong>Pico:</strong> ${best.max_pessoas}
        &nbsp;|&nbsp; <strong>Registros:</strong> ${best.total_registros}
      `;
    } else {
      highlight.style.display = 'none';
    }
  }
}

// --- Fim do bloco de análise por linha ---

async function updateSummaryCards() {
  const [linhas, onibus, viagens, paradas] = await Promise.all([
    fetchData('/linhas'), fetchData('/onibus'), fetchData('/viagens'), fetchData('/paradas')
  ]);
  if (linhas) document.getElementById('totalLinhas').textContent = linhas.length;
  if (onibus) document.getElementById('totalOnibus').textContent = onibus.length;
  if (paradas) document.getElementById('totalParadas').textContent = paradas.length;
  if (viagens) {
    const ativas = viagens.filter(v => v.status === 'Ativo').length; // alterado
    document.getElementById('viagensAtivas').textContent = ativas;
  }
}

async function updateChartLotacaoPorLinha() {
  // Buscar analytics + metadados + registros para calcular max real por trecho
  const [analytics, onibus, viagens, lotacoes] = await Promise.all([
    fetchData('/analytics/lotacao-por-linha'),
    fetchData('/onibus'),
    fetchData('/viagens'),
    fetchData('/lotacao')
  ]);
  if (!analytics || analytics.length === 0) return;

  // Map capacidade por ônibus
  const capPorOnibus = new Map((onibus || []).map(o => [o.id_onibus, Number(o.capacidade || 0)]));
  // Capacidade média por linha (para média relativa)
  const capsPorLinha = new Map(); // linha_nome -> { soma, count }
  (viagens || []).forEach(v => {
    const nome = v.linha_nome || '';
    const cap = capPorOnibus.get(v.id_onibus) || 0;
    if (!nome || cap <= 0) return;
    const agg = capsPorLinha.get(nome) || { soma:0, count:0 };
    agg.soma += cap; agg.count += 1;
    capsPorLinha.set(nome, agg);
  });
  const capsAll = (onibus || []).map(o => Number(o.capacidade || 0)).filter(x => x > 0);
  const capFallback = capsAll.length ? Math.round(capsAll.reduce((a,b)=>a+b,0)/capsAll.length) : 60;
  function capRefLinha(nome) {
    const agg = capsPorLinha.get(nome);
    if (agg && agg.count > 0) return Math.max(1, Math.round(agg.soma / agg.count));
    return capFallback;
  }

  // Mapa para máximo relativo (em %) e viagem associada
  const viagemPorId = new Map((viagens||[]).map(v => [v.id_viagem, v]));
  const maxPorLinha = new Map(); // linha_nome -> { pct, viagem_id, qtd, cap }
  for (const reg of (lotacoes||[])) {
    const v = viagemPorId.get(reg.id_viagem);
    if (!v) continue;
    const linha = v.linha_nome || '';
    if (!linha) continue;
    const cap = capPorOnibus.get(v.id_onibus) || 0;
    const qtd = Number(reg.qtd_pessoas || 0);
    const pct = cap > 0 ? (qtd / cap) * 100 : 0;
    const cur = maxPorLinha.get(linha);
    if (!cur || pct > cur.pct) {
      maxPorLinha.set(linha, { pct, viagem_id: v.id_viagem, qtd, cap });
    }
  }

  const labels = analytics.map(d => d.linha_nome);
  const mediasPct = analytics.map(d => {
    const cap = capRefLinha(d.linha_nome);
    const val = Number(d.media_pessoas || 0);
    return cap > 0 ? (val / cap) * 100 : 0;
  });
  // Máximo relativo (%) – se não encontrado na varredura, usa fallback analytics.max_pessoas/capRefLinha
  const maxPct = labels.map(nome => {
    const info = maxPorLinha.get(nome);
    if (info) return info.pct;
    const fallbackAbs = Number((analytics.find(a=>a.linha_nome===nome)?.max_pessoas) || 0);
    const cap = capRefLinha(nome);
    return cap > 0 ? (fallbackAbs / cap) * 100 : 0;
  });
  const maxViagemIds = labels.map(nome => {
    const info = maxPorLinha.get(nome);
    return info ? info.viagem_id : null;
  });

  const ctx = document.getElementById('chartLotacaoPorLinha').getContext('2d');
  if (chartLotacaoPorLinha) chartLotacaoPorLinha.destroy();
  chartLotacaoPorLinha = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: 'Ocupação média (%)',
          data: mediasPct,
          backgroundColor: 'rgba(54,162,235,.6)',
          borderColor: 'rgba(54,162,235,1)',
          borderWidth: 2
        },
        {
          label: 'Ocupação máxima (%)',
          data: maxPct,
          backgroundColor: 'rgba(255,99,132,.6)',
          borderColor: 'rgba(255,99,132,1)',
          borderWidth: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      interaction: { mode: 'nearest', intersect: true },
      scales: {
        y: {
          beginAtZero: true,
          max: 200,
          title: { display: true, text: '% Ocupação' },
          ticks: { callback: v => `${v}%` }
        }
      },
      plugins: {
        legend: { display: true, position: 'top' },
        tooltip: {
          callbacks: {
            label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y.toFixed(1)}%`,
            afterBody: (items) => {
              if (!items || !items.length) return;
              const item = items[0];
              if (item.dataset.label.includes('máxima')) {
                const idx = item.dataIndex;
                const vid = maxViagemIds[idx];
                if (vid) return `Clique na barra para abrir a viagem #${vid}`;
              } else if (item.dataset.label.includes('média')) {
                const idx = item.dataIndex;
                const nome = labels[idx];
                if (nome) return `Clique na barra para abrir detalhes da linha "${nome}"`;
              }
              return '';
            }
          }
        }
      },
      onClick: (evt, elements) => {
        if (!elements || !elements.length) return;
        const el = elements[0];
        const ds = chartLotacaoPorLinha.data.datasets[el.datasetIndex];
        if (ds.label.includes('máxima')) {
          const vid = maxViagemIds[el.index];
          if (vid) window.location.href = `/viagens-detalhes/${vid}`;
        } else if (ds.label.includes('média')) {
          const nome = labels[el.index];
          if (nome) window.location.href = `/linhas-detalhes?linha=${encodeURIComponent(nome)}`;
        }
      }
    }
  });
}

async function updateChartLotacaoHoraria() {
  const registros = await fetchData('/lotacao');
  if (!Array.isArray(registros) || !registros.length) return;

  const somaPorHora = new Map(); // hora -> soma de pessoas
  for (const reg of registros) {
    const dt = new Date(reg.data_hora);
    if (isNaN(dt.getTime())) continue;
    const h = dt.getHours();
    const qtd = Number(reg.qtd_pessoas || 0);
    somaPorHora.set(h, (somaPorHora.get(h) || 0) + (Number.isFinite(qtd) ? qtd : 0));
  }

  const horas = Array.from(somaPorHora.keys()).sort((a,b)=>a-b);
  const labels = horas.map(h => `${String(h).padStart(2,'0')}:00`);
  const values = horas.map(h => somaPorHora.get(h));

  const ctx = document.getElementById('chartLotacaoHoraria').getContext('2d');
  if (chartLotacaoHoraria) chartLotacaoHoraria.destroy();
  chartLotacaoHoraria = new Chart(ctx, {
    type: 'line',
    data: {
      labels,
      datasets: [{
        label: 'Total de Pessoas por Horário (soma)',
        data: values,
        backgroundColor: 'rgba(75,192,192,.25)',
        borderColor: 'rgba(75,192,192,1)',
        borderWidth: 3,
        fill: true,
        tension: .35
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Total de Pessoas' } },
        x: { title: { display: true, text: 'Horário do Dia' } }
      },
      plugins: {
        legend: { display: true, position: 'top' },
        tooltip: {
          callbacks: {
            label: ctx => `Total: ${ctx.parsed.y}`
          }
        }
      }
    }
  });
}

async function updateHeatmapHoraLinha() {
  const [porLinha, porHora] = await Promise.all([
    fetchData('/analytics/lotacao-por-linha'),
    fetchData('/analytics/lotacao-horaria')
  ]);
  const root = document.getElementById('heatmapDashboard');
  if (!root) return;
  if (!Array.isArray(porLinha) || !porLinha.length || !Array.isArray(porHora) || !porHora.length) {
    root.innerHTML = '<div class="text-center text-muted small">Dados insuficientes para o heatmap.</div>';
    return;
  }

  const horas = porHora.map(x => x.hora);
  const linhas = porLinha.map(x => x.linha_nome);
  const baseHora = porHora.map(x => Number(x.media_pessoas) || 0);
  const baseLinha = porLinha.map(x => Number(x.media_pessoas) || 0);
  const maxH = Math.max(...baseHora, 1);
  const maxL = Math.max(...baseLinha, 1);
  const matriz = horas.map((_h, hi) =>
    linhas.map((_l, li) => (baseHora[hi] / maxH) * (baseLinha[li] / maxL) * maxH)
  );
  const maxVal = Math.max(...matriz.flat(), 1);

  // Tabela sem listras por linha; cada célula receberá seu próprio background
  let html = '<table class="table table-sm align-middle" style="min-width:680px; border-collapse:separate; border-spacing:0">';
  html += '<thead><tr><th style="position:sticky;top:0;z-index:1;background:#0f172a;color:#fff">Hora</th>' +
          linhas.map(l => `<th style="position:sticky;top:0;z-index:1;background:#0f172a;color:#fff">${l}</th>`).join('') +
          '</tr></thead><tbody>';
  horas.forEach((h, hi) => {
    html += `<tr><td style="background:#0b1020;color:#e5e7eb;position:sticky;left:0;z-index:1">${String(h).padStart(2,'0')}h</td>`;
    matriz[hi].forEach((val, li) => {
      const v = Number(val) || 0;
      const p = v / maxVal;
      const bg = `rgba(56,189,248,${(0.12 + p * 0.7).toFixed(3)})`;
      const fg = p >= 0.6 ? '#fff' : '#0b1020';
      const br = `rgba(255,255,255,${0.08 + p * 0.12})`;
      const horaStr = String(h).padStart(2,'0');
      const linhaNome = linhas[li];
      const titulo = `${linhaNome} @ ${horaStr}:00 — ${v.toFixed(1)} pessoas (clique para filtrar viagens)`;
      html += `<td class="heat-cell" data-hora="${horaStr}" data-linha="${encodeURIComponent(linhaNome)}" title="${titulo}" style="cursor:pointer;background:${bg};color:${fg};border:1px solid ${br};text-align:center;min-width:64px">${v.toFixed(1)}</td>`;
    });
    html += '</tr>';
  });
  html += '</tbody></table>';
  root.innerHTML = html;

  // Handler de clique nas células
  root.querySelectorAll('.heat-cell').forEach(td => {
    td.addEventListener('click', () => {
      const hora = td.getAttribute('data-hora'); // HH
      const linhaEnc = td.getAttribute('data-linha'); // já encodeURIComponent
      // Redireciona para detalhes das viagens com filtros de linha e hora
      window.location.href = `/viagens-detalhes?linha=${linhaEnc}&horaDe=${hora}:00&horaAte=${hora}:00`;
    });
  });
}

// Substitui a função por uma versão enxuta que usa os helpers acima
async function updateDashboard() {
  updateTimestamp();
  await updateSummaryCards();
  await updateChartLotacaoPorLinha();
  await updateChartLotacaoHoraria();
  await populateLinhasSelect();
  await updateHeatmapHoraLinha(); // novo
}

document.addEventListener('DOMContentLoaded', () => {
  updateDashboard();
  setInterval(updateDashboard, 30000);
});
