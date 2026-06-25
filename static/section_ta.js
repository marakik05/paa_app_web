let taMapping = {};   // γεμίζει από /api/ta/reference

const CERTIFICATION_OPTIONS = ["--Επιλέξτε", "Συμβατικά", "Βιολογικά", "Ολοκληρωμένη", "ΠΟΠ/ΠΓΕ"];
const VINE_OPTIONS = ["--Επιλέξτε", "Ναι", "Όχι"];

function buildTaRow() {
    const tr = document.createElement('tr');

    // col 0: κατηγορία (searchable)
    const td0 = document.createElement('td');
    td0.dataset.col = '0';
    const allCats = Object.keys(taMapping);
    td0.appendChild(buildSearchableCombo(allCats, allCats[0] || ''));
    tr.appendChild(td0);

    // col 1: περιγραφή (searchable, δυναμική — γεμίζει από την πρώτη κατηγορία)
    const td1 = document.createElement('td');
    td1.dataset.col = '1';
    const firstCat = allCats[0] || '';
    const firstDescs = (taMapping[firstCat] || []).filter(d => d !== '--Επιλέξτε');
    td1.appendChild(buildSearchableCombo(['--Επιλέξτε', ...firstDescs], '--Επιλέξτε'));
    tr.appendChild(td1);

    // col 2: read-only (Τυπική Απόδοση — γεμίζει από server)
    const td2 = document.createElement('td');
    td2.dataset.col = '2';
    
    tr.appendChild(td2);

    // col 3: input έκτασης/αριθμού ζώων
    const td3 = document.createElement('td');
    td3.dataset.col = '3';
    const inp3 = document.createElement('input');
    inp3.type = 'text';
    inp3.inputMode = 'decimal';
    inp3.addEventListener('input', () => {
        // επιτρέπει μόνο ψηφία, κόμμα, τελεία
        inp3.value = inp3.value.replace(/[^0-9.,]/g, '');
    });
    inp3.addEventListener('change', () => {
    const v = parseFloat(inp3.value.replace(',', '.'));
    if (!isNaN(v)) inp3.value = String(v);
    });
    td3.appendChild(inp3);
    tr.appendChild(td3);

    // col 4: βιολογικά/πιστοποίηση
    const td4 = document.createElement('td');
    td4.dataset.col = '4';
    const sel4 = document.createElement('select');
    CERTIFICATION_OPTIONS.forEach(o => {
        const opt = document.createElement('option');
        opt.value = o; opt.textContent = o;
        sel4.appendChild(opt);
    });
    td4.appendChild(sel4);
    tr.appendChild(td4);

    // col 5: δένδρα >=4 ετών (ακέραιος)
    const td5 = document.createElement('td');
    td5.dataset.col = '5';
    const inp5 = document.createElement('input');
    inp5.type = 'text';
    inp5.inputMode = 'numeric';
    inp5.addEventListener('input', () => { inp5.value = inp5.value.replace(/\D/g, ''); });
    inp5.addEventListener('change', () => {
    const v = parseInt(inp5.value, 10);
    if (!isNaN(v)) inp5.value = String(v);
    });
    td5.appendChild(inp5);
    tr.appendChild(td5);

    // col 6: δένδρα <4 ετών (ακέραιος)
    const td6 = document.createElement('td');
    td6.dataset.col = '6';
    const inp6 = document.createElement('input');
    inp6.type = 'text';
    inp6.inputMode = 'numeric';
    inp6.addEventListener('input', () => { inp6.value = inp6.value.replace(/\D/g, ''); });
    inp6.addEventListener('change', () => {
    const v = parseInt(inp6.value, 10);
    if (!isNaN(v)) inp6.value = String(v);
    });
    td6.appendChild(inp6);
    tr.appendChild(td6);

    // col 7: αμπέλι >3 ετών
    const td7 = document.createElement('td');
    td7.dataset.col = '7';
    const sel7 = document.createElement('select');
    VINE_OPTIONS.forEach(o => {
        const opt = document.createElement('option');
        opt.value = o; opt.textContent = o;
        sel7.appendChild(opt);
    });
    td7.appendChild(sel7);
    tr.appendChild(td7);

    // col 8: read-only (ΤΑ ανά επιλογή — γεμίζει από server)
    const td8 = document.createElement('td');
    td8.dataset.col = '8';
    
    tr.appendChild(td8);

    // col 9: κουμπί διαγραφής γραμμής
    const td9 = document.createElement('td');
    td9.dataset.col = '9';
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'delete-row-btn';
    btn.textContent = '×';
    td9.appendChild(btn);
    tr.appendChild(td9);

    return tr;
}

