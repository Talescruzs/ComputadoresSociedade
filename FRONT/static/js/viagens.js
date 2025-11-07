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
let viagensRaw = [];
let viagensSort = { key: 'linha_nome', dir: 'asc' };
let busPlacasAll = [];      // placas de todos ônibus (mesmo sem viagens)
let linhasAllNomes = [];    // novo: nomes de todas as linhas (mesmo sem viagens)

// Parser consistente para comparação (usa UTC para neutralizar fuso)
function parseComparableTs(str){
  if(!str) return null;
  // 1) MySQL "YYYY-MM-DD HH:MM:SS" ou ISO local "YYYY-MM-DDTHH:MM(:SS opcional)"
  let m = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})(?::(\d{2}))?$/.exec(str);
  if(m){
    const Y = Number(m[1]), Mo = Number(m[2]), D = Number(m[3]);
    const h = Number(m[4]), mi = Number(m[5]), s = Number(m[6] || 0);
    return Date.UTC(Y, Mo - 1, D, h, mi, s);
  }
  // 2) RFC/GMT/ISO com Z/GMT -> preserva os dígitos usando getters UTC
  const d = new Date(str);
  if (isNaN(d.getTime())) return null;
  const useUTC = /Z|GMT/i.test(str);
  const Y = useUTC ? d.getUTCFullYear() : d.getFullYear();
  const Mo = (useUTC ? d.getUTCMonth() : d.getMonth()) + 1;
  const D = useUTC ? d.getUTCDate() : d.getDate();
  const h = useUTC ? d.getUTCHours() : d.getHours();
  const mi = useUTC ? d.getUTCMinutes() : d.getMinutes();
  const s = useUTC ? d.getUTCSeconds() : d.getSeconds();
  return Date.UTC(Y, Mo - 1, D, h, mi, s);
}

// Ajuste: garantir fuso de Brasília (America/Sao_Paulo)
// Substituir a função formatDateTime anterior por esta:
function formatDateTime(str){
  if(!str) return '—';
  // Caso 1: "YYYY-MM-DD HH:MM:SS" ou "YYYY-MM-DDTHH:MM:SS"
  const m = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2}):(\d{2})$/.exec(str);
  if(m){
    const [,Y,M,D,h,min] = m;
    return `${D}/${M}/${Y} - ${h}:${min}`;
  }
  // Caso 2: RFC/GMT/ISO -> parseia e formata dd/mm/aaaa - HH:MM
  const d = new Date(str);
  if (isNaN(d.getTime())) return str; // fallback
  const pad = (n)=>String(n).padStart(2,'0');
  const useUTC = /Z|GMT/i.test(str);
  const DD = pad(useUTC ? d.getUTCDate() : d.getDate());
  const MM = pad((useUTC ? d.getUTCMonth() : d.getMonth()) + 1);
  const YYYY = useUTC ? d.getUTCFullYear() : d.getFullYear();
  const HH = pad(useUTC ? d.getUTCHours() : d.getHours());
  const mm = pad(useUTC ? d.getUTCMinutes() : d.getMinutes());
  return `${DD}/${MM}/${YYYY} - ${HH}:${mm}`;
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
  tbody.innerHTML = data.map(v => {
    const placaLink = v.onibus_placa
      ? `<a href="/onibus-detalhes?placa=${encodeURIComponent(v.onibus_placa)}" class="text-decoration-none">${v.onibus_placa}</a>`
      : '—';
    const linhaLink = v.linha_nome
      ? `<a href="/linhas-detalhes?linha=${encodeURIComponent(v.linha_nome)}" class="text-decoration-none">${v.linha_nome}</a>`
      : '—';
    const btn = `<a href="/viagens-detalhes/${v.id_viagem}" class="btn btn-sm btn-outline-primary">Detalhes</a>`;
    return `
    <tr>
      <td>${linhaLink}</td>
      <td>${placaLink}</td>
      <td title="${formatDateTime(v.data_inicio)}">${v.data_inicio_fmt}</td>
      <td>${v.total_registros}</td>
      <td>${v.pct_excesso}</td>
      <td>${v.duracao_min}</td>
      <td>${btn}</td>
    </tr>`;
  }).join('');
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

// Helper para converter 'YYYY-MM-DD' em intervalo UTC (início/fim do dia)
function dayRangeTs(dateStr){
  if(!dateStr) return null;
  const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(dateStr);
  if(!m) return null;
  const Y = Number(m[1]), M = Number(m[2]), D = Number(m[3]);
  const start = Date.UTC(Y, M-1, D, 0, 0, 0);
  const end   = Date.UTC(Y, M-1, D, 23, 59, 59);
  return { start, end };
}

