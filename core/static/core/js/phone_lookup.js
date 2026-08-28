const form = document.getElementById("lookupForm");
const input = document.getElementById("lookupInput");
const status = document.getElementById("lookupStatus");
const result = document.getElementById("lookupResult");
const table = document.getElementById("lookupResultTable");
const dorksResult = document.getElementById("dorksResult");
const dorksTable = document.getElementById("dorksTable");

function normalizePhone(value) {
    value = value.replace(/＋/g, "+").replace(/[\u200E\u200F\u00A0]/g, "");

    const plus = value.trim().startsWith("+");

    value = value.replace(/[^\d+]/g, "");

    return plus
        ? "+" + value.replace(/\+/g, "")
        : value.replace(/\+/g, "");
}

function showDorks(dorks) {
    dorksTable.innerHTML = "";

    if (!dorks || !dorks.length) {
        dorksResult.hidden = true;
        return;
    }

    dorks.forEach(dork => {
        const row = document.createElement("a");

        row.className = "lookup-result-row dork-row";
        row.href = dork.url;
        row.target = "_blank";
        row.rel = "noopener noreferrer";

        row.innerHTML = `
            <span class="lookup-result-key dork-title">${dork.label}</span>
            <span class="lookup-result-value">${dork.query}</span>
        `;

        dorksTable.appendChild(row);
    });

    dorksResult.hidden = false;
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const query = normalizePhone(input.value);

    if (!query) {
        status.className = "lookup-status error";
        status.textContent = "Enter a phone number.";
        input.focus();
        return;
    }

    input.value = query;

    result.hidden = true;
    dorksResult.hidden = true;

    table.innerHTML = "";
    dorksTable.innerHTML = "";

    status.className = "lookup-status loading";
    status.textContent = "Lookup in progress...";

    try {
        const res = await fetch(
            `/start/phone_lookup/query/?query=${encodeURIComponent(query)}`,
            {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            }
        );

        const data = await res.json();

        if (!res.ok || data.error) {
            status.className = "lookup-status error";
            status.textContent = data.error || "Lookup failed.";
            return;
        }

        if (data.fields?.length) {
            data.fields.forEach(field => {
                const row = document.createElement("div");

                row.className = "lookup-result-row";

                row.innerHTML = `
                    <span class="lookup-result-key">${field.label}</span>
                    <span class="lookup-result-value">${field.value}</span>
                `;

                table.appendChild(row);
            });

            result.hidden = false;
        }

        showDorks(data.dorks);

        status.className = "lookup-status";
        status.textContent = "";

    } catch (err) {
        console.error(err);

        status.className = "lookup-status error";
        status.textContent = "Network error. Try again.";
    }
});