function recalcAll() {
    const tbody = document.querySelector('#ta-table tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    const region = document.getElementById('district').value;

    // φτιάχνει το payload για τον server
    const payload = {
        region: region,
        rows: rows.map(tr => {
            const cells = tr.querySelectorAll('td');
            return {
                category:      cells[0].querySelector('.combo-input').value,
                description:   cells[1].querySelector('.combo-input').value,
                quantity:      cells[3].querySelector('input').value,
                trees_over_4:  cells[5].querySelector('input').value,
                trees_under_4: cells[6].querySelector('input').value,
                vine_over_3:   cells[7].querySelector('select').value,
            };
        })
    };

    fetch('/api/ta/recalculate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(r => {
        if (!r.ok) throw new Error('http_error');
        return r.json();
    })
    .then(data => {
        // ενημέρωση κάθε γραμμής
        rows.forEach((tr, i) => {
            const cells = tr.querySelectorAll('td');
            const rowData = data.rows[i];

            // col 2: τυπική απόδοση
            cells[2].textContent = rowData.typical_output !== null
                ? formatNumber(rowData.typical_output) : '';

            // col 8: ΤΑ ανά επιλογή
            cells[8].textContent = rowData.output_per_choice !== null
                ? formatNumber(rowData.output_per_choice) : '';

            // lock_trees: αν true → κατηγορία ΔΕΝ έχει δένδρα → disable cols 5,6
            const inp5 = cells[5].querySelector('input');
            const inp6 = cells[6].querySelector('input');
            if (rowData.lock_trees) {
                inp5.disabled = true; inp5.value = '';
                inp6.disabled = true; inp6.value = '';
            } else {
                inp5.disabled = false;
                inp6.disabled = false;
            }

            // lock_ampeli: αν true → κατηγορία είναι αμπέλι → enable col 7
            const sel7 = cells[7].querySelector('select');
            if (rowData.lock_ampeli) {
                sel7.disabled = false;
            } else {
                sel7.disabled = true;
                sel7.value = '--Επιλέξτε';
            }
        });

        // ενημέρωση tfoot (τα IDs που έβαλες στο HTML)
        const t = data.totals;
        document.getElementById('total-ta').textContent =
            t.total_output !== null ? formatNumber(t.total_output) : '';
        document.getElementById('total-ta-sum').textContent =
            t.ta_productive !== null ? formatNumber(t.ta_productive) : '';
        document.getElementById('total-ta-plant').textContent =
            t.ta_plant !== null ? formatNumber(t.ta_plant) : '';
        document.getElementById('total-ta-animal').textContent =
            t.ta_animal !== null ? formatNumber(t.ta_animal) : '';
        document.getElementById('total-ta-bee-silk').textContent =
            t.ta_bees !== null ? formatNumber(t.ta_bees) : '';
    })
    .catch(() => showToast('Σφάλμα επανυπολογισμού ΤΑ.'));
}

