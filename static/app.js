(() => {
  const messages = document.querySelector('#messages');
  const input = document.querySelector('#message-input');
  const send = document.querySelector('#send-button');
  const suggestions = document.querySelector('#suggestions');
  const consentPanel = document.querySelector('#consent-panel');
  const toast = document.querySelector('#toast');
  let busy = false;
  let leadSubmitted = Boolean(window.LEAD_SUBMITTED);

  function addMessage(role, text, extra='') {
    const node = document.createElement('div');
    node.className = `message ${role} ${extra}`.trim();
    node.textContent = text;
    messages.appendChild(node);
    messages.scrollTop = messages.scrollHeight;
    return node;
  }
  function showToast(text) {
    toast.textContent = text; toast.classList.add('show');
    window.setTimeout(() => toast.classList.remove('show'), 4300);
  }
  function csrfToken() {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
    return cookie ? decodeURIComponent(cookie.split('=')[1]) : '';
  }
  function setProgress(value) {
    const n = Math.max(0, Math.min(100, Number(value) || 0));
    document.querySelector('#progress-bar').style.width = `${n}%`;
    document.querySelector('#progress-value').textContent = `${n}%`;
  }
  function toggleBusy(value) {
    busy = value; send.disabled = value || leadSubmitted;
    input.disabled = value || leadSubmitted;
  }
  (window.INITIAL_HISTORY || []).forEach(m => addMessage(m.role === 'user' ? 'user' : 'assistant', m.content));
  if (window.CONSENT_PENDING && !leadSubmitted) consentPanel.hidden = false;
  if (leadSubmitted) {
    addMessage('assistant', 'Votre demande a déjà été transmise. Merci pour votre confiance !');
    input.placeholder = 'Demande déjà transmise';
  }
  input.addEventListener('input', () => { input.style.height = 'auto'; input.style.height = `${Math.min(input.scrollHeight, 110)}px`; });
  async function sendMessage(value) {
    const text = (value ?? input.value).trim();
    if (!text || busy || leadSubmitted) return;
    addMessage('user', text);
    input.value = ''; input.style.height = 'auto';
    suggestions.hidden = true; consentPanel.hidden = true;
    const typing = document.createElement('div'); typing.className = 'message assistant'; typing.innerHTML = '<span class="typing" aria-label="MANaja écrit"><i></i><i></i><i></i></span>';
    messages.appendChild(typing); messages.scrollTop = messages.scrollHeight; toggleBusy(true);
    try {
      const response = await fetch('/api/chat', {method:'POST', headers:{'Content-Type':'application/json','X-CSRFToken':csrfToken()}, body:JSON.stringify({message:text})});
      const data = await response.json(); typing.remove();
      if (!response.ok) { addMessage('assistant', data.error || 'Une erreur est survenue. Réessayez.', 'error'); return; }
      addMessage('assistant', data.reply);
      setProgress(data.progress);
      if (data.consent_requested) consentPanel.hidden = false;
    } catch (_) {
      typing.remove(); addMessage('assistant', 'Impossible de joindre le service pour le moment. Vérifiez votre connexion et réessayez.', 'error');
    } finally { toggleBusy(false); input.focus(); }
  }
  send.addEventListener('click', () => sendMessage());
  input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); } });
  document.querySelectorAll('.suggestion').forEach(button => button.addEventListener('click', () => sendMessage(button.textContent)));
  document.querySelector('#consent-yes').addEventListener('click', async () => {
    const button = document.querySelector('#consent-yes'); button.disabled = true; button.textContent = 'Transmission…';
    try {
      const response = await fetch('/api/consent', {method:'POST', headers:{'Content-Type':'application/json','X-CSRFToken':csrfToken()}, body:JSON.stringify({consent:true})});
      const data = await response.json();
      if (!response.ok) { showToast(data.error || 'La demande n’a pas pu être transmise.'); return; }
      leadSubmitted = true; consentPanel.hidden = true; addMessage('assistant', data.message); setProgress(100);
      input.disabled = true; input.placeholder = 'Demande transmise — merci !';
      showToast(data.sheets === 'synced' ? `Demande enregistrée · Référence ${data.lead_id.slice(0,8)}` : `Demande prise en compte · Référence ${data.lead_id.slice(0,8)}`);
    } catch (_) { showToast('Erreur réseau. Votre autorisation n’a pas pu être traitée.'); }
    finally { button.disabled = false; button.textContent = 'Oui, transmettre ma demande'; }
  });
  document.querySelector('#consent-no').addEventListener('click', () => { consentPanel.hidden = true; showToast('Aucune donnée ne sera transmise sans votre accord.'); });
  document.querySelector('#new-chat').addEventListener('click', async () => {
    if (!window.confirm('Démarrer une nouvelle conversation ? L’historique local de cette session sera fermé.')) return;
    try { const r = await fetch('/api/reset', {method:'POST', headers:{'X-CSRFToken':csrfToken()}}); if (!r.ok) throw new Error(); window.location.reload(); }
    catch (_) { showToast('Impossible de démarrer une nouvelle conversation.'); }
  });
})();
