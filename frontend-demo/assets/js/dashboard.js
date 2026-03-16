/* ============================================================
   KUROKO LABS — Dashboard JS
   Week view calendar rendering + interactivity
   ============================================================ */

const DOW_LABELS = ['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'];
const MONTH_NAMES_DE = [
  'Januar','Februar','März','April','Mai','Juni',
  'Juli','August','September','Oktober','November','Dezember'
];

const PLATFORM_SHORT_CAL = {
  linkedin:  'LI',
  twitter:   'X',
  instagram: 'IG',
  threads:   'TH',
};

let currentWeekStart = getWeekStart(new Date(2026, 2, 16));
let selectedPostId = null;
let activePlatformFilter = 'all';

/* ── Helpers ── */
function pad(n) { return String(n).padStart(2, '0'); }

function fmtTime(iso) {
  const d = new Date(iso);
  return `${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

function fmtDate(iso) {
  const d = new Date(iso);
  return `${pad(d.getDate())}.${pad(d.getMonth()+1)}.${d.getFullYear()} ${fmtTime(iso)}`;
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

/* ── Week helpers ── */
function getWeekStart(date) {
  const d = new Date(date);
  const dow = (d.getDay() + 6) % 7;
  d.setDate(d.getDate() - dow);
  d.setHours(0, 0, 0, 0);
  return d;
}

function getWeekNumber(d) {
  const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  const dayNum = date.getUTCDay() || 7;
  date.setUTCDate(date.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
  return Math.ceil((((date - yearStart) / 86400000) + 1) / 7);
}

/* ── Sidebar stats ── */
function renderSidebar() {
  const el = (id) => document.getElementById(id);
  if (el('stat-total'))     el('stat-total').textContent     = STATS.totalMonth;
  if (el('stat-published')) el('stat-published').textContent = STATS.published;
  if (el('stat-scheduled')) el('stat-scheduled').textContent = STATS.scheduled;
  if (el('stat-pending'))   el('stat-pending').textContent   = STATS.pending;

  Object.entries(STATS.byPlatform).forEach(([pl, cnt]) => {
    const countEl = document.getElementById(`count-${pl}`);
    if (countEl) countEl.textContent = cnt;
  });
}

/* ── Week View ── */
function renderWeek(direction) {
  const weekEnd = new Date(currentWeekStart);
  weekEnd.setDate(weekEnd.getDate() + 6);
  const kw = getWeekNumber(currentWeekStart);

  // Build title: "KW 11 · März 2026"
  const titleEl = document.getElementById('cal-title');
  if (titleEl) {
    titleEl.textContent = `KW ${kw} · ${MONTH_NAMES_DE[currentWeekStart.getMonth()]} ${currentWeekStart.getFullYear()}`;
  }

  const grid = document.getElementById('cal-week-grid');
  if (!grid) return;

  const build = () => {
    grid.innerHTML = '';
    const today = new Date(2026, 2, 16);

    for (let i = 0; i < 7; i++) {
      const dayDate = new Date(currentWeekStart);
      dayDate.setDate(dayDate.getDate() + i);
      const isToday = dayDate.toDateString() === today.toDateString();
      const key = `${dayDate.getFullYear()}-${pad(dayDate.getMonth()+1)}-${pad(dayDate.getDate())}`;

      let posts = POSTS_BY_DATE[key] || [];
      if (activePlatformFilter !== 'all') {
        posts = posts.filter(p => p.platform === activePlatformFilter);
      }
      posts.sort((a, b) => new Date(a.scheduled_at) - new Date(b.scheduled_at));

      const col = document.createElement('div');
      col.className = `cal-day-col${isToday ? ' is-today' : ''}`;
      col.style.animationDelay = `${i * 0.04}s`;

      const postCountHtml = posts.length > 0
        ? `<div class="cal-post-count">${posts.length}</div>`
        : '<div class="cal-post-count"></div>';

      const postsHtml = posts.map(p => {
        const t = fmtTime(p.scheduled_at);
        const preview = escHtml(p.content.substring(0, 60));
        return `<div class="post-card p-${p.platform} s-${p.status}" onclick="openDetail(${p.id})" data-post-id="${p.id}">
          <div class="post-card-meta">
            <span class="post-card-platform">${PLATFORM_SHORT_CAL[p.platform] || p.platform}</span>
            <span class="post-card-time">${t}</span>
            <span class="status-dot-sm ${p.status}"></span>
          </div>
          <div class="post-card-preview">${preview}…</div>
        </div>`;
      }).join('');

      col.innerHTML = `
        <div class="cal-day-header">
          <div class="cal-dow-label">${DOW_LABELS[i]}</div>
          <div class="cal-date-num${isToday ? ' today' : ''}">${dayDate.getDate()}</div>
          ${postCountHtml}
        </div>
        <div class="cal-day-posts">
          ${postsHtml}
          ${posts.length === 0 ? '<div class="cal-empty-day">—</div>' : ''}
        </div>
      `;

      grid.appendChild(col);
    }
  };

  if (direction) {
    grid.className = 'cal-week-grid slide-out-' + direction;
    setTimeout(() => {
      build();
      const inDir = direction === 'left' ? 'right' : 'left';
      grid.className = 'cal-week-grid slide-in-' + inDir;
      setTimeout(() => { grid.className = 'cal-week-grid'; }, 300);
    }, 180);
  } else {
    build();
    grid.className = 'cal-week-grid';
  }
}

function prevWeek() {
  currentWeekStart.setDate(currentWeekStart.getDate() - 7);
  renderWeek('right');
}

function nextWeek() {
  currentWeekStart.setDate(currentWeekStart.getDate() + 7);
  renderWeek('left');
}

function goToday() {
  currentWeekStart = getWeekStart(new Date(2026, 2, 16));
  renderWeek(null);
}

/* ── Post detail ── */
function openDetail(postId) {
  const post = DEMO_POSTS.find(p => p.id === postId);
  if (!post) return;
  selectedPostId = postId;

  const panel = document.getElementById('detail-panel');
  const body = document.getElementById('detail-body');
  if (!panel || !body) return;

  const wordCount = post.content.trim().split(/\s+/).length;

  // Phase 2 feature tags
  const featureTags = [
    post.is_longform  ? '<span class="feature-tag longform">Longform</span>'   : '',
    post.is_evergreen ? '<span class="feature-tag evergreen">Evergreen ↺</span>' : '',
    post.is_repurposed? '<span class="feature-tag repurposed">Repurposed ↳</span>': '',
    post.carousel_pdf_path ? '<span class="feature-tag carousel">▣ Carousel</span>' : '',
  ].filter(Boolean).join('');

  // Engagement metrics (Phase 2)
  const maxLikes = Math.max(...DEMO_POSTS.filter(p => p.platform === post.platform).map(p => p.likes), 1);
  const engagementSection = post.status === 'published' ? `
    <div>
      <div class="label" style="margin-bottom:0.6rem;">Engagement</div>
      <div class="metrics-grid">
        ${[
          {label:'Likes', val: post.likes, cls:'likes', max: maxLikes},
          {label:'Comments', val: post.comments, cls:'comments', max: Math.max(1,Math.round(maxLikes*0.12))},
          {label:'Shares', val: post.shares, cls:'shares', max: Math.max(1,Math.round(maxLikes*0.08))},
          {label:'Reach', val: fmtBig(post.reach), cls:'reach', max: maxLikes*18, rawVal: post.reach},
          {label:'Impressions', val: fmtBig(post.impressions), cls:'', max: maxLikes*30, rawVal: post.impressions},
        ].map(m => `
          <div class="metric-item">
            <div class="metric-label">${m.label}</div>
            <div class="metric-value">${typeof m.val === 'number' ? m.val : m.val}</div>
            <div class="metric-bar-wrap">
              <div class="metric-bar-fill ${m.cls}" style="width:${Math.min(100, Math.round(((m.rawVal !== undefined ? m.rawVal : (typeof m.val === 'number' ? m.val : 0)) / m.max) * 100))}%"></div>
            </div>
          </div>
        `).join('')}
      </div>
    </div>` : '';

  // Repurposed banner
  const repurposedBanner = post.is_repurposed ? `
    <div class="repurposed-banner">
      ↳ <span>Repurposed von LinkedIn-Post #${post.repurposed_from_id} via Claude Haiku</span>
    </div>` : '';

  // Carousel section
  const carouselSection = post.carousel_pdf_path ? `
    <div>
      <div class="label" style="margin-bottom:0.45rem;">Carousel PDF</div>
      <div class="carousel-section">
        <div class="carousel-icon">▣</div>
        <div class="carousel-info">
          <div style="font-size:11px;font-weight:600;color:var(--text-primary);">10-Slide LinkedIn Carousel</div>
          <div class="carousel-path">${post.carousel_pdf_path}</div>
        </div>
        <button class="btn" style="font-size:9px;padding:.3rem .6rem;flex-shrink:0;" onclick="showToast('PDF-Download würde hier starten.')">↓ PDF</button>
      </div>
    </div>` : (post.platform === 'linkedin' ? `
    <div>
      <button class="btn" style="font-size:9px;padding:.3rem .7rem;width:100%;" onclick="generateCarousel(${post.id})">▣ Carousel generieren</button>
    </div>` : '');

  body.innerHTML = `
    <div>
      <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;flex-wrap:wrap;">
        <span class="platform-badge ${post.platform}">${PLATFORM_LABELS[post.platform]}</span>
        <span class="status-badge ${post.status}">${post.status}</span>
        ${featureTags}
      </div>
    </div>

    ${repurposedBanner}

    <div class="meta-row">
      <div class="meta-item">
        <span class="meta-item-label">Typ</span>
        <span class="meta-item-value">${post.post_type}</span>
      </div>
      <div class="meta-item">
        <span class="meta-item-label">Geplant</span>
        <span class="meta-item-value">${fmtDate(post.scheduled_at)}</span>
      </div>
      <div class="meta-item">
        <span class="meta-item-label">Wörter</span>
        <span class="meta-item-value">${wordCount}${post.is_longform ? ' ✦' : ''}</span>
      </div>
    </div>

    <div>
      <div class="label" style="margin-bottom:0.45rem;">Qualitäts-Score</div>
      <div class="quality-display">
        <div class="quality-num">${post.quality_score.toFixed(1)}</div>
        <div style="flex:1;">
          <div style="font-family:'JetBrains Mono',monospace;font-size:9px;color:var(--text-muted);margin-bottom:4px;">/ 10</div>
          <div class="quality-bar-wrap">
            <div class="quality-bar-fill" style="width:${post.quality_score * 10}%"></div>
          </div>
        </div>
      </div>
    </div>

    ${engagementSection}

    <div>
      <div class="label" style="margin-bottom:0.45rem;">Post-Inhalt</div>
      <div class="post-content-box">${escHtml(post.content)}</div>
    </div>

    ${post.image_path ? `
    <div>
      <div class="label" style="margin-bottom:0.45rem;">Bild (Gemini Imagen · SW Industrial 1080×1080)</div>
      <div class="post-img-preview">
        <div class="post-img-placeholder">1080 × 1080 px<br>SW Industrial</div>
      </div>
    </div>` : ''}

    ${carouselSection}

    <div class="detail-actions">
      ${post.status === 'pending' ? `
        <button class="btn primary" onclick="approvePost(${post.id})">Freigeben</button>
      ` : ''}
      ${post.status === 'scheduled' || post.status === 'pending' ? `
        <button class="btn" onclick="reschedulePost(${post.id})">Neu planen</button>
      ` : ''}
      <button class="btn" onclick="regeneratePost(${post.id})">Regenerieren</button>
      ${post.status !== 'published' ? `
        <button class="btn danger" onclick="deletePost(${post.id})">Löschen</button>
      ` : ''}
    </div>
  `;

  // Restore chat
  const chatMessages = document.getElementById('chat-messages');
  if (chatMessages) {
    chatMessages.innerHTML = `
      <div class="chat-msg assistant">Hallo! Ich bin der Kuroko Labs Social Agent. Wie soll ich diesen Post überarbeiten?</div>
    `;
  }

  openPanel();
}

function openPanel() {
  const panel = document.getElementById('detail-panel');
  if (panel) panel.classList.add('open');
}

function closePanel() {
  const panel = document.getElementById('detail-panel');
  if (panel) panel.classList.remove('open');
  selectedPostId = null;
}

/* ── Helpers ── */
function fmtBig(n) {
  if (n >= 1000) return (n / 1000).toFixed(1) + 'k';
  return String(n);
}

/* ── Action handlers ── */
function generateCarousel(postId) {
  showToast('Carousel-Generierung gestartet — reportlab PDF, 10 Slides, 1080×1080px…');
  const post = DEMO_POSTS.find(p => p.id === postId);
  if (post) {
    setTimeout(() => {
      post.carousel_pdf_path = `output/carousels/${post.post_type}_demo.pdf`;
      openDetail(postId);
      showToast('✓ Carousel PDF generiert');
    }, 2200);
  }
}

function approvePost(postId) {
  const post = DEMO_POSTS.find(p => p.id === postId);
  if (post) {
    post.status = 'scheduled';
    showToast('Post freigegeben — wird zu Buffer gesendet.');
    openDetail(postId);
    renderWeek(null);
    renderSidebar();
  }
}

function reschedulePost(postId) {
  showToast('Neu-Planung — Funktion in Produktion via Dashboard.');
}

function regeneratePost(postId) {
  showToast('Regenerierung via Claude API gestartet…');
}

function deletePost(postId) {
  showToast('Post gelöscht.');
  closePanel();
  renderWeek(null);
}

/* ── Chat ── */
function sendChat() {
  const input = document.getElementById('chat-input');
  if (!input || !input.value.trim()) return;

  const msg = input.value.trim();
  input.value = '';

  const messages = document.getElementById('chat-messages');
  if (!messages) return;

  const userEl = document.createElement('div');
  userEl.className = 'chat-msg user';
  userEl.textContent = msg;
  messages.appendChild(userEl);

  const thinkEl = document.createElement('div');
  thinkEl.className = 'chat-msg assistant';
  thinkEl.textContent = '…';
  messages.appendChild(thinkEl);
  messages.scrollTop = messages.scrollHeight;

  setTimeout(() => {
    thinkEl.remove();
    const replyEl = document.createElement('div');
    replyEl.className = 'chat-msg assistant';
    replyEl.textContent = getDemoReply(msg, selectedPostId);
    messages.appendChild(replyEl);
    messages.scrollTop = messages.scrollHeight;
  }, 900);
}

function getDemoReply(msg, postId) {
  const lower = msg.toLowerCase();
  if (lower.includes('kürz') || lower.includes('kurz') || lower.includes('wort')) {
    return 'Post wurde auf ~150 Wörter gekürzt. Kernaussage und Hashtags wurden beibehalten. Klicke auf „Freigeben" wenn die Version passt.';
  }
  if (lower.includes('informell') || lower.includes('locker') || lower.includes('ton')) {
    return 'Ton angepasst: etwas lockerer, direkte Ansprache stärker. Firmenperspektive bleibt erhalten.';
  }
  if (lower.includes('bild') || lower.includes('image') || lower.includes('foto')) {
    return 'Neues Bild-Prompt an Gemini Imagen gesendet. SW Industrial Stil, 1080×1080px. Generierung dauert ~8 Sekunden.';
  }
  if (lower.includes('hashtag')) {
    return 'Hashtags aktualisiert — stärker auf Zielgruppe (Fertigungsleiter DACH) ausgerichtet.';
  }
  if (lower.includes('länger') || lower.includes('mehr')) {
    return 'Post auf ~250 Wörter ausgebaut. Zweites Beispiel aus dem Quellartikel integriert.';
  }
  if (lower.includes('thema') || lower.includes('anders')) {
    return 'Neues Thema gesucht — TrendAnalyzer hat 3 Alternativen gefunden. Für welche Plattform soll das neue Thema optimiert sein?';
  }
  return 'Überarbeitung vorgenommen. Der aktualisierte Post ist bereit zur Freigabe.';
}

/* ── Toast notification ── */
function showToast(msg) {
  let toast = document.getElementById('toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'toast';
    toast.style.cssText = `
      position:fixed; bottom:1.75rem; left:50%; transform:translateX(-50%);
      background:var(--black); color:#fff; padding:0.65rem 1.25rem;
      font-family:'DM Sans',sans-serif; font-size:12px; font-weight:600;
      letter-spacing:0.04em; border-radius:6px;
      z-index:1000; opacity:0; transition:opacity 0.22s;
      pointer-events:none; white-space:nowrap;
      box-shadow: 0 4px 20px rgba(20,20,18,0.25);
    `;
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.style.opacity = '1';
  setTimeout(() => { toast.style.opacity = '0'; }, 2600);
}

/* ── Platform filter ── */
function setPlatformFilter(platform) {
  activePlatformFilter = platform;
  document.querySelectorAll('.platform-item').forEach(el => {
    el.classList.toggle('active', el.dataset.platform === platform);
  });
  renderWeek(null);
}

/* ── Chat keyboard ── */
function handleChatKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendChat();
  }
}

/* ── Init ── */
document.addEventListener('DOMContentLoaded', () => {
  renderWeek(null);
  renderSidebar();

  // Set platform filter listeners
  document.querySelectorAll('.platform-item[data-platform]').forEach(el => {
    el.addEventListener('click', () => setPlatformFilter(el.dataset.platform));
  });
});