function buildSearchableCombo(options, initialValue) {
    const wrapper = document.createElement('div');
    wrapper.className = 'combo-wrapper';

    const input = document.createElement('input');
    input.type = 'text';
    input.className = 'combo-input';
    input.value = initialValue || options[0] || '';
    input.title = input.value;
    input.autocomplete = 'off';

    // portal: το dropdown ζει στο body ώστε να μην κόβεται από τον πίνακα
    const dropdown = document.createElement('div');
    dropdown.className = 'combo-dropdown combo-dropdown-portal';
    document.body.appendChild(dropdown);

    function positionDropdown() {
        const rect = input.getBoundingClientRect();
        dropdown.style.top   = (rect.bottom + window.scrollY) + 'px';
        dropdown.style.left  = (rect.left   + window.scrollX) + 'px';
        dropdown.style.width = rect.width + 'px';
    }

    function renderOptions(filter) {
        dropdown.innerHTML = '';
        const norm = filter.trim().toLowerCase();
        options.filter(o => o.toLowerCase().includes(norm)).forEach(o => {
            const item = document.createElement('div');
            item.className = 'combo-option';
            item.textContent = o;
            item.addEventListener('mousedown', e => {
                e.preventDefault(); // αποτρέπει blur πριν την επιλογή
                input.value = o;
                dropdown.style.display = 'none';
                input.dispatchEvent(new Event('change', { bubbles: true }));
            });
            dropdown.appendChild(item);
        });
        if (dropdown.children.length) {
            positionDropdown();
            dropdown.style.display = 'block';
        } else {
            dropdown.style.display = 'none';
        }
    }

    // επανατοποθέτηση αν ο χρήστης κάνει scroll ενώ το dropdown είναι ανοιχτό
    function onScroll() {
        if (dropdown.style.display === 'block') positionDropdown();
    }
    window.addEventListener('scroll', onScroll, true);

    input.addEventListener('change', () => { input.title = input.value; });
    input.addEventListener('focus', () => renderOptions(input.value));
    input.addEventListener('input', () => renderOptions(input.value));
    input.addEventListener('blur', () => {
        setTimeout(() => {
            dropdown.style.display = 'none';
            if (!options.includes(input.value)) {
                input.value = options[0] || '';
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }, 150); // αφήνει χρόνο για το mousedown της επιλογής
    });
    input.addEventListener('keydown', e => {
        if (e.key === 'Escape') { dropdown.style.display = 'none'; input.blur(); }
    });

    const arrow = document.createElement('button');
    arrow.type = 'button';
    arrow.className = 'combo-arrow';
    arrow.innerHTML = '&#9660;';
    arrow.addEventListener('mousedown', e => {
        e.preventDefault(); // αποτρέπει blur στο input
        if (dropdown.style.display === 'block') {
            dropdown.style.display = 'none';
        } else {
            input.focus();     // πρώτα focus (πυροδοτεί renderOptions(value))
            renderOptions('');  // μετά override → εμφανίζει ΟΛΕΣ τις επιλογές
        }
    });

    wrapper.appendChild(input);
    wrapper.appendChild(arrow);

    // references για cleanup (βλ. destroyCombo) — αποτρέπει memory leak από ορφανά
    // portal dropdowns στο body και πολλαπλασιαζόμενους scroll listeners
    wrapper._comboDropdown = dropdown;
    wrapper._comboOnScroll = onScroll;

    return wrapper;
}

// Αφαιρεί το portal dropdown από το body + τον scroll listener ενός combo cell.
// Πρέπει να καλείται πριν από κάθε innerHTML='' ή tr.remove() που πετάει ένα .combo-wrapper.
function destroyCombo(td) {
    const wrapper = td.querySelector('.combo-wrapper');
    if (!wrapper) return;
    if (wrapper._comboDropdown) wrapper._comboDropdown.remove();
    if (wrapper._comboOnScroll) window.removeEventListener('scroll', wrapper._comboOnScroll, true);
}

document.addEventListener('DOMContentLoaded', () => {

    // 1. φόρτωση κατηγοριών/περιγραφών από server
    fetch('/api/ta/reference')
        .then(r => {
            if (!r.ok) throw new Error('http_error');
            return r.json();
        })
        .then(data => { taMapping = data.mapping; })
        .catch(() => showToast('Σφάλμα φόρτωσης κατηγοριών ΟΣΔΕ.'));

    // 2. κουμπί "Προσθήκη"
    document.getElementById('add-row').addEventListener('click', () => {
        const tbody = document.querySelector('#ta-table tbody');
        tbody.appendChild(buildTaRow());
        markDirty();
        recalcAll();
    });

    // 3. event delegation — 1 listener για όλο το tbody
    const tbody = document.querySelector('#ta-table tbody');

    tbody.addEventListener('change', (e) => {
        const td = e.target.closest('td');
        if (!td) return;

        markDirty();
        // αν άλλαξε η κατηγορία (col 0) → ανανεώνει τις περιγραφές (col 1)
        if (td.dataset.col === '0') {
            const cells = td.closest('tr').querySelectorAll('td');
            const descs = (taMapping[e.target.value] || []).filter(d => d !== '--Επιλέξτε');
            destroyCombo(cells[1]);
            cells[1].innerHTML = '';
            cells[1].appendChild(buildSearchableCombo(['--Επιλέξτε', ...descs], '--Επιλέξτε'));
        }
        recalcAll();  // ανακαλεί σε κάθε αλλαγή (combo ή input)
    });

    let recalcTimer;
    tbody.addEventListener('input', (e) => {
        if (e.target.tagName === 'INPUT') {
            markDirty();
            clearTimeout(recalcTimer);
            recalcTimer = setTimeout(recalcAll, 350);
        }
    });

    tbody.addEventListener('click', (e) => {
        if (e.target.classList.contains('delete-row-btn')) {
            markDirty();
            const tr = e.target.closest('tr');
            const cells = tr.querySelectorAll('td');
            destroyCombo(cells[0]);
            destroyCombo(cells[1]);
            tr.remove();
            recalcAll();
        }
    });

    // 4. αλλαγή περιφέρειας → επανυπολογισμός ΤΑ (aegean vs default)
    document.getElementById('district').addEventListener('change', recalcAll);

    // 5. κλείδωμα section ΤΑ αρχικά — ξεκλειδώνει μόνο με "Επεξεργασία"
    lockTaSection();
});

// Κλειδώνει ΟΛΟ το section (disabled fieldset + nav link) + καθαρίζει δεδομένα
// + κλειδώνει name/surname/district όσο δεν είναι επιλεγμένος παραγωγός
function lockTaSection() {
    document.getElementById('ta-fieldset').disabled = true;
    document.getElementById('name').disabled     = true;
    document.getElementById('surname').disabled  = true;
    document.getElementById('district').disabled = true;
    document.querySelector('.navbar a[data-page="ta"]').classList.add('nav-disabled');
    const tbody = document.querySelector('#ta-table tbody');
    tbody.querySelectorAll('tr').forEach(tr => {
        const cells = tr.querySelectorAll('td');
        destroyCombo(cells[0]);
        destroyCombo(cells[1]);
    });
    tbody.innerHTML = '';
    ['total-ta','total-ta-sum','total-ta-plant','total-ta-animal','total-ta-bee-silk']
        .forEach(id => { document.getElementById(id).textContent = ''; });

    // αν ο χρήστης βρίσκεται στη σελίδα ΤΑ → επιστροφή στην Αρχική
    const taPage = document.querySelector('[data-page-container="ta"]');
    if (taPage && !taPage.hidden) {
        document.querySelector('.navbar a[data-page="arxiki"]').click();
    }
}

// Ξεκλειδώνει το section + nav link + name/surname/district (μετά από "Επεξεργασία")
function unlockTaSection() {
    document.getElementById('ta-fieldset').disabled = false;
    document.getElementById('name').disabled     = false;
    document.getElementById('surname').disabled  = false;
    document.getElementById('district').disabled = false;
    document.querySelector('.navbar a[data-page="ta"]').classList.remove('nav-disabled');
}

// Helpers: parse που επιστρέφει null μόνο σε NaN (0 παραμένει 0, δεν γίνεται null)
function numOrNull(v) {
    const n = parseFloat(String(v).replace(',', '.'));
    return Number.isNaN(n) ? null : n;
}
function intOrNull(v) {
    const n = parseInt(v, 10);
    return Number.isNaN(n) ? null : n;
}

// Διαβάζει τις γραμμές του πίνακα → 14-element arrays για αποθήκευση
function getTaRows() {
    const rows = Array.from(document.querySelectorAll('#ta-table tbody tr'));
    if (rows.length === 0) return [];
    const total_output  = numOrNull(document.getElementById('total-ta').textContent);
    const ta_productive = numOrNull(document.getElementById('total-ta-sum').textContent);
    const ta_plant      = numOrNull(document.getElementById('total-ta-plant').textContent);
    const ta_animal     = numOrNull(document.getElementById('total-ta-animal').textContent);
    const ta_bees       = numOrNull(document.getElementById('total-ta-bee-silk').textContent);

    return rows.map(tr => {
        const cells = tr.querySelectorAll('td');
        return [
            cells[0].querySelector('.combo-input').value,
            cells[1].querySelector('.combo-input').value,
            numOrNull(cells[2].textContent),
            numOrNull(cells[3].querySelector('input').value),
            cells[4].querySelector('select').value,
            intOrNull(cells[5].querySelector('input').value),
            intOrNull(cells[6].querySelector('input').value),
            cells[7].querySelector('select').value,
            numOrNull(cells[8].textContent),
            total_output, ta_productive, ta_plant, ta_animal, ta_bees
        ];
    });
}

// Γεμίζει τον πίνακα από DB rows (17-element arrays από fetch_entries)
function loadTaTable(rows) {
    const tbody = document.querySelector('#ta-table tbody');
    tbody.querySelectorAll('tr').forEach(tr => {
        const cells = tr.querySelectorAll('td');
        destroyCombo(cells[0]);
        destroyCombo(cells[1]);
    });
    tbody.innerHTML = '';
    rows.forEach(r => {
        const tr = buildTaRow();
        const cells = tr.querySelectorAll('td');
        const cat  = r[3] || '';
        const desc = r[4] || '--Επιλέξτε';
        cells[0].querySelector('.combo-input').value = cat;
        const descs = (taMapping[cat] || []).filter(d => d !== '--Επιλέξτε');
        destroyCombo(cells[1]);
        cells[1].innerHTML = '';
        cells[1].appendChild(buildSearchableCombo(['--Επιλέξτε', ...descs], desc));
        cells[3].querySelector('input').value  = r[6] != null ? String(r[6]) : '';
        cells[4].querySelector('select').value = r[7] || '--Επιλέξτε';
        cells[5].querySelector('input').value  = r[8] != null ? String(r[8]) : '';
        cells[6].querySelector('input').value  = r[9] != null ? String(r[9]) : '';
        cells[7].querySelector('select').value = r[10] || '--Επιλέξτε';
        tbody.appendChild(tr);
    });
    recalcAll();
}


