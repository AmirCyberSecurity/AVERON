const form = document.getElementById('lookupForm');
const input = document.getElementById('lookupInput');
const status = document.getElementById('lookupStatus');
const result = document.getElementById('lookupResult');
const table = document.getElementById('lookupResultTable');

let source = null;
let scanRunning = false;

function normalizeDomain(value) {
    let query = value.trim();

    query = query.replace(/^https?:\/\//i, '');
    query = query.replace(/^www\./i, '');
    query = query.split('/')[0];
    query = query.split('?')[0];
    query = query.split('#')[0];

    return query.trim();
}

function addResult(data) {
    if (!data.url) {
        return;
    }

    result.hidden = false;

    const row = document.createElement("a");

    row.className = "lookup-result-row dork-row";
    row.href = data.url;
    row.target = "_blank";
    row.rel = "noopener noreferrer";

    row.innerHTML = `
        <span class="lookup-result-key dork-title">
            ${data.status ? `HTTP ${data.status}` : "FOUND"}
        </span>
        <span class="lookup-result-value">
            ${data.path || data.url}
        </span>
    `;

    table.appendChild(row);
}

function updateProgress(data) {
    if (typeof data.checked !== 'undefined' &&
        typeof data.total !== 'undefined') {

        status.textContent =
            `Scanning... ${data.checked} / ${data.total}`;
    }
}

function closeSource() {
    if (source) {
        source.close();
        source = null;
    }

    scanRunning = false;
}

form.addEventListener('submit', (e) => {
    e.preventDefault();

    if (scanRunning) {
        return;
    }

    let query = normalizeDomain(input.value);

    if (!query) {
        status.className = 'lookup-status error';
        status.textContent = 'Enter a domain.';
        return;
    }

    input.value = query;

    if (source) {
        source.close();
        source = null;
    }

    table.innerHTML = '';
    result.hidden = true;

    status.className = 'lookup-status loading';
    status.textContent = 'Starting directory lookup...';

    scanRunning = true;

    const url =
        `/start/directory_lookup/query/?query=${encodeURIComponent(query)}`;

    source = new EventSource(url);

    source.addEventListener('result', (event) => {
        try {
            const data = JSON.parse(event.data);

            addResult(data);

        } catch (err) {
            console.error('Invalid result event:', err);
        }
    });

    source.addEventListener('progress', (event) => {
        try {
            const data = JSON.parse(event.data);

            updateProgress(data);

        } catch (err) {
            console.error('Invalid progress event:', err);
        }
    });

    source.addEventListener('status', (event) => {
        try {
            const data = JSON.parse(event.data);

            if (data.message) {
                status.textContent = data.message;
            }

        } catch (err) {
            console.error('Invalid status event:', err);
        }
    });

    source.addEventListener('complete', (event) => {
        try {
            const data = JSON.parse(event.data);

            if (typeof data.checked !== 'undefined' &&
                typeof data.found !== 'undefined') {

                status.className = 'lookup-status';

                status.textContent =
                    `Scan completed · ${data.checked} checked · ${data.found} found`;

            } else {
                status.className = 'lookup-status';
                status.textContent = 'Scan completed.';
            }

        } catch (err) {
            status.className = 'lookup-status';
            status.textContent = 'Scan completed.';
        }

        closeSource();
    });

    source.addEventListener('error', (event) => {
        console.error('SSE error:', event);

        if (!scanRunning) {
            return;
        }

        status.className = 'lookup-status error';
        status.textContent = 'Target is unreachable.';
        closeSource();
    });

    source.onopen = () => {
        status.className = 'lookup-status loading';
        status.textContent = 'Directory lookup in progress...';
    };
});