// Substituir captura dos valores de filtro (placa, linha, de, ate)
function getFiltroValues() {
  const placa = document.getElementById('filtroPlaca')?.value || '';
  const linha = document.getElementById('filtroLinha')?.value || '';
  const diaDe = document.getElementById('filtroDiaDe')?.value || '';
  const diaAte = document.getElementById('filtroDiaAte')?.value || '';
  const horaDe = document.getElementById('filtroHoraDe')?.value || '';
  const horaAte = document.getElementById('filtroHoraAte')?.value || '';
  return { placa, linha, diaDe, diaAte, horaDe, horaAte };
}

// Ajustar aplicaFiltros para usar intervalos de dia
function aplicaFiltros() {
  const { placa, linha, diaDe, diaAte, horaDe, horaAte } = getFiltroValues();
  const rangeDe = dayRangeTs(diaDe);
  const rangeAte = dayRangeTs(diaAte);
  const startLimit = rangeDe?.start ?? null;
  const endLimit = rangeAte?.end ?? null;
  const horaStart = horaDe && /^(\d{2}):(\d{2})$/.exec(horaDe) ? (parseInt(RegExp.$1)*60 + parseInt(RegExp.$2)) : null;
  const horaEnd   = horaAte && /^(\d{2}):(\d{2})$/.exec(horaAte) ? (parseInt(RegExp.$1)*60 + parseInt(RegExp.$2)) : null;
  const wrap = (horaStart!=null && horaEnd!=null && horaEnd < horaStart);

  viagensCache = viagensRaw.filter(v => {
    if (placa && v.onibus_placa !== placa) return false;
    if (linha && v.linha_nome !== linha) return false;
    if (startLimit != null && v._ts_inicio < startLimit) return false;
    if (endLimit != null && v._ts_inicio > endLimit) return false;
    if (horaStart != null || horaEnd != null) {
      const hm = v.hour_of_day_min;
      if (horaStart != null && horaEnd == null && hm < horaStart) return false;
      if (horaEnd != null && horaStart == null && hm > horaEnd) return false;
      if (horaStart != null && horaEnd != null) {
        if (!wrap && (hm < horaStart || hm > horaEnd)) return false;
        if (wrap && !(hm >= horaStart || hm <= horaEnd)) return false;
      }
    }
    return true;
  });
  setMsg(`Exibindo ${viagensCache.length} de ${viagensRaw.length} viagens.`);
  applyViagensSort();
}

function setupFiltrosListeners() {
  document.getElementById('btnAplicarFiltros')?.addEventListener('click', aplicaFiltros);
  document.getElementById('btnLimparFiltros')?.addEventListener('click', () => {
    ['filtroPlaca','filtroLinha','filtroDiaDe','filtroDiaAte','filtroHoraDe','filtroHoraAte'].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });
    aplicaFiltros();
  });
  ['filtroPlaca','filtroLinha','filtroDiaDe','filtroDiaAte','filtroHoraDe','filtroHoraAte']
    .forEach(id => document.getElementById(id)?.addEventListener('change', aplicaFiltros));
}

function getURLPrefill() {
  const params = new URLSearchParams(window.location.search);
  return {
    placa: params.get('placa') || '',
    linha: params.get('linha') || '',
    // novo: horários via URL
    horaDe: params.get('horaDe') || '',
    horaAte: params.get('horaAte') || ''
  };
}

function prefillFiltersFromURL() {
  const pre = getURLPrefill();
  if (pre.placa) {
    const selPlaca = document.getElementById('filtroPlaca');
    if (selPlaca) {
      selPlaca.value = pre.placa;
      if (selPlaca.value !== pre.placa) console.warn('Placa prefill não encontrada:', pre.placa);
    }
  }
  if (pre.linha) {
    const selLinha = document.getElementById('filtroLinha');
    if (selLinha) {
      selLinha.value = pre.linha;
      if (selLinha.value !== pre.linha) console.warn('Linha prefill não encontrada:', pre.linha);
    }
  }
  // novo: preencher horários se vierem na URL (formato HH:MM)
  const hDe = document.getElementById('filtroHoraDe');
  const hAte = document.getElementById('filtroHoraAte');
  if (hDe && pre.horaDe) hDe.value = pre.horaDe;
  if (hAte && pre.horaAte) hAte.value = pre.horaAte;
}

// Hora/minuto no fuso de São Paulo (para filtrar por horário corretamente)
// Ajuste: para strings RFC/GMT, usar os dígitos originais (ignorar deslocamento de fuso)
function getHourMinuteInTZ(str, tz = 'America/Sao_Paulo') {
  if (!str) return 0;

  // Formato MySQL / ISO local (naive)
  let m = /^(\d{4})-(\d{2})-(\d{2})[ T](\d{2}):(\d{2})/.exec(str);
  if (m) {
    return (parseInt(m[4],10) * 60) + parseInt(m[5],10);
  }

  // Formato RFC c/ GMT: "Thu, 06 Nov 2025 07:00:00 GMT"
  m = /^\w{3},\s\d{2}\s\w{3}\s\d{4}\s(\d{2}):(\d{2}):\d{2}\sGMT$/i.exec(str);
  if (m) {
    return (parseInt(m[1],10) * 60) + parseInt(m[2],10);
  }

  // Formato ISO/Z (ex.: 2025-11-06T07:00:00Z) – preservar horário “visual” no fuso alvo
  const d = new Date(str);
  if (isNaN(d.getTime())) return 0;

  const parts = new Intl.DateTimeFormat('pt-BR', {
    timeZone: tz,
    hour: '2-digit',
    minute: '2-digit',
    hour12: false
  }).formatToParts(d);

  let h = 0, mi = 0;
  for (const p of parts) {
    if (p.type === 'hour') h = parseInt(p.value, 10);
    if (p.type === 'minute') mi = parseInt(p.value, 10);
  }
  return (h * 60) + mi;
}

