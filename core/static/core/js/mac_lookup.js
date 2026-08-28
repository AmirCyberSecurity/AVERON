const form = document.getElementById('lookupForm');
const input = document.getElementById('lookupInput');
const status = document.getElementById('lookupStatus');
const result = document.getElementById('lookupResult');
const table = document.getElementById('lookupResultTable');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const query = input.value.trim();

    if (!query) {
        status.className = 'lookup-status error';
        status.textContent = 'Enter a MAC address.';
        input.focus();
        return;
    }

    result.hidden = true;
    table.innerHTML = '';

    status.className = 'lookup-status loading';
    status.textContent = 'Lookup in progress...';

    try {
        const res = await fetch(
            `/start/mac_lookup/query/?query=${encodeURIComponent(query)}`,
            {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            }
        );

        const data = await res.json();

        if (!res.ok || data.error) {
            status.className = 'lookup-status error';
            status.textContent = data.error || 'Lookup failed.';
            return;
        }

        if (!data.fields || data.fields.length === 0) {
            status.className = 'lookup-status error';
            status.textContent = 'No data available for this address.';
            return;
        }

        data.fields.forEach(field => {
            const row = document.createElement('div');

            row.className = 'lookup-result-row';

            row.innerHTML = `
                <span class="lookup-result-key">${field.label}</span>
                <span class="lookup-result-value">${field.value}</span>
            `;

            table.appendChild(row);
        });

        status.className = 'lookup-status';
        status.textContent = '';
        result.hidden = false;

    } catch (err) {
        console.error(err);

        status.className = 'lookup-status error';
        status.textContent = 'Network error. Try again.';
    }
});