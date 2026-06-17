

// ─── DOMContentLoaded — αγγίζει DOM, πρέπει να περιμένει ───
document.addEventListener('DOMContentLoaded', () => {

    // Γέμισμα combo περιφέρειας από το backend (≈ combo_periferia.addItems)
    fetch('/api/regions')
        .then(res => res.json())
        .then(regions => {
            const select = document.getElementById('district');
            select.innerHTML = '';
            regions.forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.textContent = region;
                select.appendChild(option);
            });
        });

    // Ενεργοποίηση/απενεργοποίηση κουμπιών ανά σελίδα
    function updatePageButtons(targetPage) {
        const arxikiOnly = ['new-record', 'import'];
        const isArxiki = targetPage === 'arxiki';
        arxikiOnly.forEach(id => {
            document.getElementById(id).disabled = !isArxiki;
        });
    }

    // Εναλλαγή σελίδων μέσω data-page (≈ _on_current_page_changed)
    const navLinks = document.querySelectorAll('.navbar a[data-page]');
    const pages    = document.querySelectorAll('main [data-page-container]');
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            if (link.classList.contains('nav-disabled')) return;  // κλειδωμένη σελίδα
            const target = link.dataset.page;
            pages.forEach(page => {
                page.hidden = page.dataset.pageContainer !== target;
            });
            navLinks.forEach(l => l.classList.toggle('active', l === link));
            updatePageButtons(target);
        });
    });

    // Αρχική κατάσταση: η Αρχική είναι ενεργή → τα κουμπιά ενεργά
    updatePageButtons('arxiki');

    

    document.getElementById('save').addEventListener('click', () => {
    const afm = document.getElementById('AFM').value.trim();
    if (!afm) { showToast('Παρακαλώ επιλέξτε παραγωγό πρώτα!'); return; }

    const payload = {
        name:    document.getElementById('name').value.trim(),
        surname: document.getElementById('surname').value.trim(),
        region:  document.getElementById('district').value,
        initial_rows: getTaRows(),
    };

    fetch(`/api/producer/${afm}/save`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => r.json())
    .then(data => {
        if (data.ok) {
            showToast('Επιτυχής αποθήκευση!', 'green');
            loadProducersTable();
        }
    });
});

});

// Άνοιγμα modal
document.getElementById('new-record').addEventListener('click', () => {
    document.getElementById('modal-afm').value     = '';
    document.getElementById('modal-name').value    = '';
    document.getElementById('modal-surname').value = '';
    document.getElementById('modal-new-record').style.display = 'block';
    document.getElementById('modal-afm').focus();
});

// Κλείσιμο
function closeModal() { document.getElementById('modal-new-record').style.display = 'none'; }
document.getElementById('modal-close').addEventListener('click', closeModal);
document.getElementById('modal-cancel').addEventListener('click', closeModal);
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

// Φιλτράρισμα ΑΦΜ στο modal
document.getElementById('modal-afm').addEventListener('input', () => {
    const inp = document.getElementById('modal-afm');
    inp.value = inp.value.replace(/\D/g, '').slice(0, 9);
});

// Αποθήκευση από modal
document.getElementById('modal-save').addEventListener('click', () => {
    const afm     = document.getElementById('modal-afm').value.trim();
    const name    = document.getElementById('modal-name').value.trim();
    const surname = document.getElementById('modal-surname').value.trim();

    if (afm.length !== 9) { showToast('Ο ΑΦΜ πρέπει να είναι 9 ψηφία.'); return; }
    if (!name)    { showToast('Παρακαλώ συμπληρώστε Όνομα.'); return; }
    if (!surname) { showToast('Παρακαλώ συμπληρώστε Επώνυμο.'); return; }

    fetch(`/api/producer/${afm}/exists`)
        .then(r => r.json())
        .then(({ exists }) => {
            if (exists) { showToast('Παραγωγός με αυτό το ΑΦΜ υπάρχει ήδη.'); return; }
            return fetch(`/api/producer/${afm}/save`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, surname, region: '--Επιλέξτε' })
            });
        })
        .then(r => r && r.json())
        .then(data => {
            if (data && data.ok) {
                closeModal();
                loadProducersTable();
                showToast('Ο παραγωγός αποθηκεύτηκε!', 'green');
            }
        });
});
