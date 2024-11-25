// Total Balance
const totalBalanceOptions = {
  series: [
    {
      name: "Balance",
      data: [33, 28, 15, 11, 25, 10, 30, 5],
    },
  ],
  chart: {
    type: "area",
    height: 80,
    sparkline: {
      enabled: true,
    },
    zoom: {
      autoScaleYaxis: true,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  colors: ["#FF4626"],
  stroke: {
    width: 1.2,
    curve: "smooth",
  },
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.5,
      opacityTo: 0.2,
      stops: [0, 60],
    },
  },
  tooltip: {
    enabled: true,
    x: {
      show: false,
    },
    y: {
      title: {
        formatter: function (seriesName) {
          return "";
        },
      },
    },
    marker: {
      show: false,
    },
  },
  responsive: [
    {
      breakpoint: 1440,
      options: {
        chart: {
          height: 45,
        },
      },
    },
  ],
};
const totalBalanceChart = new ApexCharts(
  document.querySelector("#totalBalance"),
  totalBalanceOptions
);
totalBalanceChart.render();

// Total Earning Chart Small
const totalEarningOptions = {
  series: [
    {
      name: "Earning",
      data: [33, 28, 15, 11, 25, 10, 30, 5],
    },
  ],
  chart: {
    type: "area",
    height: 80,
    sparkline: {
      enabled: true,
    },
    zoom: {
      autoScaleYaxis: true,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  colors: ["#76D466"],
  stroke: {
    width: 1.2,
    curve: "smooth",
  },
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.5,
      opacityTo: 0.2,
      stops: [0, 60],
    },
  },
  tooltip: {
    enabled: true,
    x: {
      show: false,
    },
    y: {
      title: {
        formatter: function (seriesName) {
          return "";
        },
      },
    },
    marker: {
      show: false,
    },
  },
  responsive: [
    {
      breakpoint: 1440,
      options: {
        chart: {
          height: 45,
        },
      },
    },
  ],
};
const totalEarningChart = new ApexCharts(
  document.querySelector("#totalEarning"),
  totalEarningOptions
);
totalEarningChart.render();
