const API_BASE = (window.API_BASE || `${location.protocol}//${location.hostname}:5000/api`).replace(/\/+$/,'');

function viagemId(){
  const m = location.pathname.match(/\/viagens-detalhes\/(\d+)\b/);
  return m ? Number(m[1]) : null;
}

let trechosRaw = [];
let trechosSort = { key: 'data_hora', dir: 'asc' };

function setMsg(t){
  const el = document.getElementById('paradaMsg');
  if(el) el.textContent = t || '';
}

function fmtDT(str){
  if(!str) return '—';
  const d = new Date(str);
  if(isNaN(d.getTime())) return str;
  return d.toLocaleString('pt-BR');
}

async function api(ep){
  try{
    const r = await fetch(`${API_BASE}${ep}`);
    if(!r.ok) throw new Error(r.status);
    return await r.json();
  }catch(e){
    console.error('fetch', ep, e);
    setMsg(`Falha ao carregar ${ep}: ${e.message}`);
    return null;
  }
}

function compareTrechos(a,b,key){
  if(key==='data_hora'){
    const ta = new Date(a.data_hora).getTime() || 0;
    const tb = new Date(b.data_hora).getTime() || 0;
    return ta - tb;
  }
  if(key==='qtd_pessoas') return a.qtd_pessoas - b.qtd_pessoas;
  if(key==='pct_lotacao') return a._pct_lotacao - b._pct_lotacao;
  return 0;
}

function applySortAndRender(capacidade){
  const { key, dir } = trechosSort;
  const data = [...trechosRaw].sort((a,b)=>{
    const c = compareTrechos(a,b,key);
    return dir==='asc'?c:-c;
  });
  document.querySelectorAll('thead th.sortable').forEach(th=>{
    th.classList.remove('sort-asc','sort-desc');
    if(th.dataset.sortKey===key){
      th.classList.add(dir==='asc'?'sort-asc':'sort-desc');
    }
  });
  render(data, capacidade);
}

function setupSorting(capacidade){
  document.querySelectorAll('thead th.sortable').forEach(th=>{
    th.style.cursor='pointer';
    th.addEventListener('click', ()=>{
      const k = th.dataset.sortKey;
      if(!k) return;
      if(trechosSort.key===k){
        trechosSort.dir = trechosSort.dir==='asc'?'desc':'asc';
      }else{
        trechosSort.key = k;
        trechosSort.dir = k==='data_hora' ? 'asc' : 'desc';
      }
      applySortAndRender(capacidade);
    });
  });
}

function render(trechos, capacidade){
  const tbody = document.getElementById('vdTrechos');
  if(!tbody) return;
  if(!trechos.length){
    tbody.innerHTML = '<tr><td colspan="6" class="text-center">Sem registros</td></tr>';
    return;
  }
  tbody.innerHTML = trechos.map(t=>{
    const pct = capacidade>0 ? (t.qtd_pessoas / capacidade)*100 : 0;
    const pctTxt = `${pct.toFixed(1)}%`;
    const bar = `
      <div class="progress" style="height:14px">
        <div class="progress-bar ${pct>=100?'bg-danger': pct>=70?'bg-warning':'bg-success'}"
             role="progressbar"
             style="width:${Math.min(pct,120)}%"
             aria-valuenow="${pct.toFixed(1)}" aria-valuemin="0" aria-valuemax="100"></div>
      </div>`;

    // Links para detalhes da parada (se IDs presentes)
    const origemTxt = t.parada_origem_nome || '—';
    const destinoTxt = t.parada_destino_nome || '—';
    const origem = t.parada_origem_id
      ? `<a href="/paradas-detalhes/${t.parada_origem_id}" class="text-decoration-none">${origemTxt}</a>`
      : origemTxt;
    const destino = t.parada_destino_id
      ? `<a href="/paradas-detalhes/${t.parada_destino_id}" class="text-decoration-none">${destinoTxt}</a>`
      : destinoTxt;

    return `
      <tr>
        <td>${origem}</td>
        <td>${destino}</td>
        <td>${fmtDT(t.data_hora)}</td>
        <td>${t.qtd_pessoas}</td>
        <td>${pctTxt}</td>
        <td style="min-width:120px">${bar}</td>
      </tr>`;
  }).join('');
}

async function loadDetalhe(){
  const id = viagemId();
  if(!id){
    setMsg('ID da viagem não encontrado.');
    return;
  }
  setMsg('Carregando...');
  const [viagem, trechos] = await Promise.all([
    api(`/viagens/${id}`),
    api(`/viagens/${id}/trechos`)
  ]);
  if(viagem){
    const h = document.getElementById('vdTitulo');
    if(h) h.textContent = `Viagem #${viagem.id_viagem} - Linha ${viagem.linha_nome} - Ônibus ${viagem.placa}`;
  }
  const cap = trechos && trechos.length ? Number(trechos[0].capacidade||0) : 0;
  trechosRaw = Array.isArray(trechos)? trechos.map(t=>{
    const pct = cap>0 ? (t.qtd_pessoas/cap)*100 : 0;
    return { ...t, _pct_lotacao: pct };
  }):[];
  setupSorting(cap);
  applySortAndRender(cap);
  setMsg(`Total de trechos: ${trechosRaw.length} | Capacidade ônibus: ${cap}`);
}

document.addEventListener('DOMContentLoaded', loadDetalhe);
