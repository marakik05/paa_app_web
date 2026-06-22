
let _importNewData = [], _importConflicts = [];

// ─── Παρακολούθηση μη-αποθηκευμένων αλλαγών ───
let _hasUnsavedChanges = false;
function markDirty() { _hasUnsavedChanges = true; }
function markClean() { _hasUnsavedChanges = false; }

// ─── DOMContentLoaded — αγγίζει DOM, πρέπει να περιμένει ───
document.addEventListener('DOMContentLoaded', () => {

    // Σήμανση αλλαγών στα στοιχεία παραγωγού
    document.getElementById('name').addEventListener('input', markDirty);
    document.getElementById('surname').addEventListener('input', markDirty);
    document.getElementById('district').addEventListener('change', markDirty);

    // Γέμισμα combo περιφέρειας από το backend (≈ combo_periferia.addItems)
    fetch('/api/regions')
        .then(res => {
            if (!res.ok) throw new Error('http_error');
            return res.json();
        })
        .then(regions => {
            [document.getElementById('district'), document.getElementById('modal-district')]
                .forEach(select => {
                    select.innerHTML = '';
                    regions.forEach(region => {
                        const option = document.createElement('option');
                        option.value = region;
                        option.textContent = region;
                        select.appendChild(option);
                    });
                });
        })
        .catch(() => showToast('Σφάλμα φόρτωσης περιφερειών.'));

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

    // ─── Import ───
    document.getElementById('import').addEventListener('click', async () => {
        if (_hasUnsavedChanges &&
            !(await showConfirmModal('Υπάρχουν μη αποθηκευμένες αλλαγές που θα διαγραφούν με την εισαγωγή. Θέλετε να συνεχίσετε;'))) {
            return;
        }
        document.getElementById('import-file-input').value = '';
        document.getElementById('import-file-input').click();
    });

    document.getElementById('import-file-input').addEventListener('change', function() {
        if (!this.files[0]) return;
        const fd = new FormData();
        fd.append('file', this.files[0]);
        fetch('/api/import/parse', { method: 'POST', body: fd })
            .then(r => {
                if (!r.ok) throw new Error('http_error');
                return r.json();
            })
            .then(data => {
                if (!data.ok) { showToast(data.error || 'Σφάλμα εισαγωγής.'); return; }
                _importNewData = data.new_data;
                _importConflicts = data.conflicts;
                if (data.conflicts.length === 0) {
                    _executeImport({}, data.new_data);
                } else {
                    _showConflictModal(data.new_data, data.conflicts);
                }
            })
            .catch(() => showToast('Σφάλμα επικοινωνίας με τον server.'));
    });

    // ─── Export ───
    document.getElementById('export').addEventListener('click', () => {
        const afm = document.getElementById('AFM').value.trim();
        if (!afm) { showToast('Επιλέξτε παραγωγό πρώτα.'); return; }

        const payload = {
            name:    document.getElementById('name').value,
            surname: document.getElementById('surname').value,
            region:  document.getElementById('district').value,
            rows:    getTaRows(),
            totals: {
                total_ta:  document.getElementById('total-ta').textContent     || '',
                ta_prod:   document.getElementById('total-ta-sum').textContent  || '',
                ta_plant:  document.getElementById('total-ta-plant').textContent  || '',
                ta_animal: document.getElementById('total-ta-animal').textContent || '',
                ta_bees:   document.getElementById('total-ta-bee-silk').textContent || '',
            },
        };

        fetch(`/api/producer/${afm}/export`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        })
        .then(r => {
            if (!r.ok) throw new Error('http_error');
            return r.blob();
        })
        .then(blob => {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `${afm}_ΤΑ.xlsx`;
            a.click();
            URL.revokeObjectURL(url);
        })
        .catch(() => showToast('Σφάλμα εξαγωγής αρχείου.'));
    });



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
    .then(r => {
        if (!r.ok) throw new Error('http_error');
        return r.json();
    })
    .then(data => {
        if (data.ok) {
            showToast('Επιτυχής αποθήκευση!', 'success');
            markClean();
            loadProducersTable();
        } else {
            showToast('Σφάλμα κατά την αποθήκευση.');
        }
    })
    .catch(() => showToast('Σφάλμα επικοινωνίας με τον server.'));
});

    // Προειδοποίηση κλεισίματος καρτέλας/παραθύρου με μη-αποθηκευμένες αλλαγές
    window.addEventListener('beforeunload', (e) => {
        if (_hasUnsavedChanges) {
            e.preventDefault();
            e.returnValue = '';  // απαιτείται για να εμφανιστεί το native prompt
        }
    });

});

