const API_BASE = (window.API_BASE || `${location.protocol}//${location.hostname}:5000/api`).replace(/\/+$/,'');

// Define cor padrão dos textos dos gráficos para branco
if (window.Chart && Chart.defaults) {
  Chart.defaults.color = '#fff';
  Chart.defaults.plugins.legend.labels.color = '#fff';
  Chart.defaults.plugins.tooltip.titleColor = '#fff';
  Chart.defaults.plugins.tooltip.bodyColor = '#fff';
}


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
  const el = document.getElementById('paradaMsg');
  if(el) el.textContent = t || '';
}

function getParadaIdFromURL(){
  const m = location.pathname.match(/\/paradas-detalhes\/(\d+)\b/);
  return m ? Number(m[1]) : null;
}

function isToday(ts){
  const d = new Date(ts);
  if(isNaN(d.getTime())) return false;
  const now = new Date();
  return d.getFullYear()===now.getFullYear() && d.getMonth()===now.getMonth() && d.getDate()===now.getDate();
}

function renderTabela(rows){
  const tbody = document.getElementById('tabelaParadaLinhas');
  if(!tbody) return;
  if(!rows.length){
    tbody.innerHTML = '<tr><td colspan="3" class="text-center">Nenhum dado encontrado</td></tr>';
    return;
  }
  tbody.innerHTML = rows.map(r=>{
    const link = r.linha
      ? `<a href="/linhas-detalhes?linha=${encodeURIComponent(r.linha)}" class="text-decoration-none">${r.linha}</a>`
      : '—';
    return `
      <tr>
        <td>${link}</td>
        <td>${r.hoje}</td>
        <td>${r.total}</td>
      </tr>`;
  }).join('');
}

// Novo: gráfico por hora (definição única mais abaixo com suporte a linhaCtx)
// Removida definição duplicada de paradaHoraChartInst e renderChartHoras para evitar erro de redeclaração.

let paradaLotacoesRaw = []; // registros de lotação relacionados à parada (para cálculo filtrado)
let paradaLinhasLista = []; // lista de linhas dessa parada

function collectParadaLotacoes(lotacoes, paradaNome){
  // Filtra só registros cujo parada_origem_nome é a parada atual
  return (lotacoes||[]).filter(r => (r.parada_origem_nome || '') === paradaNome);
}

function computeEmbarquesPorLinhaHora(filters){
  // Embarques = max(qtd_pessoas_atual - qtd_pessoas_anterior_viagem,0) somente quando origem = parada
  // Agrupamos por viagem para calcular diferença
  const { linhaFiltro, diaDe, diaAte, horaDe, horaAte } = filters;
  const tsDiaDe = diaDe ? new Date(diaDe + 'T00:00:00').getTime() : null;
  const tsDiaAte = diaAte ? new Date(diaAte + 'T23:59:59').getTime() : null;
  const horaMin = horaDe ? parseHora(horaDe) : null;
  const horaMax = horaAte ? parseHora(horaAte) : null;
  const wrapHora = (horaMin!=null && horaMax!=null && horaMax < horaMin);

  const porViagem = new Map();
  for(const r of paradaLotacoesRaw){
    if(linhaFiltro && r.linha_nome !== linhaFiltro) continue;
    // filtro por dia
    const ts = new Date(r.data_hora).getTime();
    if(tsDiaDe!=null && ts < tsDiaDe) continue;
    if(tsDiaAte!=null && ts > tsDiaAte) continue;
    // filtro por hora
    const h = new Date(r.data_hora).getHours();
    const hm = h; // hora inteiro
    if(horaMin!=null || horaMax!=null){
      if(horaMin!=null && horaMax==null && hm < horaMin) continue;
      if(horaMax!=null && horaMin==null && hm > horaMax) continue;
      if(horaMin!=null && horaMax!=null){
        if(!wrapHora && (hm < horaMin || hm > horaMax)) continue;
        if(wrapHora && !(hm >= horaMin || hm <= horaMax)) continue;
      }
    }
    const arr = porViagem.get(r.id_viagem) || [];
    arr.push(r);
    porViagem.set(r.id_viagem, arr);
  }

  const resultado = []; // {hora, linha, embarques}
  for(const [_, registros] of porViagem.entries()){
    const ordenados = registros.slice().sort((a,b)=> new Date(a.data_hora) - new Date(b.data_hora));
    let prevQtd = 0;
    let prevTs = null;
    for(const reg of ordenados){
      const qtd = Number(reg.qtd_pessoas||0);
      const diff = Math.max(qtd - prevQtd, 0);
      prevQtd = qtd;
      prevTs = reg.data_hora;
      const hora = new Date(reg.data_hora).getHours();
      resultado.push({ hora, linha: reg.linha_nome || '—', embarques: diff });
    }
  }

  // Aggregated por hora se linhaFiltro vazio (mostrar 'Todas'), senão discriminar por hora para linha
  if(!linhaFiltro){
    const arr24 = Array(24).fill(0);
    for(const item of resultado){
      if(item.hora>=0 && item.hora<24){
        arr24[item.hora] += item.embarques;
      }
    }
    return { tipo:'todas', arr24, detalhado: arr24.map((v,h)=>({hora:h,linha:'Todas',embarques:v})) };
  }else{
    // apenas registros da linha (já filtrado) -> consolidate por hora
    const arr24 = Array(24).fill(0);
    for(const item of resultado){
      if(item.hora>=0 && item.hora<24) arr24[item.hora] += item.embarques;
    }
    const detalhado = arr24.map((v,h)=>({hora:h,linha:linhaFiltro,embarques:v}));
    return { tipo:'linha', arr24, detalhado };
  }
}