async function loadViagens(){
  const tbody = document.getElementById('tabelaViagens');
  if(tbody) tbody.innerHTML = '<tr><td colspan="6" class="text-center">Carregando...</td></tr>';
  setMsg('Carregando viagens...');
  const [viagens, linhas, onibus, lotacoes] = await Promise.all([
    api('/viagens') || [],
    api('/linhas') || [],
    api('/onibus') || [],
    api('/lotacao') || []
  ]);

  // guarda todas as placas e nomes de linhas (inclusive sem viagens)
  busPlacasAll = Array.isArray(onibus) ? onibus.map(o=>o.placa) : [];
  linhasAllNomes = Array.isArray(linhas) ? linhas.map(l=>l.nome) : [];

  if(!Array.isArray(viagens) || !viagens.length){
    popularSelects();
    prefillFiltersFromURL();
    aplicaFiltros(); // render vazio -> "Nenhuma viagem encontrada"
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

  viagensRaw = (viagens || []).map(v=>{
    const linhaNome = mapLinha.get(v.id_linha) || `Linha ${v.id_linha}`;
    const bus = mapOnibus.get(v.id_onibus) || { placa:'—', cap:0 };
    const regs = lotacoesPorViagem.get(v.id_viagem) || [];
    const totalReg = regs.length;

    let exc = 0;
    // Usa parser consistente para os registros e para o início
    const startTs = parseComparableTs(v.data_hora_inicio);
    let maxTs = startTs || 0;

    regs.forEach(r=>{
      const qtd = Number(r.qtd_pessoas||0);
      if(bus.cap>0 && qtd>bus.cap) exc++;
      const ts = parseComparableTs(r.data_hora);
      if(ts != null && ts > maxTs) maxTs = ts;
    });

    const pct = totalReg>0 ? (exc/totalReg)*100 : 0;
    const duracaoMin = (maxTs && startTs && maxTs>=startTs) ? Math.round((maxTs-startTs)/60000) : 0;

    const startStr = v.data_hora_inicio || '';
    const hm = getHourMinuteInTZ(startStr, 'America/Sao_Paulo'); // ajusta ao fuso

    return {
      id_viagem: v.id_viagem,
      linha_nome: linhaNome,
      onibus_placa: bus.placa,
      data_inicio: v.data_hora_inicio,
      data_inicio_fmt: formatDateTime(v.data_hora_inicio),
      _ts_inicio: (startTs==null?0:startTs),
      total_registros: totalReg,
      pct_excesso_val: pct,
      pct_excesso: `${pct.toFixed(2)}%`,
      duracao_min: duracaoMin,
      hour_of_day_min: hm
    };
  });

  popularSelects();
  prefillFiltersFromURL();
  aplicaFiltros();
  setMsg(`Total carregado: ${viagensRaw.length} viagens.`);
  applyViagensSort();
}

document.addEventListener('DOMContentLoaded', ()=>{
  loadViagens();
  setupViagensSorting();
  setupFiltrosListeners();
  const btn = document.getElementById('btnRefreshViagens');
  if(btn) btn.addEventListener('click', ()=> loadViagens());
});

function popularSelects() {
  const selPlaca = document.getElementById('filtroPlaca');
  const selLinha = document.getElementById('filtroLinha');
  if (!selPlaca || !selLinha) return;

  // Preserva seleção atual (se existir)
  const prevPlaca = selPlaca.value || '';
  const prevLinha = selLinha.value || '';

  // Usa exclusivamente os catálogos da API (inclui itens sem viagens)
  const placas = [...new Set((busPlacasAll || []).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
  const linhas = [...new Set((linhasAllNomes || []).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'pt-BR'));

  selPlaca.innerHTML = '<option value="">(Todas)</option>' + placas.map(p => `<option value="${p}">${p}</option>`).join('');
  selLinha.innerHTML = '<option value="">(Todas)</option>' + linhas.map(l => `<option value="${l}">${l}</option>`).join('');

  // Restaura seleção anterior se ainda existir nas opções
  if (prevPlaca && placas.includes(prevPlaca)) selPlaca.value = prevPlaca;
  if (prevLinha && linhas.includes(prevLinha)) selLinha.value = prevLinha;
}
