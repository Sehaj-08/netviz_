async function loadDevices() {
    const btn = document.getElementById("scanBtn");
    const loading = document.getElementById("loading");

    loading.style.display = "inline";
    btn.disabled = true;

    try {
        const res = await fetch("/devices");
        const devices = await res.json();

        const container = document.getElementById("devices");
        container.innerHTML = "";

        if (!devices || devices.length === 0) {
            container.innerHTML = "<p>No devices found.</p>";
            return;
        }

        devices.forEach(dev => {
            const card = document.createElement("div");
            card.className = "device-card";

            card.innerHTML = `
                <strong>IP:</strong> ${dev.ip}<br>
                <strong>MAC:</strong> ${dev.mac || "Unknown"}<br>
                <strong>Hostname:</strong> ${dev.hostname}<br>
                <strong>Latency:</strong> ${dev.latency_ms} ms<br>
                <strong>Last Seen:</strong> ${new Date(dev.last_seen * 1000).toLocaleString()}
            `;

            container.appendChild(card);
        });

        drawGraph(devices);

    } catch (err) {
        console.error("Error:", err);
    } finally {
        loading.style.display = "none";
        btn.disabled = false;
    }
}

function drawGraph(devices) {
    document.getElementById("graph").innerHTML =
        `<strong>Router</strong> → ${devices.length} connected device(s)`;
}

document.getElementById("scanBtn").addEventListener("click", loadDevices);
