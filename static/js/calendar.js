/* Kuroko Labs — FullCalendar init — Phase 2 */

const PLATFORM_COLORS = {
  linkedin:  '#000000',
  twitter:   '#333333',
  instagram: '#555555',
  threads:   '#888888',
};

// Phase 2: prefix characters for special post types
function eventPrefix(props) {
  const parts = [];
  if (props.is_longform)   parts.push('LF');
  if (props.is_evergreen)  parts.push('↺');
  if (props.is_repurposed) parts.push('↳');
  if (props.has_carousel)  parts.push('▣');
  return parts.length ? `[${parts.join(' ')}] ` : '';
}

document.addEventListener('DOMContentLoaded', function () {
  const el = document.getElementById('calendar');
  if (!el) return;

  const calendar = new FullCalendar.Calendar(el, {
    initialView: 'dayGridMonth',
    firstDay: 1,
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: '',
    },
    height: 'auto',
    events: '/api/calendar/events',
    eventColor: '#000000',

    eventContent: function(info) {
      const props = info.event.extendedProps || {};
      const platform = props.platform || 'linkedin';
      const color = PLATFORM_COLORS[platform] || '#000';
      const prefix = eventPrefix(props);
      const title = prefix + (info.event.title || '');
      return {
        html: `<div style="background:${color};color:#fff;padding:1px 4px;font-size:0.66rem;
                           font-family:'DM Mono',monospace;font-weight:500;overflow:hidden;
                           white-space:nowrap;text-overflow:ellipsis;" title="${info.event.title}">
                 ${title}
               </div>`
      };
    },

    eventClick: function (info) {
      const postId = info.event.extendedProps.post_id;
      if (!postId) return;

      htmx.ajax('GET', `/posts/${postId}`, {
        target: '#post-detail-panel',
        swap: 'innerHTML',
      });

      // Scroll detail panel into view on mobile
      const panel = document.getElementById('post-detail-panel');
      if (panel && window.innerWidth < 900) {
        panel.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    },
  });

  calendar.render();
});
