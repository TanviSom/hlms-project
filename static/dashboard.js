

var sidebarOpen = false;
var sidebar = document.getElementById("sidebar");

function openSidebar() {
    if(!sidebarOpen) {
        sidebar.classList.add("sidebar-responsive");
        sidebarOpen = true 
    }
}

function closeSidebar() {
    if(sidebarOpen) {
        sidebar.classList.remove("sidebar-responsive");
        sidebarOpen= false;
    }
}

var lineChartOptions = {
  series: [{
      data: [400, 430, 448, 470, 540, 580, 690, 1100, 1200, 1380]
  }],
  chart: {
      type: 'line',  // Change type from 'bar' to 'line'
      height: 350,
      toolbar: {
          show: false
      },
  },
  colors: [
      "#246dec",
  ],
  stroke: {
      curve: 'smooth',  // Makes the line smooth; remove if you want sharp edges
      width: 2
  },
  markers: {
      size: 5, // Adjust marker size
      colors: ['#246dec'],  // Change marker colors
  },
  dataLabels: {
      enabled: false  // Disable data labels
  },
  legend: {
      show: false
  },
  xaxis: {
      categories: ['South Korea', 'Canada', 'United Kingdom', 'Netherlands', 'Italy', 'France', 'Japan',
          'United States', 'China', 'Germany'
      ],
  },
  yaxis: {
      title: {
          text: "Count"
      }
  }
};

var lineChart = new ApexCharts(document.querySelector("#bar-chart"), lineChartOptions);
lineChart.render();

  const date = new Date();

const renderCalendar = () => {
  date.setDate(1);

  const monthDays = document.querySelector(".days");

  const lastDay = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDate();

  const prevLastDay = new Date(
    date.getFullYear(),
    date.getMonth(),
    0
  ).getDate();

  const firstDayIndex = date.getDay();

  const lastDayIndex = new Date(
    date.getFullYear(),
    date.getMonth() + 1,
    0
  ).getDay();

  const nextDays = 7 - lastDayIndex - 1;

  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];

  document.querySelector(".date h1").innerHTML = months[date.getMonth()];

  document.querySelector(".date p").innerHTML = new Date().toDateString();

  let days = "";

  for (let x = firstDayIndex; x > 0; x--) {
    days += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
  }

  for (let i = 1; i <= lastDay; i++) {
    if (
      i === new Date().getDate() &&
      date.getMonth() === new Date().getMonth()
    ) {
      days += `<div class="today">${i}</div>`;
    } else {
      days += `<div>${i}</div>`;
    }
  }

  for (let j = 1; j <= nextDays; j++) {
    days += `<div class="next-date">${j}</div>`;
    monthDays.innerHTML = days;
  }
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