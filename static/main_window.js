// ─── Βοηθητικές — μόνο καθαρισμός DOM ───
function clearForm() {
    document.getElementById('AFM').value     = '';
    document.getElementById('name').value    = '';
    document.getElementById('surname').value = '';
    document.getElementById('district').selectedIndex = 0;
}

function clearFieldsExceptAfm() {
    document.getElementById('name').value    = '';
    document.getElementById('surname').value = '';
    document.getElementById('district').selectedIndex = 0;
}

// ─── Κύρια λογική ΑΦΜ (≈ on_afm_changed) ───
function handleAfmChanged(afm) {
    document.getElementById('save').disabled   = true;
    document.getElementById('export').disabled = true;
    document.getElementById('import').disabled = true;

    if (afm.length === 0) {
        clearForm();
        document.getElementById('import').disabled = false;
        return;
    }

    if (afm.length < 9) {
        clearFieldsExceptAfm();
        return;
    }

    // afm.length === 9 — ≈ fetch_producer(afm)
    clearFieldsExceptAfm();
    fetch(`/api/producer/${afm}/exists`)
        .then(res => res.json())
        .then(({ exists }) => {
            if (!exists) {
                // Δεν υπάρχει → νέα εγγραφή
                document.getElementById('save').disabled   = false;
                document.getElementById('export').disabled = false;
            } else {
                // Υπάρχει → πρέπει πρώτα φόρτωση
                document.getElementById('save').disabled   = true;
                document.getElementById('export').disabled = true;
            }
        })
        .catch(() => {
            // ≈ except Exception: ασφαλές fallback
            document.getElementById('save').disabled   = false;
            document.getElementById('export').disabled = false;
            document.getElementById('import').disabled = false;
        });
}

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

    // Εναλλαγή σελίδων μέσω data-page (≈ _on_current_page_changed)
    const navLinks = document.querySelectorAll('.navbar a[data-page]');
    const pages    = document.querySelectorAll('main [data-page-container]');
    navLinks.forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const target = link.dataset.page;
            pages.forEach(page => {
                page.hidden = page.dataset.pageContainer !== target;
            });
            navLinks.forEach(l => l.classList.toggle('active', l === link));
        });
    });

    // ΑΦΜ input — φιλτράρισμα + on_afm_changed (≈ QRegExpValidator + textChanged)
    const afmInput = document.getElementById('AFM');
    afmInput.addEventListener('input', () => {
        afmInput.value = afmInput.value.replace(/\D/g, '').slice(0, 9);
        handleAfmChanged(afmInput.value);
    });

});
