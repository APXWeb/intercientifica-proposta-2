/* Intercientifica · Proposta 2 · interface
   Tudo aqui melhora uma página que já funciona sem JavaScript. */
(() => {
  'use strict';
  const doc = document.documentElement;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const norm = (t) => (t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();

  /* ---------------------------------------------------------- pronto para o registro de entrada */
  const ready = () => doc.classList.add('is-ready');
  if (document.fonts && document.fonts.ready) {
    Promise.race([document.fonts.ready, new Promise((r) => setTimeout(r, 900))]).then(() => requestAnimationFrame(ready));
  } else {
    ready();
  }

  /* ---------------------------------------------------------- cabeçalho sobre áreas vermelhas */
  const mast = $('#mast');
  const reds = $$('.box, .ptop--red, .close, .nf');
  const mastH = () => (mast ? mast.offsetHeight : 68);
  let ticking = false;
  function paintMast() {
    ticking = false;
    if (!mast) return;
    const y = mastH() / 2;
    const over = reds.some((el) => {
      const r = el.getBoundingClientRect();
      return r.top <= y && r.bottom >= y;
    });
    mast.classList.toggle('is-on-red', over);
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(paintMast); } }, { passive: true });
  addEventListener('resize', paintMast);
  paintMast();

  /* ---------------------------------------------------------- menu móvel */
  const sheet = $('#sheet');
  const menuBtn = $('.mast__menu');
  let lastFocus = null;
  function openSheet() {
    lastFocus = document.activeElement;
    sheet.hidden = false;
    requestAnimationFrame(() => sheet.classList.add('is-open'));
    menuBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
    setTimeout(() => $('.sheet__close', sheet).focus(), 60);
  }
  function closeSheet() {
    sheet.classList.remove('is-open');
    menuBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    setTimeout(() => { if (!sheet.classList.contains('is-open')) sheet.hidden = true; }, reduceMotion ? 0 : 700);
    if (lastFocus) lastFocus.focus();
  }
  if (sheet && menuBtn) {
    menuBtn.addEventListener('click', openSheet);
    $('.sheet__close', sheet).addEventListener('click', closeSheet);
    $$('a', sheet).forEach((a) => a.addEventListener('click', closeSheet));
    sheet.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeSheet();
      if (e.key !== 'Tab') return;
      const f = $$('a, button', sheet);
      const first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
    matchMedia('(min-width: 961px)').addEventListener('change', (m) => { if (m.matches && sheet.classList.contains('is-open')) closeSheet(); });
  }

  /* ---------------------------------------------------------- revelações */
  const revealables = $$('[data-r], .lrow');
  if ('IntersectionObserver' in window && !reduceMotion) {
    // observa o pai: um alvo recortado por clip-path nunca "intersecta"
    const byParent = new Map();
    revealables.forEach((el) => {
      const host = el.parentElement;
      if (!byParent.has(host)) byParent.set(host, []);
      byParent.get(host).push(el);
    });
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        byParent.get(e.target).forEach((el) => el.classList.add('in'));
        io.unobserve(e.target);
      });
    }, { rootMargin: '0px 0px -10% 0px', threshold: 0 });
    byParent.forEach((_, host) => io.observe(host));
    // rede de segurança: nada fica escondido se o observador falhar
    setTimeout(() => revealables.forEach((el) => { if (el.getBoundingClientRect().top < innerHeight) el.classList.add('in'); }), 2500);
  } else {
    revealables.forEach((el) => el.classList.add('in'));
  }

  /* ---------------------------------------------------------- índice de kits: linha inteira clicável e prévia que segue o cursor */
  $$('.kits tbody tr').forEach((tr) => {
    tr.addEventListener('click', (e) => {
      if (e.target.closest('a')) return;
      const a = $('a.row-link', tr);
      if (a) location.href = a.href;
    });
  });
  const peek = $('#peek');
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  if (peek && fine) {
    const img = $('img', peek);
    let tx = 0, ty = 0, x = 0, y = 0, raf = 0, on = false;
    const loop = () => {
      x += (tx - x) * (reduceMotion ? 1 : 0.18);
      y += (ty - y) * (reduceMotion ? 1 : 0.18);
      peek.style.left = x + 'px';
      peek.style.top = y + 'px';
      raf = on || Math.abs(tx - x) > 0.5 ? requestAnimationFrame(loop) : 0;
    };
    $$('[data-peek] tbody').forEach((tb) => {
      tb.addEventListener('pointermove', (e) => {
        const tr = e.target.closest('tr');
        if (!tr || tr.classList.contains('is-hidden')) return;
        const src = tr.dataset.img;
        if (src && img.getAttribute('src') !== src) img.src = src;
        tx = e.clientX + 190; ty = e.clientY;
        if (tx + 160 > innerWidth) tx = e.clientX - 190;
        if (!on) { on = true; x = tx; y = ty; peek.classList.add('is-on'); }
        if (!raf) raf = requestAnimationFrame(loop);
      });
      tb.addEventListener('pointerleave', () => { on = false; peek.classList.remove('is-on'); });
    });
  }

  /* ---------------------------------------------------------- catálogo: filtros e busca */
  const filters = $('#filters');
  if (filters) {
    const rows = $$('.kits tbody tr');
    const q = $('#q'), count = $('#count'), empty = $('#empty'), reset = $('#reset');
    const total = rows.length;
    const params = new URLSearchParams(location.search);
    const setRadio = (name, v) => { const el = $(`input[name="${name}"][value="${v}"]`, filters); if (el) el.checked = true; };
    if (params.get('linha')) setRadio('line', params.get('linha'));
    if (params.get('formato')) setRadio('format', params.get('formato'));
    if (params.get('q')) q.value = params.get('q');
    function apply() {
      const line = $('input[name="line"]:checked', filters).value;
      const fmt = $('input[name="format"]:checked', filters).value;
      const words = norm(q.value).split(/\s+/).filter(Boolean);
      let shown = 0;
      rows.forEach((tr) => {
        const hay = norm(tr.dataset.search);
        const ok = (!line || tr.dataset.line === line) &&
          (!fmt || tr.dataset.formats.split(' ').includes(fmt)) &&
          words.every((w) => hay.includes(w));
        tr.classList.toggle('is-hidden', !ok);
        if (ok) shown++;
      });
      const filtered = line || fmt || words.length;
      count.textContent = filtered ? `${shown} de ${total} kits` : `${total} kits`;
      empty.hidden = shown !== 0;
      reset.hidden = !filtered;
      const p = new URLSearchParams();
      if (line) p.set('linha', line);
      if (fmt) p.set('formato', fmt);
      if (q.value.trim()) p.set('q', q.value.trim());
      history.replaceState(null, '', p.toString() ? `?${p}` : location.pathname);
    }
    const clear = () => { setRadio('line', ''); setRadio('format', ''); q.value = ''; apply(); q.focus(); };
    filters.addEventListener('input', apply);
    filters.addEventListener('submit', (e) => { e.preventDefault(); apply(); });
    reset.addEventListener('click', clear);
    $('#reset2').addEventListener('click', clear);
    apply();
  }

  /* ---------------------------------------------------------- publicações: filtros e busca */
  const pubf = $('#pubfilters');
  if (pubf) {
    const items = $$('.index-list li');
    const q = $('#pq'), count = $('#pcount'), empty = $('#pempty');
    const params = new URLSearchParams(location.search);
    if (params.get('tipo')) { const el = $(`input[name="kind"][value="${params.get('tipo')}"]`, pubf); if (el) el.checked = true; }
    if (params.get('q')) q.value = params.get('q');
    function apply() {
      const kind = $('input[name="kind"]:checked', pubf).value;
      const words = norm(q.value).split(/\s+/).filter(Boolean);
      let shown = 0;
      items.forEach((li) => {
        const ok = (!kind || li.dataset.kind === kind) && words.every((w) => norm(li.dataset.search).includes(w));
        li.hidden = !ok;
        if (ok) shown++;
      });
      count.textContent = (kind || words.length) ? `${shown} de ${items.length} publicações` : `${items.length} publicações`;
      empty.hidden = shown !== 0;
      const p = new URLSearchParams();
      if (kind) p.set('tipo', kind);
      if (q.value.trim()) p.set('q', q.value.trim());
      history.replaceState(null, '', p.toString() ? `?${p}` : location.pathname);
    }
    pubf.addEventListener('input', apply);
    pubf.addEventListener('submit', (e) => { e.preventDefault(); apply(); });
    apply();
  }

  /* ---------------------------------------------------------- mapa sob demanda */
  $$('[data-map-load]').forEach((btn) => btn.addEventListener('click', () => {
    const box = btn.closest('[data-map]');
    const f = document.createElement('iframe');
    f.src = window.MAP_SRC;
    f.title = 'Mapa com a localização da Intercientifica no Parque Tecnológico UNIVAP';
    f.loading = 'lazy';
    f.referrerPolicy = 'no-referrer-when-downgrade';
    box.innerHTML = '';
    box.appendChild(f);
  }));

  /* ---------------------------------------------------------- formulário: WhatsApp, sem simular envio */
  const form = $('#contact-form');
  if (form) {
    const p = new URLSearchParams(location.search);
    const subj = $('#assunto'), kit = $('#kit');
    if (p.get('assunto') && [...subj.options].some((o) => o.value === p.get('assunto'))) subj.value = p.get('assunto');
    if (p.get('kit') && [...kit.options].some((o) => o.value === p.get('kit'))) kit.value = p.get('kit');
    const status = $('#form-status');
    const rules = {
      nome: (v) => (v.trim().length >= 2 ? '' : 'Informe o seu nome.'),
      email: (v) => (/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()) ? '' : 'Informe um e-mail válido, como nome@laboratorio.com.br.'),
      tel: (v) => (!v.trim() || v.replace(/\D/g, '').length >= 8 ? '' : 'O telefone parece incompleto. Inclua o DDD.'),
      assunto: (v) => (v ? '' : 'Escolha um assunto para direcionarmos a sua mensagem.'),
      msg: (v) => (v.trim().length >= 10 ? '' : 'Escreva a sua mensagem (pelo menos 10 caracteres).'),
    };
    let tried = false;
    const check = (name) => {
      const el = form.elements[name];
      const msg = rules[name](el.value);
      const box = el.closest('.f');
      const err = $(`#${name}-err`);
      box.classList.toggle('is-invalid', !!msg);
      el.setAttribute('aria-invalid', msg ? 'true' : 'false');
      if (err) err.textContent = msg;
      return !msg;
    };
    Object.keys(rules).forEach((n) => {
      const el = form.elements[n];
      el.addEventListener('blur', () => { if (tried || el.value) check(n); });
      el.addEventListener('input', () => { if (tried) check(n); });
    });
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      tried = true;
      const bad = Object.keys(rules).filter((n) => !check(n));
      if (bad.length) {
        status.className = 'form__status is-error';
        status.textContent = bad.length === 1 ? 'Falta corrigir 1 campo.' : `Faltam corrigir ${bad.length} campos.`;
        form.elements[bad[0]].focus();
        return;
      }
      const f = form.elements;
      const kitOpt = kit.selectedOptions[0];
      const lines = [
        'Olá! Vim pelo site da Intercientifica.',
        '',
        `*Nome:* ${f.nome.value.trim()} ${f.sobrenome.value.trim()}`.trim(),
        f.org.value.trim() ? `*Laboratório ou instituição:* ${f.org.value.trim()}` : null,
        `*E-mail:* ${f.email.value.trim()}`,
        f.tel.value.trim() ? `*Telefone:* ${f.ddi.value} ${f.tel.value.trim()}` : null,
        `*Assunto:* ${f.assunto.value}`,
        kit.value ? `*Kit:* ${kitOpt.textContent} (REF. ${kitOpt.dataset.ref})` : null,
        '',
        f.msg.value.trim(),
      ].filter((l) => l !== null);
      const url = `https://wa.me/${form.dataset.whatsapp}?text=${encodeURIComponent(lines.join('\n').replace(/\n{3,}/g, '\n\n'))}`;
      const w = window.open(url, '_blank');
      status.className = 'form__status' + (w ? ' is-ok' : '');
      if (w) {
        try { w.opener = null; } catch (_) { /* ignorado */ }
        status.innerHTML = 'Abrimos o WhatsApp em uma nova aba com a sua mensagem. <strong>Ela ainda não foi enviada:</strong> confira e toque em enviar no WhatsApp. Se a aba não apareceu, <a target="_blank" rel="noopener">abra o WhatsApp por este link</a>.';
      } else {
        status.innerHTML = 'O navegador bloqueou a nova aba. <a target="_blank" rel="noopener">Abra o WhatsApp por este link</a> para enviar a sua mensagem.';
      }
      $('a', status).href = url;
    });
  }

  /* ---------------------------------------------------------- princípio: narrativa presa ao scroll */
  const story = $('#story');
  if (story) {
    const steps = $$('.step', story);
    const stage = $('#stage');
    const plates = $$('.plate-svg', stage);
    const countN = $('[data-count]', stage), countL = $('[data-count-label]', stage);
    const labels = ['Coleta', 'Picotagem', 'Ensaio multiplex', 'Leitura'];
    story.classList.add('is-live');
    let active = -1;
    function setStep(i) {
      if (i === active) return;
      active = i;
      steps.forEach((s, k) => s.classList.toggle('is-active', k === i));
      stage.dataset.step = i;
      plates.forEach((pl, k) => pl.classList.toggle('is-on', k === i));
      countN.textContent = i + 1;
      countL.textContent = labels[i];
    }
    // progresso contínuo (0 a 3) lido pelo WebGL
    function measure() {
      const vh = innerHeight;
      // no celular o palco fica preso no topo: a etapa só vira ativa quando o título aparece abaixo dele
      const narrow = innerWidth < 900;
      const centers = steps.map((s) => { const r = s.getBoundingClientRect(); return narrow ? r.top : r.top + r.height / 2; });
      const stageBottom = narrow ? stage.getBoundingClientRect().bottom : 0;
      const mid = narrow ? stageBottom + (vh - stageBottom) * 0.6 : vh * 0.5;
      let prog = 0;
      for (let i = 0; i < centers.length - 1; i++) {
        const a = centers[i], b = centers[i + 1];
        if (mid >= b) prog = i + 1;
        else if (mid > a) { prog = i + (mid - a) / (b - a); break; }
        else break;
      }
      window.__storyProgress = Math.max(0, Math.min(3, prog));
      setStep(Math.max(0, Math.min(3, Math.round(window.__storyProgress))));
    }
    let t2 = false;
    addEventListener('scroll', () => { if (!t2) { t2 = true; requestAnimationFrame(() => { t2 = false; measure(); }); } }, { passive: true });
    addEventListener('resize', measure);
    measure();
  }
})();
