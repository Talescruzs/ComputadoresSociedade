const API_BASE = (window.API_BASE || `${location.protocol}//${location.hostname}:5000/api`).replace(/\/+$/,'');

async function api(ep){
  console.log('[viagens] fetch', ep);
  try {
    const r = await fetch(`${API_BASE}${ep}`);
    if(!r.ok) throw new Error(`HTTP ${r.status}`);
    return await r.json();
  } catch(e){
    console.error("Erro fetch", ep, e);
    setMsg(`Falha ao carregar ${ep}: ${e.message}`);
    return null;
  }
}

function setMsg(txt){
  const el = document.getElementById('viagensMsg');
  if(el) el.textContent = txt || '';
}

let viagensCache = [];
let viagensRaw = []; // novo: dados sem filtro
let viagensSort = { key: 'linha_nome', dir: 'asc' };

function formatDateTime(str){
  if(!str) return '—';
  const d = new Date(str);
  if(isNaN(d.getTime())) return '—';
  return d.toLocaleString('pt-BR', { hour12:false });
}
function formatDate(str){
  if(!str) return '—';
  const d = new Date(str);
  if(isNaN(d.getTime())) return '—';
  return d.toLocaleDateString('pt-BR');
}

function compareViagens(a,b,key){
  if(key === 'total_registros') return a.total_registros - b.total_registros;
  if(key === 'pct_excesso') return a.pct_excesso_val - b.pct_excesso_val;
  if(key === 'duracao_min') return a.duracao_min - b.duracao_min;
  if(key === 'data_inicio') return a._ts_inicio - b._ts_inicio;
  if(key === 'onibus_placa') return a.onibus_placa.localeCompare(b.onibus_placa,'pt-BR');
  if(key === 'status') return a.status.localeCompare(b.status,'pt-BR');
  return a.linha_nome.localeCompare(b.linha_nome,'pt-BR');
}

function renderViagens(data){
  const tbody = document.getElementById('tabelaViagens');
  if(!tbody) return;
  if(!data.length){
    tbody.innerHTML = '<tr><td colspan="7" class="text-center">Nenhuma viagem encontrada</td></tr>';
    return;
  }
  tbody.innerHTML = data.map(v => `
    <tr>
      <td>${v.linha_nome}</td>
      <td>${v.onibus_placa}</td>
      <td title="${v.data_inicio}">${v.data_inicio_fmt}</td>
      <td>${v.total_registros}</td>
      <td>${v.pct_excesso}</td>
      <td>${v.duracao_min}</td>
    </tr>
  `).join('');
}

function applyViagensSort(){
  const { key, dir } = viagensSort;
  const sorted = [...viagensCache].sort((a,b)=>{
    const cmp = compareViagens(a,b,key);
    return dir === 'asc' ? cmp : -cmp;
  });
  document.querySelectorAll('thead th.sortable').forEach(th=>{
    th.classList.remove('sort-asc','sort-desc');
    if(th.dataset.sortKey === key){
      th.classList.add(dir === 'asc' ? 'sort-asc' : 'sort-desc');
    }
  });
  renderViagens(sorted);
}

function setupViagensSorting(){
  document.querySelectorAll('thead th.sortable').forEach(th=>{
    th.addEventListener('click', ()=>{
      const k = th.dataset.sortKey;
      if(!k) return;
      if(viagensSort.key === k){
        viagensSort.dir = viagensSort.dir === 'asc' ? 'desc' : 'asc';
      } else {
        viagensSort.key = k;
        viagensSort.dir = k === 'linha_nome' ? 'asc' : 'desc';
      }
      applyViagensSort();
    });
  });
}

function getFiltroValues() {
  const placa = document.getElementById('filtroPlaca')?.value || '';
  const linha = document.getElementById('filtroLinha')?.value || '';
  const de = document.getElementById('filtroInicioDe')?.value || '';
  const ate = document.getElementById('filtroInicioAte')?.value || '';
  const incluirSem = document.getElementById('filtroIncluirSemViagem')?.checked;
  const somenteSem = document.getElementById('filtroSomenteSemViagem')?.checked;
  return { placa, linha, de, ate, incluirSem, somenteSem };
}

function aplicaFiltros() {
  const { placa, linha, de, ate, incluirSem, somenteSem } = getFiltroValues();
  const tsDe = de ? new Date(de).getTime() : null;
  const tsAte = ate ? new Date(ate).getTime() : null;
  viagensCache = viagensRaw.filter(v => {
    if (!incluirSem && v.no_trip) return false;
    if (somenteSem && !v.no_trip) return false;
    if (placa && v.onibus_placa !== placa) return false;
    if (linha && v.linha_nome !== linha) return false;
    if (tsDe && v._ts_inicio < tsDe) return false;
    if (tsAte && v._ts_inicio > tsAte) return false;
    return true;
  });
  setMsg(`Exibindo ${viagensCache.length} de ${viagensRaw.length} registros (incluindo ônibus sem viagens).`);
  applyViagensSort();
}

