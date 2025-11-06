// Configuração da API (usa variável injetada ou fallback)
const API_URL = (window.API_BASE || `${location.protocol}//${location.hostname}:${(window.API_PORT || 5000)}/api`).replace(/\/+$/,'');

// Variáveis globais para os gráficos
let chartLotacaoPorLinha = null;
let chartLotacaoHoraria = null;
let chartTrechosLotados = null;
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
  const data = await fetchData('/analytics/lotacao-por-linha');
  if (!data || data.length === 0) return;
  const ctx = document.getElementById('chartLotacaoPorLinha').getContext('2d');
  if (chartLotacaoPorLinha) chartLotacaoPorLinha.destroy();
  chartLotacaoPorLinha = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.map(d => d.linha_nome),
      datasets: [
        { label: 'Média de Pessoas', data: data.map(d => Number(d.media_pessoas)), backgroundColor: 'rgba(54,162,235,.6)', borderColor: 'rgba(54,162,235,1)', borderWidth: 2 },
        { label: 'Máximo de Pessoas', data: data.map(d => Number(d.max_pessoas)), backgroundColor: 'rgba(255,99,132,.6)', borderColor: 'rgba(255,99,132,1)', borderWidth: 2 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: true,
      scales: { y: { beginAtZero: true, title: { display: true, text: 'Número de Pessoas' } } },
      plugins: {
        legend: { display: true, position: 'top' },
        tooltip: {
          callbacks: {
            afterLabel: (ctx) => `Total de registros: ${data[ctx.dataIndex].total_registros}`
          }
        }
      }
  }
  });
}

async function updateChartLotacaoHoraria() {
  const data = await fetchData('/analytics/lotacao-horaria');
  if (!data || data.length === 0) return;
  const ctx = document.getElementById('chartLotacaoHoraria').getContext('2d');
  if (chartLotacaoHoraria) chartLotacaoHoraria.destroy();
  chartLotacaoHoraria = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.map(d => `${d.hora}:00`),
      datasets: [{
        label: 'Média de Pessoas por Horário',
        data: data.map(d => Number(d.media_pessoas)),
        backgroundColor: 'rgba(75,192,192,.2)',
        borderColor: 'rgba(75,192,192,1)',
        borderWidth: 3, fill: true, tension: .4
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: true,
      scales: {
        y: { beginAtZero: true, title: { display: true, text: 'Número de Pessoas' } },
        x: { title: { display: true, text: 'Horário' } }
      },
      plugins: { legend: { display: true, position: 'top' } }
    }
  });
}

// Helpers para "Top 10 Trechos Mais Lotados"
async function fetchTrechosDependencies() {
  const [trechosAgg, onibus, recentes] = await Promise.all([
    fetchData('/analytics/lotacao-por-trecho'),
    fetchData('/onibus'),
    fetchData('/lotacao')
  ]);
  return { trechosAgg: Array.isArray(trechosAgg) ? trechosAgg : [], onibus: Array.isArray(onibus) ? onibus : [], recentes: Array.isArray(recentes) ? recentes : [] };
}

function getCapacidadeReferencia(onibus) {
  if (!onibus || !onibus.length) return 60;
  const caps = onibus.map(o => Number(o.capacidade || 0)).filter(v => Number.isFinite(v) && v > 0);
  return caps.length ? Math.max(...caps) : 60;
}

function buildLastTsMap(recentes) {
  const lastTsMap = new Map();
  for (const r of recentes) {
    const key = `${r.linha_nome || ''}>>>${r.parada_origem_nome || ''}>>>${r.parada_destino_nome || ''}`;
    const ts = new Date(r.data_hora).getTime() || 0;
    const cur = lastTsMap.get(key);
    if (!cur || ts > cur) lastTsMap.set(key, ts);
  }
  return lastTsMap;
}

function buildTrechosArrays(top10, capMax) {
  const labels = top10.map(d => `${d.parada_origem} → ${d.parada_destino || ''}`);
  const medias = top10.map(d => Number(d.media_pessoas) || 0);
  const ocupacoes = medias.map(m => Math.min((capMax > 0 ? (m / capMax) * 100 : 0), 200));
  return { labels, medias, ocupacoes };
}

function renderTrechosChart(labels, ocupacoes, medias, top10, capMax, lastTsMap) {
  const ctxElem = document.getElementById('chartTrechosLotados');
  if (!ctxElem) return;
  const ctx = ctxElem.getContext('2d');
  if (chartTrechosLotados) chartTrechosLotados.destroy();

  chartTrechosLotados = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Ocupação média (%) por trecho',
        data: ocupacoes,
        backgroundColor: 'rgba(255,159,64,.6)',
        borderColor: 'rgba(255,159,64,1)',
        borderWidth: 2
      }]
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        x: {
          beginAtZero: true,
          max: 200,
          title: { display: true, text: '% Ocupação (média pessoas / capacidade do ônibus)' },
          ticks: { callback: (v) => `${v}%` }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: (ctx) => `Ocupação: ${ctx.parsed.x.toFixed(1)}%`,
            afterLabel: (ctx) => {
              const i = ctx.dataIndex;
              const media = medias[i];
              const max = top10[i].max_pessoas;
              const regs = top10[i].total_registros;
              const linha = top10[i].linha_nome || '—';
              const key = `${linha}>>>${top10[i].parada_origem || ''}>>>${top10[i].parada_destino || ''}`;
              const ts = lastTsMap.get(key);
              const when = ts ? new Date(ts).toLocaleString('pt-BR') : '—';
              return [
                `Linha: ${linha}`,
                `Horário recente: ${when}`,
                `Média de pessoas: ${Number.isFinite(media) ? media.toFixed(1) : '0.0'}`,
                `Capacidade ref.: ${capMax}`,
                `Máximo observado: ${max}`,
                `Registros: ${regs}`
              ];
            }
          }
        }
      }
    }
  });
}

