const toggle = document.getElementById('toggle-theme');
toggle.addEventListener('click', () => {
  const html = document.documentElement;
  html.classList.toggle('dark');
  const icon = toggle.querySelector('i');
  icon.classList.toggle('fa-moon');
  icon.classList.toggle('fa-sun');
  icon.classList.add('animate-spin');
  setTimeout(() => icon.classList.remove('animate-spin'), 400);
});

Chart.defaults.plugins.animation = {
  duration: 1200,
  easing: 'easeOutQuart',
};

document.addEventListener('DOMContentLoaded', () => {
  const formContainer = document.getElementById('metrics-form-container');
  const submitBtn = document.getElementById('submit-btn');
  const ctxMain = document.getElementById('metrics-chart').getContext('2d');
  const ctxTrend = document.getElementById('trend-chart').getContext('2d');
  let mainChart, trendChart;

  submitBtn.addEventListener('click', async (e) => {
    e.preventDefault();

    const start = document.getElementById('start-date').value;
    const end = document.getElementById('end-date').value;
    const res = await fetch(`/api/metrics?start_date=${start}&end_date=${end}`);
    const data = await res.json();

    const total = data.counts.reduce((a, b) => a + b, 0);
    const avg = (total / data.counts.length).toFixed(2);
    const maxCount = Math.max(...data.counts);
    const peakDay = data.dates[data.counts.indexOf(maxCount)];

    // Animate UI updates
    const animateValue = (id, start, end, duration) => {
      let startTimestamp = null;
      const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        document.getElementById(id).textContent = Math.floor(progress * (end - start) + start);
        if (progress < 1) {
          window.requestAnimationFrame(step);
        }
      };
      window.requestAnimationFrame(step);
    };

    animateValue('total-detections', 0, total, 1200);
    animateValue('avg-detections', 0, avg, 1200);
    animateValue('max-count', 0, maxCount, 1200);
    document.getElementById('peak-day').textContent = peakDay;

    // Destroy existing charts
    if (mainChart) mainChart.destroy();
    if (trendChart) trendChart.destroy();

    // Main Bar Chart
    mainChart = new Chart(ctxMain, {
      type: 'bar',
      data: {
        labels: data.dates,
        datasets: [{
          label: 'Daily Detections',
          data: data.counts,
          backgroundColor: 'rgba(30, 64, 175, 0.9)',
          borderColor: 'rgba(30, 64, 175, 1)',
          borderWidth: 1,
          borderRadius: 12,
          hoverBackgroundColor: 'rgba(30, 64, 175, 1)',
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            cornerRadius: 10,
            padding: 14,
            titleFont: { size: 14, weight: 'bold' },
            bodyFont: { size: 12 },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { stepSize: 1, font: { size: 12 } },
            grid: { color: 'rgba(0, 0, 0, 0.05)' },
          },
          x: {
            ticks: { font: { size: 12 } },
            grid: { display: false },
          },
        },
        animation: {
          onComplete: () => {
            ctxMain.canvas.classList.add('animate-pulse-glow');
            setTimeout(() => ctxMain.canvas.classList.remove('animate-pulse-glow'), 2500);
          },
        },
      }
    });

    // Recent Trend Chart (Line)
    trendChart = new Chart(ctxTrend, {
      type: 'line',
      data: {
        labels: data.dates,
        datasets: [{
          label: 'Detection Trend',
          data: data.counts,
          fill: {
            target: 'origin',
            above: 'rgba(5, 150, 105, 0.25)',
          },
          borderColor: 'rgba(5, 150, 105, 1)',
          tension: 0.5,
          pointRadius: 5,
          pointBackgroundColor: 'rgba(5, 150, 105, 1)',
          pointHoverRadius: 10,
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: 'rgba(5, 150, 105, 1)',
          pointHoverBorderWidth: 3,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(0, 0, 0, 0.85)',
            cornerRadius: 10,
            padding: 14,
            titleFont: { size: 14, weight: 'bold' },
            bodyFont: { size: 12 },
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: { font: { size: 12 } },
            grid: { color: 'rgba(0, 0, 0, 0.05)' },
          },
          x: {
            ticks: { font: { size: 12 } },
            grid: { display: false },
          },
        },
        animation: {
          onComplete: () => {
            ctxTrend.canvas.classList.add('animate-pulse-glow');
            setTimeout(() => ctxTrend.canvas.classList.remove('animate-pulse-glow'), 2500);
          },
        },
      }
    });
  });
});