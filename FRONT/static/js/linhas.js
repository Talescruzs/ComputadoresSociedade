const API_BASE = (window.API_BASE || `${location.protocol}//${location.hostname}:5000/api`).replace(/\/+$/,'');

async function fetchJSON(ep) {
  try {
    const r = await fetch(`${API_BASE}${ep}`);
    if (!r.ok) throw new Error(r.status);
    return await r.json();
  } catch(e) {
    console.error("Falha fetch", ep, e);
    return null;
  }
}

// Cache e estado de ordenação
let linhasRaw = []; // novo: cache sem filtro
let linhasCache = [];
let linhasSort = { key: 'nome', dir: 'asc' };

function compareLinhas(a, b, key) {
  if (key === 'total_paradas') {
    return Number(a.total_paradas || 0) - Number(b.total_paradas || 0);
  }
  if (key === 'pct_excesso') {
    return Number(a.pct_excesso_val || 0) - Number(b.pct_excesso_val || 0);
  }
  const sa = String(a.nome || '').toLocaleLowerCase('pt-BR');
  const sb = String(b.nome || '').toLocaleLowerCase('pt-BR');
  return sa.localeCompare(sb, 'pt-BR');
}

function renderLinhasTable(data) {
  const tbody = document.getElementById('tabelaLinhas');
  if (!tbody) return;
  if (!data || data.length === 0) {
    tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhuma linha encontrada</td></tr>';
    return;
  }
  tbody.innerHTML = data.map(row => {
    const linhaEncoded = encodeURIComponent(row.nome);
    return `
      <tr>
        <td>${row.nome}</td>
        <td>${row.total_paradas}</td>
        <td>${row.pct_excesso}</td>
        <td class="rota-cadeia">${row.rota_cadeia}</td>
        <td><a href="/viagens-detalhes?linha=${linhaEncoded}" class="btn btn-sm btn-outline-primary">Ver viagens</a></td>
      </tr>
    `;
  }).join('');
}

function applyLinhasSortAndRender() {
  const { key, dir } = linhasSort;
  const sorted = [...linhasCache].sort((a, b) => {
    const cmp = compareLinhas(a, b, key);
    return dir === 'asc' ? cmp : -cmp;
  });
  // Atualiza indicadores visuais no thead
  const ths = document.querySelectorAll('thead th.sortable');
  ths.forEach(th => {
    th.classList.remove('sort-asc', 'sort-desc');
    if (th.dataset.sortKey === key) th.classList.add(dir === 'asc' ? 'sort-asc' : 'sort-desc');
  });
  renderLinhasTable(sorted);
}

function setupLinhasSorting() {
  const ths = document.querySelectorAll('thead th.sortable');
  ths.forEach(th => {
    th.addEventListener('click', () => {
      const newKey = th.dataset.sortKey;
      if (!newKey) return;
      if (linhasSort.key === newKey) {
        linhasSort.dir = (linhasSort.dir === 'asc') ? 'desc' : 'asc';
      } else {
        linhasSort.key = newKey;
        linhasSort.dir = newKey === 'nome' ? 'asc' : 'desc';
      }
      applyLinhasSortAndRender();
    });
  });
}

// Filtros
function popularSelectLinhas() {
  const sel = document.getElementById('filtroLinhaNome');
  if (!sel) return;
  const nomes = [...new Set(linhasRaw.map(l => l.nome).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
  sel.innerHTML = '<option value="">(Todas)</option>' + nomes.map(n=>`<option value="${n}">${n}</option>`).join('');
}

function getURLPrefill() {
  const p = new URLSearchParams(location.search);
  return { linha: p.get('linha') || '' };
}

function prefillFiltroLinha() {
  const { linha } = getURLPrefill();
  if (!linha) return;
  const sel = document.getElementById('filtroLinhaNome');
  if (sel) {
    sel.value = linha;
    if (sel.value !== linha) console.warn('Linha para prefill não encontrada:', linha);
  }
}

function aplicaFiltroLinhas() {
  const sel = document.getElementById('filtroLinhaNome');
  const filtro = sel?.value || '';
  linhasCache = linhasRaw.filter(r => !filtro || r.nome === filtro);
  applyLinhasSortAndRender();
}

function setupFiltroLinhasEvents() {
  document.getElementById('btnFiltrarLinhas')?.addEventListener('click', aplicaFiltroLinhas);
  document.getElementById('btnLimparLinhas')?.addEventListener('click', () => {
    const sel = document.getElementById('filtroLinhaNome');
    if (sel) sel.value = '';
    aplicaFiltroLinhas();
  });
  document.getElementById('filtroLinhaNome')?.addEventListener('change', aplicaFiltroLinhas);
}

async function loadLinhas() {
  const tbody = document.getElementById('tabelaLinhas');
  if (!tbody) return;
  tbody.innerHTML = '<tr><td colspan="5" class="text-center">Carregando...</td></tr>';

  const [linhas, viagens, onibus, lotacoes] = await Promise.all([
    fetchJSON('/linhas') || [],
    fetchJSON('/viagens') || [],
    fetchJSON('/onibus') || [],
    fetchJSON('/lotacao') || []
  ]);

  if (!linhas.length) {
    tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhuma linha encontrada</td></tr>';
    return;
  }

  // Mapas auxiliares
  const capacidadePorOnibus = new Map(onibus.map(o => [o.id_onibus, Number(o.capacidade || 0)]));
  const linhaPorViagem = new Map(viagens.map(v => [v.id_viagem, v.id_linha]));
  const onibusPorViagem = new Map(viagens.map(v => [v.id_viagem, v.id_onibus]));

  const statsLinha = new Map();
  for (const reg of lotacoes || []) {
    const idViagem = reg.id_viagem;
    const idLinha = linhaPorViagem.get(idViagem);
    const idOnibus = onibusPorViagem.get(idViagem);
    if (idLinha == null) continue;
    const capacidade = capacidadePorOnibus.get(idOnibus) || 0;
    const qtd = Number(reg.qtd_pessoas || 0);
    if (!statsLinha.has(idLinha)) statsLinha.set(idLinha, { total: 0, excesso: 0 });
    const stat = statsLinha.get(idLinha);
    stat.total += 1;
    if (capacidade > 0 && qtd > capacidade) stat.excesso += 1;
  }

  const rows = [];
  for (const l of linhas) {
    const rota = await fetchJSON(`/linhas/${l.id_linha}/rota`) || [];
    const totalParadas = rota.length;
    const rotaCadeia = (rota.length ? rota.map(r => r.parada_nome).join(' →<wbr> ') : '—');

    const stat = statsLinha.get(l.id_linha) || { total: 0, excesso: 0 };
    const pctVal = stat.total > 0 ? (stat.excesso / stat.total) * 100 : 0;
    rows.push({
      nome: l.nome,
      total_paradas: totalParadas,
      rota_cadeia: rotaCadeia,
      pct_excesso_val: pctVal,
      pct_excesso: `${pctVal.toFixed(2)}%`
    });
  }

  // popula filtros e aplica
  linhasRaw = rows;
  popularSelectLinhas();
  prefillFiltroLinha();
  aplicaFiltroLinhas();
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
  loadLinhas();
  setupLinhasSorting();
  setupFiltroLinhasEvents();
});
