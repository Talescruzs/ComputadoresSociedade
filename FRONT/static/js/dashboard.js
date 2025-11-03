// Configuração da API (usa variável injetada ou fallback)
const API_URL = (window.API_BASE || 'http://localhost:5000/api').replace(/\/+$/,'');

// Variáveis globais para os gráficos
let chartLotacaoPorLinha = null;
let chartLotacaoHoraria = null;
let chartTrechosLotados = null;

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

async function updateSummaryCards() {
  const [linhas, onibus, viagens, paradas] = await Promise.all([
    fetchData('/linhas'), fetchData('/onibus'), fetchData('/viagens'), fetchData('/paradas')
  ]);
  if (linhas) document.getElementById('totalLinhas').textContent = linhas.length;
  if (onibus) document.getElementById('totalOnibus').textContent = onibus.length;
  if (paradas) document.getElementById('totalParadas').textContent = paradas.length;
  if (viagens) {
    const ativas = viagens.filter(v => v.status === 'em_andamento').length;
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

async function updateChartTrechosLotados() {
  const data = await fetchData('/analytics/lotacao-por-trecho');
  if (!data || data.length === 0) return;
  const top10 = data.slice(0, 10);
  const ctx = document.getElementById('chartTrechosLotados').getContext('2d');
  if (chartTrechosLotados) chartTrechosLotados.destroy();
  chartTrechosLotados = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: top10.map(d => `${d.parada_origem} → ${d.parada_destino}`),
      datasets: [{
        label: 'Média de Pessoas',
        data: top10.map(d => Number(d.media_pessoas)),
        backgroundColor: 'rgba(255,159,64,.6)',
        borderColor: 'rgba(255,159,64,1)',
        borderWidth: 2
      }]
    },
    options: {
      indexAxis: 'y', responsive: true, maintainAspectRatio: true,
      scales: { x: { beginAtZero: true, title: { display: true, text: 'Número de Pessoas' } } },
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            afterLabel: (ctx) => {
              const i = ctx.dataIndex;
              return `Máximo: ${top10[i].max_pessoas}\nRegistros: ${top10[i].total_registros}`;
            }
          }
        }
      }
    }
  });
}

async function updateRegistrosTable() {
  const data = await fetchData('/lotacao');
  const tbody = document.getElementById('tabelaRegistros');
  if (!data || data.length === 0) {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum registro encontrado</td></tr>';
    return;
  }
  const recent = data.slice(0, 20);
  tbody.innerHTML = recent.map(reg => {
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

async function updateMapaLotacao() {
  const dataLinhas = await fetchData('/analytics/lotacao-por-linha');
  const dataTrechos = await fetchData('/analytics/lotacao-por-trecho');
  if (!dataLinhas || !dataTrechos) return;
  const mapaDiv = document.getElementById('mapaLotacao');
  mapaDiv.innerHTML = dataLinhas.map(linha => {
    const trechos = dataTrechos.filter(t => t.linha_nome === linha.linha_nome);
    const mediaGeral = Number(linha.media_pessoas);
    return `
      <div class="linha-item mb-4" style="background: linear-gradient(90deg, ${getColorByOccupancy(mediaGeral)} 0%, transparent 100%);">
        <h5 class="mb-3">${linha.linha_nome}</h5>
        <small>Média: ${mediaGeral.toFixed(1)} pessoas | Máximo: ${linha.max_pessoas} pessoas</small>
        <div class="mt-3">
          ${trechos.slice(0,5).map(t => {
            const media = Number(t.media_pessoas);
            const percentage = Math.min((media / 60) * 100, 100);
            return `
              <div class="trecho">
                <div class="parada">${t.parada_origem}</div>
                <div class="barra-lotacao">
                  <div class="barra-preenchida" style="width:${percentage}%">${media.toFixed(1)} pessoas</div>
                </div>
                <div class="parada">${t.parada_destino || 'Fim'}</div>
                <span class="badge ${getStatusClass(media)} badge-lotacao">${getLotacaoStatus(media)}</span>
              </div>`;
          }).join('')}
        </div>
      </div>`;
  }).join('');
}

function getStatusClass(qtd) { if (qtd >= 50) return 'bg-danger'; if (qtd >= 30) return 'bg-warning'; return 'bg-success'; }
function getLotacaoStatus(qtd) { if (qtd >= 50) return 'Lotado'; if (qtd >= 30) return 'Moderado'; return 'Normal'; }
function getColorByOccupancy(qtd) { if (qtd >= 50) return '#dc3545'; if (qtd >= 30) return '#ffc107'; return '#28a745'; }

async function updateDashboard() {
  updateTimestamp();
  await updateSummaryCards();
  await updateChartLotacaoPorLinha();
  await updateChartLotacaoHoraria();
  await updateChartTrechosLotados();
  await updateRegistrosTable();
  await updateMapaLotacao();
}

document.addEventListener('DOMContentLoaded', () => {
  updateDashboard();
  setInterval(updateDashboard, 30000);
});
