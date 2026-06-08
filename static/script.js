document.addEventListener('DOMContentLoaded', () => {
    // Γέμισμα του combo περιφέρειας από το backend
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
    const pages = document.querySelectorAll('main [data-page-container]');

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
});

// Εναλλαγή σελίδων μέσω data-page (≈ _on_current_page_changed)

const navLinks = document.querySelectorAll('.navbar a[data-page]');
const pages = document.querySelectorAll('main [data-page-container]');

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

// Επεξεργασία του πεδίου ΑΦΜ για να επιτρέπονται μόνο ψηφία και μέχρι 9 χαρακτήρες
const afmInput = document.getElementById('AFM');

afmInput.addEventListener('input', () => {
    // Κρατάει ΜΟΝΟ ψηφία, μέχρι 9 χαρακτήρες — ίδια λογική με \d{0,9}
    afmInput.value = afmInput.value.replace(/\D/g, '').slice(0, 9);
    handleAfmChanged(afmInput.value);
});

const afmSearch = document.getElementById('search-afm');

afmSearch.addEventListener('input', () => {
    // Κρατάει ΜΟΝΟ ψηφία, μέχρι 9 χαρακτήρες — ίδια λογική με \d{0,9}
    afmSearch.value = afmSearch.value.replace(/\D/g, '').slice(0, 9);
    
});

// Λογική που ενεργοποιείται όταν αλλάζει το πεδίο ΑΦΜ (≈ _on_afm_changed)
function handleAfmChanged(afm) {
    // Reset state — ≈ search_or_edit_performed = False, disable save/export/import
    document.getElementById('save').disabled = true;
    document.getElementById('export').disabled = true;
    document.getElementById('import').disabled = true;

    if (afm.length === 0) {
        // ≈ clear_ui() + lock actions + enable import
        clearForm();
        document.getElementById('import').disabled = false;
        return;
    }

    if (afm.length < 9) {
        // ≈ _lock_actions(False) + clear_ui_not_afm()
        clearFieldsExceptAfm();
        return;
    }

    // afm.length === 9 — ≈ fetch_producer(afm)
    fetch(`/api/producer/${afm}/exists`)
        .then(res => res.json())
        .then(({ exists }) => {
            clearFieldsExceptAfm();
            if (!exists) {
                // Δεν υπάρχει → νέα εγγραφή
                document.getElementById('save').disabled = false;
                document.getElementById('export').disabled = false;
            } else {
                // Υπάρχει → πρέπει πρώτα φόρτωση/search
                document.getElementById('save').disabled = true;
                document.getElementById('export').disabled = true;
            }
        })
        .catch(() => {
            // ≈ except Exception: ασφαλές fallback — άνοιξε τα πάντα
            document.getElementById('save').disabled = false;
            document.getElementById('export').disabled = false;
            document.getElementById('import').disabled = false;
        });
}