function parseHora(hhmm){
  const m = /^(\d{2}):(\d{2})$/.exec(hhmm||'');
  if(!m) return null;
  return Number(m[1]); // só hora inteira para filtro
}

// Atualiza chart com array 24
let paradaHoraChartInst = null;
function renderChartHoras(arr24, linhaCtx){
  const ctx = document.getElementById('paradaHoraChart')?.getContext('2d');
  if(!ctx) return;
  if(paradaHoraChartInst) paradaHoraChartInst.destroy();
  const labels = Array.from({length:24}, (_,i)=>`${String(i).padStart(2,'0')}:00`);
  paradaHoraChartInst = new Chart(ctx, {
    type:'bar',
    data:{
      labels,
      datasets:[{
        label: linhaCtx ? `Embarques por hora (${linhaCtx})` : 'Embarques por hora (todas as linhas)',
        data: arr24,
        backgroundColor:'rgba(14,165,233,.6)',
        borderColor:'rgba(14,165,233,1)',
        borderWidth:2
      }]
    },
    options:{
      responsive:true,
      maintainAspectRatio:false,
      plugins:{ legend:{ display:true } },
      scales:{
        y:{ beginAtZero:true, title:{ display:true, text:'Passageiros'} },
        x:{ title:{ display:true, text:'Hora do dia'} }
      }
    }
  });
}

// Filtros
function getFiltrosHora(){
  return {
    linhaFiltro: document.getElementById('filtroLinha')?.value || '',
    diaDe: document.getElementById('filtroDiaDe')?.value || '',
    diaAte: document.getElementById('filtroDiaAte')?.value || '',
    horaDe: document.getElementById('filtroHoraDe')?.value || '',
    horaAte: document.getElementById('filtroHoraAte')?.value || '',
  };
}

function aplicarFiltrosHora(){
  const filtros = getFiltrosHora();
  const calc = computeEmbarquesPorLinhaHora(filtros);
  renderChartHoras(calc.arr24, filtros.linhaFiltro || '');
}

function setupFiltrosHora(){
  document.getElementById('btnAplicarFiltrosPH')?.addEventListener('click', aplicarFiltrosHora);
  document.getElementById('btnLimparFiltrosPH')?.addEventListener('click', ()=>{
    ['filtroLinha','filtroDiaDe','filtroDiaAte','filtroHoraDe','filtroHoraAte'].forEach(id=>{
      const el = document.getElementById(id); if(el) el.value='';
    });
    aplicarFiltrosHora();
  });
  // alteração imediata opcional
  ['filtroLinha','filtroDiaDe','filtroDiaAte','filtroHoraDe','filtroHoraAte'].forEach(id=>{
    document.getElementById(id)?.addEventListener('change', aplicarFiltrosHora);
  });
}

function popularSelectLinhasParada(){
  const sel = document.getElementById('filtroLinha');
  if(!sel) return;
  const linhasOrd = [...new Set(paradaLinhasLista.filter(Boolean))].sort((a,b)=>a.localeCompare(b,'pt-BR'));
  const current = sel.value;
  sel.innerHTML = '<option value="">(Todas)</option>' + linhasOrd.map(l=>`<option value="${l}">${l}</option>`).join('');
  if(current && linhasOrd.includes(current)) sel.value = current;
}

async function loadParadaDetalhes(){
  const id = getParadaIdFromURL();
  if(!id){
    setMsg('ID da parada não encontrado na URL.');
    renderTabela([]);
    return;
  }
  setMsg('Carregando detalhes da parada...');
  const [paradas, linhasRel, lotacoes, stats] = await Promise.all([
    api('/paradas') || [],
    api(`/paradas/${id}/linhas`) || [],
    api('/lotacao') || [],
    api('/paradas/pessoas-total') || []
  ]);

  const parada = Array.isArray(paradas) ? paradas.find(p=>p.id_parada===id) : null;
  if(parada){
    const t = document.getElementById('paradaTitulo');
    if(t) t.textContent = `Parada: ${parada.nome}`;
  }

  const totalApi = Array.isArray(stats) ? (stats.find(s => s.id_parada === id)?.pessoas_total || 0) : 0;
  setMsg(`Total de pessoas (todos os registros): ${totalApi}`);

  // Linhas da parada
  paradaLinhasLista = (linhasRel||[]).map(l=>l.linha_nome).filter(Boolean);
  popularSelectLinhasParada();

  // Dados por linha (tabela inferior)
  const linhasSet = new Set(paradaLinhasLista);
  const agg = new Map(); // linha -> { hoje,total }
  for(const nomeLinha of linhasSet){ agg.set(nomeLinha, { hoje:0, total:0 }); }
  for(const r of (lotacoes||[])){
    const nomParada = r.parada_origem_nome || '';
    if(!parada || nomParada !== parada.nome) continue;
    const nomeLinha = r.linha_nome || '—';
    if(!agg.has(nomeLinha)) agg.set(nomeLinha, { hoje:0, total:0 });
    const qtd = Number(r.qtd_pessoas || 0);
    const cur = agg.get(nomeLinha);
    cur.total += Number.isFinite(qtd) ? qtd : 0;
    if(isToday(r.data_hora)) cur.hoje += Number.isFinite(qtd) ? qtd : 0;
  }
  const rows = [...agg.entries()].map(([linha,vals])=>({ linha, ...vals }))
               .sort((a,b)=> a.linha.localeCompare(b.linha,'pt-BR'));
  renderTabela(rows);

  // Guardar lotações da parada para cálculos de embarque por hora e aplicar filtros no gráfico
  paradaLotacoesRaw = collectParadaLotacoes(lotacoes, parada?.nome || '');
  aplicarFiltrosHora();
  setupFiltrosHora();
}

document.addEventListener('DOMContentLoaded', loadParadaDetalhes);
