function rupees(value) {
  return `Rs. ${Number(value).toFixed(2)}`;
}

function calculateEnergyCharge(units) {
  if (units <= 100) {
    return units * 3;
  }
  if (units <= 300) {
    return 300 + (units - 100) * 5;
  }
  return 1300 + (units - 300) * 7;
}

function initThemeToggle() {
  const toggle = document.getElementById("themeToggle");
  if (!toggle) return;

  toggle.addEventListener("click", () => {
    document.documentElement.classList.toggle("dark");
    const isDark = document.documentElement.classList.contains("dark");
    localStorage.setItem("theme", isDark ? "dark" : "light");
  });
}

function initDashboardCharts() {
  if (!window.dashboardData || typeof Chart === "undefined") return;

  Chart.defaults.font.family = "Manrope, ui-sans-serif, system-ui, sans-serif";
  Chart.defaults.color = "#64748b";

  const usageCanvas = document.getElementById("usageChart");
  if (usageCanvas) {
    new Chart(usageCanvas, {
      type: "bar",
      data: {
        labels: window.dashboardData.labels,
        datasets: [
          {
            label: "Units Used",
            data: window.dashboardData.usage,
            borderRadius: 8,
            backgroundColor: "#395fe9",
            maxBarThickness: 42,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: {
            grid: { display: false },
          },
          y: {
            beginAtZero: true,
            grid: { color: "#e2e8f0" },
          },
        },
      },
    });
  }

  const revenueCanvas = document.getElementById("revenueChart");
  if (revenueCanvas) {
    new Chart(revenueCanvas, {
      type: "line",
      data: {
        labels: window.dashboardData.labels,
        datasets: [
          {
            label: "Revenue",
            data: window.dashboardData.revenue,
            borderColor: "#0f766e",
            backgroundColor: "rgba(15, 118, 110, 0.15)",
            fill: true,
            pointRadius: 3,
            pointBackgroundColor: "#0f766e",
            tension: 0.35,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: {
            grid: { display: false },
          },
          y: {
            beginAtZero: true,
            grid: { color: "#e2e8f0" },
          },
        },
      },
    });
  }

  const statusCanvas = document.getElementById("statusChart");
  if (statusCanvas) {
    new Chart(statusCanvas, {
      type: "doughnut",
      data: {
        labels: window.dashboardData.statusLabels,
        datasets: [
          {
            data: window.dashboardData.statusData,
            backgroundColor: ["#10b981", "#f59e0b"],
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "70%",
        plugins: {
          legend: {
            position: "bottom",
            labels: {
              boxWidth: 12,
              boxHeight: 12,
            },
          },
        },
      },
    });
  }
}

function initConsumerCharts() {
  if (!window.consumerDashboardData || typeof Chart === "undefined") return;

  Chart.defaults.font.family = "Manrope, ui-sans-serif, system-ui, sans-serif";
  Chart.defaults.color = "#64748b";

  const usageCanvas = document.getElementById("consumerUsageChart");
  if (usageCanvas) {
    new Chart(usageCanvas, {
      type: "bar",
      data: {
        labels: window.consumerDashboardData.labels,
        datasets: [
          {
            label: "Units",
            data: window.consumerDashboardData.usage,
            backgroundColor: "#395fe9",
            borderRadius: 8,
            maxBarThickness: 42,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
        },
        scales: {
          x: { grid: { display: false } },
          y: { beginAtZero: true, grid: { color: "#e2e8f0" } },
        },
      },
    });
  }

  const statusCanvas = document.getElementById("consumerStatusChart");
  if (statusCanvas) {
    new Chart(statusCanvas, {
      type: "doughnut",
      data: {
        labels: window.consumerDashboardData.statusLabels,
        datasets: [
          {
            data: window.consumerDashboardData.statusData,
            backgroundColor: ["#10b981", "#f59e0b"],
            borderWidth: 0,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: "70%",
        plugins: {
          legend: {
            position: "bottom",
            labels: { boxWidth: 12, boxHeight: 12 },
          },
        },
      },
    });
  }
}

function initBillPreview() {
  const previousInput = document.getElementById("id_previous_reading");
  const currentInput = document.getElementById("id_current_reading");
  const unitsNode = document.getElementById("previewUnits");
  const energyNode = document.getElementById("previewEnergy");
  const taxNode = document.getElementById("previewTax");
  const totalNode = document.getElementById("previewTotal");

  if (!previousInput || !currentInput || !unitsNode || !energyNode || !taxNode || !totalNode) {
    return;
  }

  const updatePreview = () => {
    const previous = Number(previousInput.value || 0);
    const current = Number(currentInput.value || 0);
    const units = Math.max(current - previous, 0);
    const energy = calculateEnergyCharge(units);
    const subtotal = energy + 100;
    const tax = subtotal * 0.05;
    const total = subtotal + tax;

    unitsNode.textContent = units;
    energyNode.textContent = rupees(energy);
    taxNode.textContent = rupees(tax);
    totalNode.textContent = rupees(total);
  };

  previousInput.addEventListener("input", updatePreview);
  currentInput.addEventListener("input", updatePreview);
  updatePreview();
}

function initIcons() {
  if (window.lucide && typeof window.lucide.createIcons === "function") {
    window.lucide.createIcons();
  }
}

document.addEventListener("DOMContentLoaded", () => {
  initThemeToggle();
  initDashboardCharts();
  initConsumerCharts();
  initBillPreview();
  initIcons();
});