function popularSelects() {
  const selPlaca = document.getElementById('filtroPlaca');
  const selLinha = document.getElementById('filtroLinha');
  if (!selPlaca || !selLinha) return;
  const placas = [...new Set(viagensRaw.map(v => v.onibus_placa).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
  const linhas = [...new Set(viagensRaw.map(v => v.linha_nome).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
  selPlaca.innerHTML = '<option value="">(Todas)</option>' + placas.map(p => `<option value="${p}">${p}</option>`).join('');
  selLinha.innerHTML = '<option value="">(Todas)</option>' + linhas.map(l => `<option value="${l}">${l}</option>`).join('');
}

function setupFiltrosListeners() {
  document.getElementById('btnAplicarFiltros')?.addEventListener('click', aplicaFiltros);
  document.getElementById('btnLimparFiltros')?.addEventListener('click', () => {
    ['filtroPlaca','filtroLinha','filtroInicioDe','filtroInicioAte'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });
    const inc = document.getElementById('filtroIncluirSemViagem');
    const som = document.getElementById('filtroSomenteSemViagem');
    if (inc) inc.checked = true;
    if (som) som.checked = false;
    aplicaFiltros();
  });
  ['filtroPlaca','filtroLinha','filtroInicioDe','filtroInicioAte','filtroIncluirSemViagem','filtroSomenteSemViagem']
    .forEach(id => document.getElementById(id)?.addEventListener('change', aplicaFiltros));
}

function getURLPrefill() {
  const params = new URLSearchParams(window.location.search);
  return {
    placa: params.get('placa') || ''
  };
}

function prefillFiltersFromURL() {
  const pre = getURLPrefill();
  if (pre.placa) {
    const selPlaca = document.getElementById('filtroPlaca');
    if (selPlaca) {
      selPlaca.value = pre.placa;
      // Caso a placa não exista nas opções (ex.: removida), ignora sem erro
      if (selPlaca.value !== pre.placa) {
        console.warn('Placa para prefill não encontrada nas opções:', pre.placa);
      }
    }
  }
}

async function loadViagens(){
  const tbody = document.getElementById('tabelaViagens');
  if(tbody) tbody.innerHTML = '<tr><td colspan="7" class="text-center">Carregando...</td></tr>';
  setMsg('Carregando viagens...');
  const [viagens, linhas, onibus, lotacoes] = await Promise.all([
    api('/viagens') || [],
    api('/linhas') || [],
    api('/onibus') || [],
    api('/lotacao') || []
  ]);
  if(!Array.isArray(viagens) || !viagens.length){
    if(tbody) tbody.innerHTML = '<tr><td colspan="7" class="text-center">Nenhuma viagem encontrada</td></tr>';
    setMsg('Nenhuma viagem encontrada.');
    return;
  }

  const mapLinha = new Map(linhas.map(l=>[l.id_linha, l.nome]));
  const mapOnibus = new Map(onibus.map(o=>[o.id_onibus, { placa:o.placa, cap:Number(o.capacidade||0) }]));
  const lotacoesPorViagem = new Map();
  for(const reg of (lotacoes||[])){
    const arr = lotacoesPorViagem.get(reg.id_viagem) || [];
    arr.push(reg);
    lotacoesPorViagem.set(reg.id_viagem, arr);
  }

  const onibusIdsComViagem = new Set(viagens.map(v => v.id_onibus));
  const onibusSemViagem = onibus.filter(o => !onibusIdsComViagem.has(o.id_onibus));

  const viagensProcessadas = viagens.map(v=>{
    const linhaNome = mapLinha.get(v.id_linha) || `Linha ${v.id_linha}`;
    const bus = mapOnibus.get(v.id_onibus) || { placa:'—', cap:0 };
    const regs = lotacoesPorViagem.get(v.id_viagem) || [];
    const totalReg = regs.length;
    let exc = 0;
    let maxTs = v.data_hora_inicio ? new Date(v.data_hora_inicio).getTime() : 0;
    regs.forEach(r=>{
      const qtd = Number(r.qtd_pessoas||0);
      if(bus.cap>0 && qtd>bus.cap) exc++;
      const ts = new Date(r.data_hora).getTime();
      if(!isNaN(ts) && ts>maxTs) maxTs = ts;
    });
    const pct = totalReg>0 ? (exc/totalReg)*100 : 0;
    const startTs = new Date(v.data_hora_inicio).getTime();
    const duracaoMin = (maxTs && !isNaN(startTs) && maxTs>=startTs) ? Math.round((maxTs-startTs)/60000) : 0;
    return {
      id_viagem: v.id_viagem,
      linha_nome: linhaNome,
      onibus_placa: bus.placa,
      data_inicio: v.data_hora_inicio,
      data_inicio_fmt: formatDateTime(v.data_hora_inicio),
      _ts_inicio: isNaN(startTs)?0:startTs,
      total_registros: totalReg,
      pct_excesso_val: pct,
      pct_excesso: `${pct.toFixed(2)}%`,
      duracao_min: duracaoMin,
      no_trip: false
    };
  });

  const synthetics = onibusSemViagem.map(o => ({
    id_viagem: null,
    linha_nome: '—',
    onibus_placa: o.placa,
    data_inicio: null,
    data_inicio_fmt: '—',
    _ts_inicio: 0,
    total_registros: 0,
    pct_excesso_val: 0,
    pct_excesso: '0.00%',
    duracao_min: 0,
    no_trip: true
  }));

  viagensRaw = [...viagensProcessadas, ...synthetics];
  popularSelects();
  prefillFiltersFromURL();
  aplicaFiltros();
  setMsg(`Total carregado: ${viagensRaw.length} (viagens: ${viagensProcessadas.length}, ônibus sem viagens: ${synthetics.length}).`);
  applyViagensSort();
}

document.addEventListener('DOMContentLoaded', ()=>{
  loadViagens();
  setupViagensSorting();
  setupFiltrosListeners();
  const btn = document.getElementById('btnRefreshViagens');
  if(btn) btn.addEventListener('click', ()=> loadViagens());
});
