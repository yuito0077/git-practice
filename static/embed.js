(function() {
  // Styles for the floating button and iframe container
  const styles = `
    #embed-chat-widget-btn {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background: #38bdf8;
      color: #0f172a;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      z-index: 99999;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s, background 0.2s;
    }
    #embed-chat-widget-btn:hover {
      transform: scale(1.05);
      background: #7dd3fc;
    }
    #embed-chat-widget-btn svg {
      width: 30px;
      height: 30px;
      fill: currentColor;
    }
    #embed-chat-widget-container {
      position: fixed;
      bottom: 90px;
      right: 20px;
      width: 350px;
      height: 500px;
      border: none;
      border-radius: 12px;
      z-index: 99999;
      display: none;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      overflow: hidden;
    }
    #embed-chat-widget-iframe {
      width: 100%;
      height: 100%;
      border: none;
      background: transparent;
    }
  `;

  const styleEl = document.createElement('style');
  styleEl.innerHTML = styles;
  document.head.appendChild(styleEl);

  // Container for iframe
  const container = document.createElement('div');
  container.id = 'embed-chat-widget-container';

  const iframe = document.createElement('iframe');
  iframe.id = 'embed-chat-widget-iframe';
  // Use absolute URL based on script source if possible, or fallback to /embed
  let scriptSrc = document.currentScript ? document.currentScript.src : '';
  let baseUrl = '';
  if (scriptSrc) {
    try {
      const url = new URL(scriptSrc);
      baseUrl = url.origin;
    } catch(e) {}
  }
  iframe.src = baseUrl + '/embed';

  container.appendChild(iframe);
  document.body.appendChild(container);

  // Floating button
  const button = document.createElement('button');
  button.id = 'embed-chat-widget-btn';
  button.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>';

  button.onclick = function() {
    if (container.style.display === 'none' || container.style.display === '') {
      container.style.display = 'block';
      // Switch icon to close
      button.innerHTML = '<svg viewBox="0 0 24 24"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>';
    } else {
      container.style.display = 'none';
      // Switch back to chat icon
      button.innerHTML = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>';
    }
  };

  document.body.appendChild(button);
})();
