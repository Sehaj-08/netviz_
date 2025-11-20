async function loadDevices() {
    const btn = document.getElementById("scanBtn");
    const loading = document.getElementById("loading");

    // Show loading ONLY when button is clicked
    loading.style.display = "inline";
    btn.disabled = true;

    try {
        const res = await fetch("/devices");
        const devices = await res.json();

        const devicesContainer = document.getElementById("devices");
        devicesContainer.innerHTML = "";

        if (!devices || devices.length === 0) {
            devicesContainer.innerHTML = "<p>No devices found.</p>";
            return;
        }

        devices.forEach(dev => {
            const div = document.createElement("div");
            div.className = "device-card";

            div.innerHTML = `
                <strong>IP:</strong> ${dev.ip}<br>
                <strong>MAC:</strong> ${dev.mac || "Unknown"}<br>
                <strong>Hostname:</strong> ${dev.hostname}<br>
                <strong>Latency:</strong> ${dev.latency_ms} ms<br>
                <strong>Last Seen:</strong> ${new Date(dev.last_seen * 1000).toLocaleString()}
            `;

            devicesContainer.appendChild(div);
        });

        drawGraph(devices);

    } catch (error) {
        console.error("Error fetching devices:", error);
    } finally {
        // Hide loading AFTER scan completes
        loading.style.display = "none";
        btn.disabled = false;
    }
}

function drawGraph(devices) {
    const graph = document.getElementById("graph");
    graph.innerHTML = `
        <strong>Router</strong> → ${devices.length} connected device(s)
    `;
}

// Scan happens ONLY on click now
document.getElementById("scanBtn").addEventListener("click", loadDevices);
