const API_BASE = (window.API_BASE || `${location.protocol}//${location.hostname}:5000/api`).replace(/\/+$/,'');

async function api(ep){
  try{
    const r = await fetch(`${API_BASE}${ep}`);
    if(!r.ok) throw new Error(r.status);
    return await r.json();
  }catch(e){
    console.error('Erro fetch', ep, e);
    setMsg(`Falha ao buscar ${ep}: ${e.message}`);
    return null;
  }
}

function setMsg(t){
  const el = document.getElementById('paradasMsg');
  if(el) el.textContent = t || '';
}

let paradasRaw = [];
let paradasCache = [];
let paradasSort = { key:'nome', dir:'asc' };

function compareParada(a,b,key){
  if(key==='qtd_linhas') return a.qtd_linhas - b.qtd_linhas;
  if(key==='pessoas_total') return a.pessoas_total - b.pessoas_total;
  return a.nome.localeCompare(b.nome,'pt-BR');
}

function renderParadas(data){
  const tbody = document.getElementById('tabelaParadas');
  if(!tbody) return;
  if(!data.length){
    tbody.innerHTML = '<tr><td colspan="5" class="text-center">Nenhuma parada encontrada</td></tr>';
    return;
  }
  tbody.innerHTML = data.map(p=>{
    const linhasTxt = p.linhas.join(', ') || '—';
    return `<tr>
      <td>${p.nome}</td>
      <td>${p.qtd_linhas}</td>
      <td>${p.pessoas_total}</td>
      <td style="max-width:360px">${linhasTxt}</td>
      <td><a href="/paradas-detalhes/${p.id_parada}" class="btn btn-sm btn-outline-primary">Detalhes</a></td>
    </tr>`;
  }).join('');
}

function applySort(){
  const {key,dir} = paradasSort;
  const sorted = [...paradasCache].sort((a,b)=>{
    const c = compareParada(a,b,key);
    return dir==='asc'? c : -c;
  });
  document.querySelectorAll('thead th.sortable').forEach(th=>{
    th.classList.remove('sort-asc','sort-desc');
    if(th.dataset.sortKey===key) th.classList.add(dir==='asc'?'sort-asc':'sort-desc');
  });
  renderParadas(sorted);
}

function setupSorting(){
  document.querySelectorAll('thead th.sortable').forEach(th=>{
    th.style.cursor='pointer';
    th.addEventListener('click', ()=>{
      const k = th.dataset.sortKey;
      if(!k) return;
      if(paradasSort.key===k){
        paradasSort.dir = paradasSort.dir==='asc'?'desc':'asc';
      }else{
        paradasSort.key = k;
        paradasSort.dir = (k==='nome') ? 'asc' : 'desc';
      }
      applySort();
    });
  });
}

async function loadParadas(){
  setMsg('Carregando paradas...');
  const [paradas, stats] = await Promise.all([
    api('/paradas') || [],
    api('/paradas/pessoas-total') || []
  ]);
  if(!Array.isArray(paradas) || !paradas.length){
    paradasRaw = [];
    paradasCache = [];
    setMsg('Nenhuma parada encontrada.');
    renderParadas([]);
    return;
  }

  // Mapa id_parada -> pessoas_total (garante zero se não vier)
  const mapTotal = new Map();
  (stats||[]).forEach(s=>{
    mapTotal.set(s.id_parada, Number(s.pessoas_total)||0);
  });

  const rows = [];
  for(const p of paradas){
    const rel = await api(`/paradas/${p.id_parada}/linhas`) || [];
    const linhas = rel.map(x=>x.linha_nome);
    rows.push({
      id_parada: p.id_parada,
      nome: p.nome,
      linhas,
      qtd_linhas: linhas.length,
      pessoas_total: mapTotal.get(p.id_parada) || 0
    });
  }
  paradasRaw = rows;
  paradasCache = rows;
  setMsg(`Total de paradas: ${rows.length}`);
  applySort();
}

document.addEventListener('DOMContentLoaded', ()=>{
  loadParadas();
  setupSorting();
});
