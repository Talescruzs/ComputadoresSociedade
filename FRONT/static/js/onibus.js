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

let onibusCache = [];
let onibusRaw = []; // novo: dados completos sem filtro
let onibusSort = { key: 'placa', dir: 'asc' };
let prefillPlaca = ''; // novo

function getURLPrefill() {
  const p = new URLSearchParams(location.search);
  prefillPlaca = p.get('placa') || '';
}

function popularFiltroPlacas() {
  const sel = document.getElementById('filtroOnibusPlaca');
  if (!sel) return;
  const placas = [...new Set(onibusRaw.map(o => o.placa))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
  sel.innerHTML = '<option value="">(Todas)</option>' + placas.map(p=>`<option value="${p}">${p}</option>`).join('');
  if (prefillPlaca) {
    sel.value = prefillPlaca;
    if (sel.value !== prefillPlaca) console.warn('Placa para prefill não encontrada:', prefillPlaca);
  }
}

function aplicaFiltroOnibus(){
  const sel = document.getElementById('filtroOnibusPlaca');
  const placa = sel?.value || '';
  onibusCache = onibusRaw.filter(o => !placa || o.placa === placa);
  applyOnibusSortAndRender();
}

function setupFiltroEvents(){
  document.getElementById('btnFiltrarOnibus')?.addEventListener('click', aplicaFiltroOnibus);
  document.getElementById('btnLimparOnibus')?.addEventListener('click', ()=>{
    const sel = document.getElementById('filtroOnibusPlaca');
    if (sel) sel.value = '';
    aplicaFiltroOnibus();
  });
  document.getElementById('filtroOnibusPlaca')?.addEventListener('change', aplicaFiltroOnibus);
}

function compareOnibus(a, b, key) {
  if (key === 'capacidade') return Number(a.capacidade || 0) - Number(b.capacidade || 0);
  if (key === 'viagens_total') return Number(a.viagens_total || 0) - Number(b.viagens_total || 0);
  if (key === 'pct_excesso') return Number(a.pct_excesso_val || 0) - Number(b.pct_excesso_val || 0);
  const sa = String(a.placa || '').toLocaleLowerCase('pt-BR');
  const sb = String(b.placa || '').toLocaleLowerCase('pt-BR');
  return sa.localeCompare(sb, 'pt-BR');
}

function renderOnibusTable(data) {
  const tbody = document.getElementById('tabelaOnibus');
  if (!tbody) return;
  if (!data || !data.length) {
    tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum ônibus encontrado</td></tr>';
    return;
  }
  tbody.innerHTML = data.map(o => {
    const placaEncoded = encodeURIComponent(o.placa);
    return `
      <tr>
        <td>${o.placa}</td>
        <td>${o.capacidade}</td>
        <td>${o.viagens_total}</td>
        <td>${o.pct_excesso}</td>
        <td>${o.data_ultima_manutencao_fmt}</td>
        <td><a href="/viagens-detalhes?placa=${placaEncoded}" class="btn btn-sm btn-outline-primary">Ver viagens</a></td>
      </tr>
    `;
  }).join('');
}

function applyOnibusSortAndRender() {
  const { key, dir } = onibusSort;
  const sorted = [...onibusCache].sort((a, b) => {
    const cmp = compareOnibus(a, b, key);
    return dir === 'asc' ? cmp : -cmp;
  });
  const ths = document.querySelectorAll('thead th.sortable');
  ths.forEach(th => {
    th.classList.remove('sort-asc','sort-desc');
    if (th.dataset.sortKey === key) th.classList.add(dir === 'asc' ? 'sort-asc' : 'sort-desc');
  });
  renderOnibusTable(sorted);
}

function setupOnibusSorting() {
  const ths = document.querySelectorAll('thead th.sortable');
  ths.forEach(th => {
    th.addEventListener('click', () => {
      const newKey = th.dataset.sortKey;
      if (!newKey) return;
      if (onibusSort.key === newKey) {
        onibusSort.dir = onibusSort.dir === 'asc' ? 'desc' : 'asc';
      } else {
        onibusSort.key = newKey;
        onibusSort.dir = newKey === 'placa' ? 'asc' : 'desc';
      }
      applyOnibusSortAndRender();
    });
  });
}

async function loadOnibus() {
  const tbody = document.getElementById('tabelaOnibus');
  if (!tbody) return;
  tbody.innerHTML = '<tr><td colspan="6" class="text-center">Carregando...</td></tr>';

  const [onibus, viagens, lotacoes] = await Promise.all([
    fetchJSON('/onibus') || [],
    fetchJSON('/viagens') || [],
    fetchJSON('/lotacao') || []
  ]);

  if (!onibus.length) {
    onibusRaw = [];
    onibusCache = [];
    tbody.innerHTML = '<tr><td colspan="6" class="text-center">Nenhum ônibus encontrado</td></tr>';
    return;
  }

  const viagensPorOnibus = new Map();
  const capacidadePorOnibus = new Map(onibus.map(o => [o.id_onibus, Number(o.capacidade || 0)]));

  for (const v of viagens) {
    const id = v.id_onibus;
    if (!viagensPorOnibus.has(id)) viagensPorOnibus.set(id, []);
    viagensPorOnibus.get(id).push(v.id_viagem);
  }

  const excessos = new Map();
  const totais = new Map();

  for (const reg of lotacoes) {
    const vid = reg.id_viagem;
    // descobrir ônibus: linear (poucos registros) ou criar mapa antes
    // otimiza criando mapa viagem->onibus
  }

  const viagemToOnibus = new Map(viagens.map(v => [v.id_viagem, v.id_onibus]));

  for (const reg of lotacoes) {
    const oid = viagemToOnibus.get(reg.id_viagem);
    if (oid == null) continue;
    const cap = capacidadePorOnibus.get(oid) || 0;
    const qtd = Number(reg.qtd_pessoas || 0);
    totais.set(oid, (totais.get(oid) || 0) + 1);
    if (cap > 0 && qtd > cap) {
      excessos.set(oid, (excessos.get(oid) || 0) + 1);
    }
  }

  onibusRaw = onibus.map(o => {
    const totalReg = totais.get(o.id_onibus) || 0;
    const excReg = excessos.get(o.id_onibus) || 0;
    const pct = totalReg > 0 ? (excReg / totalReg) * 100 : 0;
    return {
      placa: o.placa,
      capacidade: o.capacidade,
      viagens_total: (viagensPorOnibus.get(o.id_onibus) || []).length,
      pct_excesso_val: pct,
      pct_excesso: `${pct.toFixed(2)}%`,
      data_ultima_manutencao: o.data_ultima_manutencao,
      data_ultima_manutencao_fmt: formatDate(o.data_ultima_manutencao)
    };
  });

  popularFiltroPlacas();
  aplicaFiltroOnibus();
}

function formatDate(str) {
  if (!str) return '—';
  const d = new Date(str);
  if (isNaN(d.getTime())) return '—';
  const dia = String(d.getDate()).padStart(2,'0');
  const mes = String(d.getMonth()+1).padStart(2,'0');
  const ano = d.getFullYear();
  return `${dia}/${mes}/${ano}`;
}

document.addEventListener('DOMContentLoaded', () => {
  getURLPrefill();
  loadOnibus();
  setupOnibusSorting();
  setupFiltroEvents();
});
