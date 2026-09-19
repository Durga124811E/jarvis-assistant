const chatBox = document.getElementById('chat');
const messageInput = document.getElementById('messageInput');
const voiceBtn = document.getElementById('voiceBtn');

function addMessage(text, who = 'bot') {
  const div = document.createElement('div');
  div.className = `bubble ${who}`;
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendCommand(text) {
  const command = (text || messageInput.value || '').trim();
  if (!command) return;

  addMessage(command, 'user');
  messageInput.value = '';

  fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: command })
  })
    .then((res) => res.json())
    .then((data) => addMessage(data.reply, 'bot'))
    .catch(() => addMessage('Ultron could not process that request.', 'bot'));
}

document.getElementById('sendBtn').addEventListener('click', () => sendCommand());
messageInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendCommand();
});

document.querySelectorAll('.quick').forEach((btn) => {
  btn.addEventListener('click', () => sendCommand(btn.getAttribute('data-command')));
});

function createMiniEntry(label, value) {
  const row = document.createElement('div');
  row.textContent = `${label}: ${value}`;
  return row;
}

function refreshTradeList() {
  fetch('/api/trade')
    .then((r) => r.json())
    .then((data) => {
      const list = document.getElementById('tradeList');
      list.innerHTML = '';
      (data.trades || []).slice(-5).reverse().forEach((trade) => {
        list.appendChild(createMiniEntry(`${trade.symbol} ${trade.side}`, `${trade.entry} / ${trade.stop} / ${trade.target}`));
      });
    });
}

function refreshProjectList() {
  fetch('/api/project')
    .then((r) => r.json())
    .then((data) => {
      const list = document.getElementById('projectList');
      list.innerHTML = '';
      (data.projects || []).slice(-5).reverse().forEach((project) => {
        list.appendChild(createMiniEntry(project.title, project.due || project.status));
      });
    });
}

function refreshAppList() {
  fetch('/api/application')
    .then((r) => r.json())
    .then((data) => {
      const list = document.getElementById('appList');
      list.innerHTML = '';
      (data.applications || []).slice(-5).reverse().forEach((app) => {
        list.appendChild(createMiniEntry(app.company, app.role));
      });
    });
}

document.getElementById('saveTradeBtn').addEventListener('click', () => {
  const payload = {
    symbol: document.getElementById('tradeSymbol').value,
    side: document.getElementById('tradeSide').value,
    entry: document.getElementById('tradeEntry').value,
    stop: document.getElementById('tradeStop').value,
    target: document.getElementById('tradeTarget').value,
    note: document.getElementById('tradeNote').value,
  };

  fetch('/api/trade', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  }).then(() => refreshTradeList());
});

document.getElementById('saveProjectBtn').addEventListener('click', () => {
  const payload = {
    title: document.getElementById('projectTitle').value,
    due: document.getElementById('projectDue').value,
    status: 'planned'
  };

  fetch('/api/project', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  }).then(() => refreshProjectList());
});

document.getElementById('saveAppBtn').addEventListener('click', () => {
  const payload = {
    company: document.getElementById('appCompany').value,
    role: document.getElementById('appRole').value,
    status: 'applied'
  };

  fetch('/api/application', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  }).then(() => refreshAppList());
});

if ('speechSynthesis' in window) {
  function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1.1;
    utterance.lang = 'en-US';
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
  }

  const originalReply = (text) => addMessage(text, 'bot');

  function speakAndReply(text) {
    originalReply(text);
    speak(text);
  }

  // monkey patch chat response flow
  const originalFetch = window.fetch;
  window.fetch = function(url, options) {
    return originalFetch.call(this, url, options).then((response) => {
      if (url === '/api/chat' && options && options.method === 'POST') {
        return response.json().then((data) => {
          if (data.reply) {
            speakAndReply(data.reply);
          }
          return { json: () => Promise.resolve(data) };
        });
      }
      return response;
    });
  };
}

voiceBtn.addEventListener('click', () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    addMessage('Speech recognition is not available in this browser.', 'bot');
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.start();
  addMessage('Listening...', 'bot');

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    addMessage(transcript, 'user');
    sendCommand(transcript);
  };

  recognition.onerror = () => {
    addMessage('Could not understand the voice command.', 'bot');
  };
});

refreshTradeList();
refreshProjectList();
refreshAppList();
