function showToast(msg, type = 'error') {
    const t = document.createElement('div');
    t.textContent = msg;
    t.className = `toast toast-${type}`;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}

// Styled modal αντί για native confirm() — επιστρέφει Promise<boolean>
function showConfirmModal(message, title = 'Επιβεβαίωση') {
    return new Promise(resolve => {
        document.getElementById('modal-confirm-title').textContent = title;
        document.getElementById('modal-confirm-message').textContent = message;
        const modal = document.getElementById('modal-confirm');
        modal.style.display = 'block';

        const okBtn = document.getElementById('modal-confirm-ok');
        const cancelBtn = document.getElementById('modal-confirm-cancel');
        const closeBtn = document.getElementById('modal-confirm-close');

        function close(result) {
            modal.style.display = 'none';
            okBtn.removeEventListener('click', onOk);
            cancelBtn.removeEventListener('click', onCancel);
            closeBtn.removeEventListener('click', onCancel);
            resolve(result);
        }
        function onOk()     { close(true); }
        function onCancel() { close(false); }

        okBtn.addEventListener('click', onOk);
        cancelBtn.addEventListener('click', onCancel);
        closeBtn.addEventListener('click', onCancel);
    });
}
