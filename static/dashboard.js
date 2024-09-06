
// Sidebar toggle functionality
var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
    if (!sidebarOpen) {
        sidebar.classList.add("sidebar-responsive");
        sidebarOpen = true;
    }
}

function closeSidebar() {
    if (sidebarOpen) {
        sidebar.classList.remove("sidebar-responsive");
        sidebarOpen = false;
    }
}

// Calendar Functionality
const date = new Date();

const renderCalendar = () => {
    date.setDate(1);
    const monthDays = document.querySelector(".days");

    const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDate();
    const prevLastDay = new Date(date.getFullYear(), date.getMonth(), 0).getDate();
    const firstDayIndex = date.getDay();
    const lastDayIndex = new Date(date.getFullYear(), date.getMonth() + 1, 0).getDay();
    const nextDays = 7 - lastDayIndex - 1;

    const months = [
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"
    ];

    document.querySelector(".date h1").innerHTML = months[date.getMonth()];
    document.querySelector(".date p").innerHTML = new Date().toDateString();

    let days = "";

    // Previous Month's Days
    for (let x = firstDayIndex; x > 0; x--) {
        days += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
    }

    // Current Month's Days
    for (let i = 1; i <= lastDay; i++) {
        if (i === new Date().getDate() && date.getMonth() === new Date().getMonth()) {
            days += `<div class="today">${i}</div>`;
        } else {
            days += `<div>${i}</div>`;
        }
    }

    // Next Month's Days
    for (let j = 1; j <= nextDays; j++) {
        days += `<div class="next-date">${j}</div>`;
    }

    monthDays.innerHTML = days;
};

document.querySelector(".prev").addEventListener("click", () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
});

document.querySelector(".next").addEventListener("click", () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
});

renderCalendar();

// Months and Years toggle logic
document.getElementById('months').addEventListener('change', function () {
    if (this.checked) {
        document.getElementById('years').checked = false;
    }
});

document.getElementById('years').addEventListener('change', function () {
    if (this.checked) {
        document.getElementById('months').checked = false;
    }
});

// Chart Functionality (Line Chart with Balance, Cumulative Interest, Principal Paid)
var lineChartOptions = {
    series: [
        {
            name: 'Balance',
            data: [180000, 160000, 140000, 120000, 100000, 80000, 60000, 40000, 20000, 0]
        },
        {
            name: 'Cumulative Interest',
            data: [0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000]
        },
        {
            name: 'Principal Paid',
            data: [0, 20000, 40000, 60000, 80000, 100000, 120000, 140000, 160000, 180000]
        }
    ],
    chart: {
        type: 'line',
        height: 350,
        toolbar: { show: false }
    },
    colors: ['#246dec', '#f44336', '#4caf50'],
    stroke: { curve: 'smooth', width: 2 },
    markers: { size: 5, colors: ['#246dec', '#f44336', '#4caf50'] },
    dataLabels: { enabled: false },
    legend: { show: true, position: 'top' },
    xaxis: {
        categories: ['0', '20', '40', '60', '80', '100', '120', '140', '160', '180'],
        title: { text: 'Period (Payment Number)' }
    },
    yaxis: { title: { text: 'Amount ($)' } }
};

var lineChart = new ApexCharts(document.querySelector("#bar-chart"), lineChartOptions);
lineChart.render();

// Loan Form Submission and Dynamic Chart Update
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loanForm');
    const chartContainer = document.getElementById('chart');

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        const formData = new FormData(form);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        // Send form data to backend
        const response = await fetch('/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        const result = await response.json(); // Get the data back from the server
        updateChart(result);
    });

    // Function to update the chart with backend data
    function updateChart(data) {
        const chartOptions = {
            chart: { type: 'line', height: 350 },
            series: [
                { name: 'EMI', data: data.emis },
                { name: 'Balance', data: data.balance },
                { name: 'Cumulative Interest', data: data.cumulative_interest }
            ],
            xaxis: { categories: data.months },
            title: { text: 'Loan Payment Breakdown Over Time' },
            stroke: { curve: 'smooth' },
            colors: ['#246dec', '#f44336', '#4caf50']
        };

        // Destroy old chart
        if (window.chart) {
            window.chart.destroy();
        }

        // Render the new chart
        window.chart = new ApexCharts(chartContainer, chartOptions);
        window.chart.render();
    }
});