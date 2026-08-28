const form = document.getElementById('lookupForm');
const input = document.getElementById('lookupInput');
const status = document.getElementById('lookupStatus');
const result = document.getElementById('lookupResult');
const table = document.getElementById('lookupResultTable');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    let query = input.value.trim();

    if (!query) {
        status.className = 'lookup-status error';
        status.textContent = 'Enter a domain.';
        return;
    }

    query = query.replace(/^https?:\/\//i, '');
    query = query.replace(/^www\./i, '');
    query = query.split('/')[0];
    query = query.split('?')[0];
    query = query.split('#')[0];

    input.value = query;

    if (!query) {
        status.className = 'lookup-status error';
        status.textContent = 'Enter a domain.';
        return;
    }

    result.hidden = true;
    table.innerHTML = '';

    status.className = 'lookup-status loading';
    status.textContent = 'Lookup in progress...';

    try {
        const res = await fetch(
            `/start/domain_lookup/query/?query=${encodeURIComponent(query)}`,
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
            status.textContent = 'No data available for this domain.';
            return;
        }

        data.fields.forEach(field => {
            const row = document.createElement('div');
            row.className = 'lookup-result-row';

            const key = document.createElement('span');
            key.className = 'lookup-result-key';
            key.textContent = field.label;

            const value = document.createElement('span');
            value.className = 'lookup-result-value';
            value.textContent = field.value;

            row.appendChild(key);
            row.appendChild(value);
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