// Substitui a função por uma versão enxuta que usa os helpers acima
async function updateChartTrechosLotados() {
  const { trechosAgg, onibus, recentes } = await fetchTrechosDependencies();
  if (!trechosAgg.length) return;

  const capMax = getCapacidadeReferencia(onibus);
  const lastTsMap = buildLastTsMap(recentes);

  const top10 = trechosAgg.slice(0, 10);
  const { labels, medias, ocupacoes } = buildTrechosArrays(top10, capMax);

  renderTrechosChart(labels, ocupacoes, medias, top10, capMax, lastTsMap);
}

let registrosDataCache = [];
let registrosSort = { key: 'data_hora', dir: 'desc' }; // padrão: mais recentes primeiro

function compareReg(a, b, key) {
  // Conversões por tipo de coluna
  if (key === 'data_hora') {
    const da = new Date(a.data_hora).getTime() || 0;
    const db = new Date(b.data_hora).getTime() || 0;
    return da - db;
  }
  if (key === 'qtd_pessoas') {
    return Number(a.qtd_pessoas || 0) - Number(b.qtd_pessoas || 0);
  }
  // strings: linha_nome, parada_origem_nome, parada_destino_nome
  const sa = String(a[key] ?? '').toLocaleLowerCase('pt-BR');
  const sb = String(b[key] ?? '').toLocaleLowerCase('pt-BR');
  return sa.localeCompare(sb, 'pt-BR');
}

function renderRegistrosTable(rows) {
  const tbody = document.getElementById('tabelaRegistros');
  if (!tbody) return;
  if (!rows || rows.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum registro encontrado</td></tr>';
    return;
  }
  tbody.innerHTML = rows.slice(0, 20).map(reg => {
    const dh = new Date(reg.data_hora);
    const destino = reg.parada_destino_nome || 'N/A';
    const statusClass = getStatusClass(reg.qtd_pessoas);
    return `
      <tr>
        <td>${dh.toLocaleString('pt-BR')}</td>
        <td><strong>${reg.linha_nome}</strong></td>
        <td>${reg.parada_origem_nome}</td>
        <td>${destino}</td>
        <td><span class="badge ${statusClass}">${reg.qtd_pessoas}</span></td>
        <td><span class="badge bg-info status-badge">${getLotacaoStatus(reg.qtd_pessoas)}</span></td>
      </tr>`;
  }).join('');
}

function applyRegistrosSortAndRender() {
  if (!Array.isArray(registrosDataCache)) return;
  const { key, dir } = registrosSort;
  const sorted = [...registrosDataCache].sort((a, b) => {
    const cmp = compareReg(a, b, key);
    return dir === 'asc' ? cmp : -cmp;
  });
  renderRegistrosTable(sorted);
}

function setupRegistrosSorting() {
  const ths = document.querySelectorAll('thead th.sortable');
  ths.forEach(th => {
    th.style.cursor = 'pointer';
    th.addEventListener('click', () => {
      const newKey = th.dataset.sortKey;
      if (!newKey) return;
      if (registrosSort.key === newKey) {
        registrosSort.dir = registrosSort.dir === 'asc' ? 'desc' : 'asc';
      } else {
        registrosSort.key = newKey;
        registrosSort.dir = (newKey === 'data_hora') ? 'desc' : 'asc';
      }
      applyRegistrosSortAndRender();
    });
  });
}

async function updateRegistrosTable() {
  const data = await fetchData('/lotacao');
  // Substitui rendering direto por cache + sort
  registrosDataCache = Array.isArray(data) ? data : [];
  applyRegistrosSortAndRender();
}

// Mantém getStatusClass e getLotacaoStatus (usados em outras partes)
function getStatusClass(qtd) { if (qtd >= 50) return 'bg-danger'; if (qtd >= 30) return 'bg-warning'; return 'bg-success'; }
function getLotacaoStatus(qtd) { if (qtd >= 50) return 'Lotado'; if (qtd >= 30) return 'Moderado'; return 'Normal'; }

async function updateDashboard() {
  updateTimestamp();
  await updateSummaryCards();
  await updateChartLotacaoPorLinha();
  await updateChartLotacaoHoraria();
  await updateChartTrechosLotados();
  await updateRegistrosTable();
  await populateLinhasSelect();
}

document.addEventListener('DOMContentLoaded', () => {
  updateDashboard();
  setInterval(updateDashboard, 30000);
  // Novo: habilita ordenação dos cabeçalhos da tabela
  setupRegistrosSorting();
});
