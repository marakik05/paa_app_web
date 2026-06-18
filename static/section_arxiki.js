let _allProducers = [];

//Συνάρτηση για το κουμπί επεξεργασίας παραγωγού
function handleEditClick(afm) {
    document.getElementById('AFM').value = afm;

    unlockTaSection();  // πρώτα ξεκλειδώνει το nav link "ΤΑ Αρχικής"
    document.querySelector('.navbar a[data-page="ta"]').click();  // μεταφορά στο section ΤΑ

    // καθαρισμός φίλτρων — ο χρήστης θα το αντιληφθεί όταν επιστρέψει στην Αρχική
    document.getElementById('search-afm').value     = '';
    document.getElementById('search-surname').value = '';
    _renderTable();

    loadProducer(afm);  // γεμίζει name/surname/district + τον πίνακα ΤΑ
}

//Συνάρτηση για το κουμπί διαγραφής παραγωγού
function handleDeleteClick(afm) {
    if (!confirm(`Διαγραφή παραγωγού με ΑΦΜ ${afm};`)) return;
    fetch(`/api/producer/${afm}`, { method: 'DELETE' })
        .then(r => r.json())
        .then(data => {
            if (!data.ok) { showToast('Σφάλμα κατά τη διαγραφή.'); return; }
            showToast('Ο παραγωγός διαγράφηκε.', 'green');
            loadProducersTable();
            if (document.getElementById('AFM').value === afm) {
                document.getElementById('AFM').value     = '';
                document.getElementById('name').value    = '';
                document.getElementById('surname').value = '';
                lockTaSection();;
            }
        });
}

// Σύνάρτηση φόρτωσης δεδομένων παραγωγού στην φόρμα
function loadProducer(afm) {
    fetch(`/api/producer/${afm}/full`)
        .then(r => r.json())
        .then(data => {
            if (!data.found) { showToast('Το ΑΦΜ δεν βρέθηκε στη βάση.'); return; }
            document.getElementById('name').value     = data.name;
            document.getElementById('surname').value  = data.surname;
            document.getElementById('district').value = data.region;
            loadTaTable(data.initial_rows || []);
            showToast('Τα δεδομένα φορτώθηκαν!', 'green');
        });
}

// ─── Helpers μορφοποίησης για τον πίνακα της αρχικής ───
function formatNumber(val) {
    return (val === null || val === undefined) ? '' : Number(val).toFixed(2);
}

function formatTimestamp(ts) {
    if (!ts) return '';
    const [datePart, timePart] = ts.split(' ');
    const [y, m, d] = datePart.split('-');
    const hm = timePart.slice(0, 5);
    return `${d}/${m}/${y} ${hm}`;
}

// ─── Απόδοση φιλτραρισμένων γραμμών στον πίνακα ───
function _renderTable() {
    const afmQ  = (document.getElementById('search-afm').value     || '').trim();
    const surnQ = (document.getElementById('search-surname').value  || '').trim().toLowerCase();
    const tbody = document.querySelector('#records-table tbody');
    tbody.innerHTML = '';

    _allProducers
        .filter(row => {
            const afm     = (row[0] || '');
            const surname = (row[2] || '').toLowerCase();
            return afm.includes(afmQ) && surname.includes(surnQ);
        })
        .forEach(row => {
            const [afm, firstName, lastName, region, initialTa, lastModified] = row;

            const tr = document.createElement('tr');
            tr.dataset.afm = afm;

            const cells = [afm, firstName, lastName, region, formatNumber(initialTa)];
            cells.forEach(value => {
                const td = document.createElement('td');
                td.textContent = value || '';
                tr.appendChild(td);
            });

            // Τελευταία Επεξεργασία
            const tsTd = document.createElement('td');
            tsTd.textContent = formatTimestamp(lastModified);
            tr.appendChild(tsTd);

            // Επεξεργασία
            const editTd = document.createElement('td');
            const editBtn = document.createElement('button');
            editBtn.type = 'button';
            editBtn.className = 'edit-btn';
            editBtn.textContent = 'Επεξεργασία';
            editBtn.dataset.afm = afm;
            editTd.appendChild(editBtn);
            tr.appendChild(editTd);

            // Διαγραφή
            const deleteTd = document.createElement('td');
            const deleteBtn = document.createElement('button');
            deleteBtn.type = 'button';
            deleteBtn.className = 'delete-btn';
            deleteBtn.textContent = 'Διαγραφή';
            deleteBtn.dataset.afm = afm;
            deleteTd.appendChild(deleteBtn);
            tr.appendChild(deleteTd);

            tbody.appendChild(tr);
        });
}

// ─── Γέμισμα πίνακα συγκεντρωτικών εγγραφών (≈ load_producers) ───
function loadProducersTable() {
    fetch('/api/producers')
        .then(r => r.json())
        .then(rows => {
            _allProducers = rows;
            _renderTable();
        });
}

// Λογική για την Αρχική Σελίδα
document.addEventListener('DOMContentLoaded', () => {
    const afmSearch  = document.getElementById('search-afm');
    const surnSearch = document.getElementById('search-surname');

    afmSearch.addEventListener('input', () => {
        afmSearch.value = afmSearch.value.replace(/\D/g, '').slice(0, 9);
        _renderTable();
    });

    surnSearch.addEventListener('input', _renderTable);

    // event delegation για edit/delete buttons
    const tbody = document.querySelector('#records-table tbody');
    tbody.addEventListener('click', (e) => {
        const afm = e.target.dataset.afm;
        if (!afm) return;
        if (e.target.classList.contains('edit-btn'))   handleEditClick(afm);
        if (e.target.classList.contains('delete-btn')) handleDeleteClick(afm);
    });

    // Αρχικό γέμισμα πίνακα
    loadProducersTable();
});
