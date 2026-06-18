function showToast(msg, color = 'red') {
    const t = document.createElement('div');
    t.textContent = msg;
    t.style.cssText = `position:fixed;top:150px;left:50%;transform:translateX(-50%);background:${color};
                       color:white;padding:10px 18px;border-radius:6px;z-index:9999`;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}