function _executeImport(decisions, producers) {
    fetch('/api/import/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ producers, decisions })
    })
    .then(r => {
        if (!r.ok) throw new Error('http_error');
        return r.json();
    })
    .then(data => {
        if (data.ok) {
            loadProducersTable();
            document.getElementById('AFM').value     = '';
            document.getElementById('name').value    = '';
            document.getElementById('surname').value = '';
            document.getElementById('district').selectedIndex = 0;
            markClean();
            lockTaSection();
            showToast(
                `Εισήχθησαν ${data.total_success} παραγωγοί` +
                (data.total_failed ? ` (${data.total_failed} σφάλματα)` : '') + '.',
                'success'
            );
        } else {
            showToast('Σφάλμα κατά την εισαγωγή.');
        }
    })
    .catch(() => showToast('Σφάλμα επικοινωνίας με τον server.'));
}

function _showConflictModal(newData, conflicts) {
    const list = document.getElementById('conflict-list');
    list.innerHTML = '';
    conflicts.forEach(c => {
        const row = document.createElement('div');
        row.style.cssText = 'display:flex;align-items:center;gap:8px;margin:4px 0';
        row.innerHTML =
            `<span style="flex:1">${c.afm} — ${c.name} ${c.surname}</span>
            <label><input type="radio" name="conf_${c.afm}" value="replace" checked> Αντικατάσταση</label>
            <label><input type="radio" name="conf_${c.afm}" value="skip"> Παράλειψη</label>`;
        list.appendChild(row);
    });
    document.getElementById('modal-import-conflict').style.display = 'block';

    document.getElementById('conflict-replace-all').onclick = () =>
        conflicts.forEach(c =>
            list.querySelector(`[name="conf_${c.afm}"][value="replace"]`).checked = true);
    document.getElementById('conflict-skip-all').onclick = () =>
        conflicts.forEach(c =>
            list.querySelector(`[name="conf_${c.afm}"][value="skip"]`).checked = true);
    document.getElementById('conflict-cancel').onclick = () =>
        document.getElementById('modal-import-conflict').style.display = 'none';
    document.getElementById('modal-conflict-close').onclick = () =>
        document.getElementById('modal-import-conflict').style.display = 'none';
    document.getElementById('conflict-confirm').onclick = () => {
        const decisions = {};
        conflicts.forEach(c => {
            decisions[c.afm] = list.querySelector(`[name="conf_${c.afm}"]:checked`).value;
        });
        document.getElementById('modal-import-conflict').style.display = 'none';
        const withFlag = conflicts.map(c => ({ ...c, _conflict: true }));
        _executeImport(decisions, newData.concat(withFlag));
    };
}

// Άνοιγμα modal
document.getElementById('new-record').addEventListener('click', () => {
    document.getElementById('modal-afm').value     = '';
    document.getElementById('modal-name').value    = '';
    document.getElementById('modal-surname').value = '';
    document.getElementById('modal-district').selectedIndex = 0;
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
    const region  = document.getElementById('modal-district').value;

    if (afm.length !== 9) { showToast('Ο ΑΦΜ πρέπει να είναι 9 ψηφία.'); return; }
    if (!name)    { showToast('Παρακαλώ συμπληρώστε Όνομα.'); return; }
    if (!surname) { showToast('Παρακαλώ συμπληρώστε Επώνυμο.'); return; }

    fetch(`/api/producer/${afm}/exists`)
        .then(r => {
            if (!r.ok) throw new Error('http_error');
            return r.json();
        })
        .then(({ exists }) => {
            if (exists) { showToast('Παραγωγός με αυτό το ΑΦΜ υπάρχει ήδη.'); return; }
            return fetch(`/api/producer/${afm}/save`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, surname, region })
            }).then(r => {
                if (!r.ok) throw new Error('http_error');
                return r.json();
            });
        })
        .then(data => {
            if (data && data.ok) {
                closeModal();
                loadProducersTable();
                showToast('Ο παραγωγός αποθηκεύτηκε!', 'success');
            } else if (data) {
                showToast('Σφάλμα κατά την αποθήκευση.');
            }
        })
        .catch(() => showToast('Σφάλμα επικοινωνίας με τον server.'));
});
