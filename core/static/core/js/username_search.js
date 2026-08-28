const form = document.getElementById("lookupForm");
const input = document.getElementById("lookupInput");
const status = document.getElementById("lookupStatus");
const result = document.getElementById("lookupResult");
const table = document.getElementById("lookupResultTable");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const query = input.value.trim();

    if (!query) {
        status.className = "lookup-status error";
        status.textContent = "Enter a username.";
        input.focus();
        return;
    }

    if (query.length < 3 || query.length > 20) {
        status.className = "lookup-status error";
        status.textContent = "Username must be between 3 and 20 characters.";
        return;
    }

    if (!/^[A-Za-z0-9._-]+$/.test(query)) {
        status.className = "lookup-status error";
        status.textContent = "Username contains invalid characters.";
        return;
    }

    result.hidden = true;
    table.innerHTML = "";

    status.className = "lookup-status loading";
    status.textContent = "Search in progress...";

    try {
        const res = await fetch(
            `/start/username_search/query/?query=${encodeURIComponent(query)}`,
            {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        );

        const data = await res.json();

        if (!res.ok || data.error) {
            status.className = "lookup-status error";
            status.textContent = data.error || "Search failed.";
            return;
        }

        if (!data.fields || data.fields.length === 0) {
            status.className = "lookup-status error";
            status.textContent = "No platforms found for this username.";
            return;
        }

        data.fields.forEach(field => {
            if (!field.url) return;

            const row = document.createElement("a");

            row.className = "lookup-result-row dork-row";
            row.href = field.url;
            row.target = "_blank";
            row.rel = "noopener noreferrer";

            row.innerHTML = `
                <span class="lookup-result-key dork-title">${field.label}</span>
                <span class="lookup-result-value">${field.value}</span>
            `;

            table.appendChild(row);
        });

        if (!table.children.length) {
            status.className = "lookup-status error";
            status.textContent = "No valid profiles found.";
            return;
        }

        result.hidden = false;
        status.className = "lookup-status";
        status.textContent = "";

    } catch (err) {
        console.error(err);
        status.className = "lookup-status error";
        status.textContent = "Network error. Try again.";
    }
});