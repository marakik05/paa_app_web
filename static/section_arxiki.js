// Λογική για την Αρχική Σελίδα (διαχείριση φόρμας αναζήτησης ΑΦΜ και εμφάνιση αποτελεσμάτων)
document.addEventListener('DOMContentLoaded', () => {
    const afmSearch = document.getElementById('search-afm');

    afmSearch.addEventListener('input', () => {
        // Κρατάει ΜΟΝΟ ψηφία, μέχρι 9 χαρακτήρες — ίδια λογική με \d{0,9}
        afmSearch.value = afmSearch.value.replace(/\D/g, '').slice(0, 9);
        
    });});