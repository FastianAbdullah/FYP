// Total Orders Chart
const totalOrderOption = {
  series: [
    {
      name: "Order",
      data: [15, 20, 10, 25, 15, 25],
    },
  ],
  chart: {
    type: "bar",
    width: 70,
    height: 50,
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
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 2,
      columnWidth: 4,
      colors: {
        backgroundBarColors: ["#F9F6FF"],
        backgroundBarRadius: 2,
      },
    },
  },
  colors: ["#795DED"],
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
};
const totalOrderChart = new ApexCharts(
  document.querySelector("#total-order-chart"),
  totalOrderOption
);
totalOrderChart.render();

// New Orders Chart
const newOrderOption = {
  series: [
    {
      name: "Order",
      data: [15, 20, 10, 25, 15, 25],
    },
  ],
  chart: {
    type: "bar",
    width: 70,
    height: 50,
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
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 2,
      columnWidth: 4,
      colors: {
        backgroundBarColors: ["#ff462633"],
        backgroundBarRadius: 2,
      },
    },
  },
  colors: ["#FF4626"],
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
};
const newOrderChart = new ApexCharts(
  document.querySelector("#new-order-chart"),
  newOrderOption
);
newOrderChart.render();

// On Going Delivery Chart
const onDeliveryOption = {
  series: [
    {
      name: "On Delivery",
      data: [15, 20, 10, 25, 15, 25],
    },
  ],
  chart: {
    type: "bar",
    width: 70,
    height: 50,
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
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 2,
      columnWidth: 4,
      colors: {
        backgroundBarColors: ["#EAF2FF"],
        backgroundBarRadius: 2,
      },
    },
  },
  colors: ["#498CFF"],
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
};
const onDeliveryChart = new ApexCharts(
  document.querySelector("#on-going-delivery-chart"),
  onDeliveryOption
);
onDeliveryChart.render();

// Complete Delivery Chart
const completeDeliveryOption = {
  series: [
    {
      name: "On Delivery",
      data: [15, 20, 10, 25, 15, 25],
    },
  ],
  chart: {
    type: "bar",
    width: 70,
    height: 50,
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
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 2,
      columnWidth: 4,
      colors: {
        backgroundBarColors: ["#D2F0CD"],
        backgroundBarRadius: 2,
      },
    },
  },
  colors: ["#66CC33"],
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
};
const completeDeliveryChart = new ApexCharts(
  document.querySelector("#complete-delivery-chart"),
  completeDeliveryOption
);
completeDeliveryChart.render();

// Order Status Chart
const orderStatusOption = {
  series: [
    {
      name: "Orders",
      data: [30, 40, 35, 50, 25, 60, 45, 55, 70, 65, 45, 60],
    },
    {
      name: "Delivery",
      data: [50, 35, 45, 40, 60, 50, 35, 40, 65, 55, 70, 60],
    },
  ],
  chart: {
    type: "area",
    height: "275",
    offsetX: -10,
    offsetY: 20,
    toolbar: {
      show: false,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  dataLabels: {
    enabled: false,
  },
  grid: {
    borderColor: "#EEE",
    strokeDashArray: 5,
  },
  xaxis: {
    categories: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
  },
  yaxis: {
    min: 5,
    max: 90,
    tickAmount: 5,
    labels: {
      formatter: (val) => val + "k",
    },
  },
  stroke: {
    curve: "straight",
    colors: ["#795DED", "#498CFF"],
    width: 2,
  },
  markers: {
    colors: ["#795DED", "#498CFF"],
  },
  fill: {
    type: "gradient",
    colors: ["#795DED", "#498CFF"],
    gradient: {
      opacityFrom: 0.4,
      opacityTo: 0.15,
      stops: [0, 60],
    },
  },
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "18%",
      endingShape: "rounded",
    },
  },
  legend: {
    position: "top",
    horizontalAlign: "left",
    offsetX: -30,
    offsetY: 0,
    markers: {
      width: 20,
      height: 8,
      radius: 5,
      fillColors: ["#795DED", "#498CFF"],
      offsetX: -3,
      offsetY: -1,
    },
    itemMargin: {
      horizontal: 20,
    },
  },
  tooltip: {
    followCursor: true,
    marker: {
      show: false,
    },
    y: {
      formatter: (val) => {
        return val + "k";
      },
    },
  },
};

const orderStatusChart = new ApexCharts(
  document.querySelector("#order-status-chart"),
  orderStatusOption
);
orderStatusChart.render();

// Delivery By Truck Chart
const deliveryByTruckOptions = {
  chart: {
    type: "bar",
    height: 250,
    width: "100%",
    offsetX: -5,
    offsetY: 15,
    toolbar: {
      show: false,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  xaxis: {
    categories: ["Vehicle", "Textile", "Argo", "Energy", "Metals", "Wood"],
  },
  yaxis: {
    show: false,
  },
  series: [
    {
      name: "Achive",
      data: [80, 55, 75, 40, 45, 80],
    },
  ],
  grid: {
    borderColor: "#EEE",
  },
  dataLabels: {
    enabled: false,
  },
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 15,
      columnWidth: 35,
    },
  },
  colors: ["#795DED"],
  legend: {
    show: false,
  },
  tooltip: {
    y: {
      formatter: (val) => {
        return val + "%";
      },
    },
  },
  responsive: [
    {
      breakpoint: 640,
      options: {
        plotOptions: {
          bar: {
            borderRadius: 10,
            columnWidth: 20,
          },
        },
      },
    },
  ],
};

const deliveryByTruck = new ApexCharts(
  document.querySelector("#delivery-by-truck-chart"),
  deliveryByTruckOptions
);
deliveryByTruck.render();

// Delivery By Ship Chart
const deliveryByShipOptions = {
  chart: {
    type: "bar",
    height: 250,
    width: "100%",
    offsetX: -5,
    offsetY: 15,
    toolbar: {
      show: false,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  xaxis: {
    categories: ["Vehicle", "Textile", "Argo", "Energy", "Metals", "Wood"],
  },
  yaxis: {
    show: false,
  },
  series: [
    {
      name: "Achive",
      data: [85, 50, 70, 45, 50, 85],
    },
  ],
  grid: {
    borderColor: "#EEE",
  },
  dataLabels: {
    enabled: false,
  },
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 15,
      columnWidth: 35,
    },
  },
  colors: ["#795DED"],
  legend: {
    show: false,
  },
  tooltip: {
    y: {
      formatter: (val) => {
        return val + "%";
      },
    },
  },
};

const deliveryByShip = new ApexCharts(
  document.querySelector("#delivery-by-ship-chart"),
  deliveryByShipOptions
);
deliveryByShip.render();

// Delivery By Fly Chart
const deliveryByFlyOptions = {
  chart: {
    type: "bar",
    height: 250,
    width: "100%",
    offsetX: -5,
    offsetY: 15,
    toolbar: {
      show: false,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  xaxis: {
    categories: ["Vehicle", "Textile", "Argo", "Energy", "Metals", "Wood"],
  },
  yaxis: {
    show: false,
  },
  series: [
    {
      name: "Achive",
      data: [78, 60, 73, 42, 47, 78],
    },
  ],
  grid: {
    borderColor: "#EEE",
  },
  dataLabels: {
    enabled: false,
  },
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 15,
      columnWidth: 35,
    },
  },
  colors: ["#795DED"],
  legend: {
    show: false,
  },
  tooltip: {
    y: {
      formatter: (val) => {
        return val + "%";
      },
    },
  },
};

const deliveryByFly = new ApexCharts(
  document.querySelector("#delivery-by-fly-chart"),
  deliveryByFlyOptions
);
deliveryByFly.render();

// Delivery By Train Chart
const deliveryByTrainOptions = {
  chart: {
    type: "bar",
    height: 250,
    width: "100%",
    offsetX: -5,
    offsetY: 15,
    toolbar: {
      show: false,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  xaxis: {
    categories: ["Vehicle", "Textile", "Argo", "Energy", "Metals", "Wood"],
  },
  yaxis: {
    show: false,
  },
  series: [
    {
      name: "Achive",
      data: [82, 53, 77, 43, 48, 82],
    },
  ],
  grid: {
    borderColor: "#EEE",
  },
  dataLabels: {
    enabled: false,
  },
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 15,
      columnWidth: 35,
    },
  },
  colors: ["#795DED"],
  legend: {
    show: false,
  },
  tooltip: {
    y: {
      formatter: (val) => {
        return val + "%";
      },
    },
  },
};

const deliveryByTrain = new ApexCharts(
  document.querySelector("#delivery-by-train-chart"),
  deliveryByTrainOptions
);
deliveryByTrain.render();

// Delivery Analysis
const deliveryAnalysisOption = {
  series: [1000, 1754, 1234, 500],
  labels: ["Processing", "On Delivery", "Complete", "Delayed"],
  chart: {
    height: 250,
    type: "donut",
  },
  dataLabels: {
    enabled: false,
  },
  legend: {
    show: false,
  },
  stroke: {
    show: false,
  },
  plotOptions: {
    pie: {
      donut: {
        size: "40%",
        background: "transparent",
        labels: {
          show: true,
          name: {
            show: false,
          },
          value: {
            show: false,
          },
          total: {
            show: false,
          },
        },
      },
    },
  },
  colors: ["#498CFF", "#795DED", "#66CC33", "#FF4626"],
};
const deliveryAnalysisChart = new ApexCharts(
  document.querySelector("#delivery-analysis-chart"),
  deliveryAnalysisOption
);
deliveryAnalysisChart.render();

// Sales Analysis Chart
const salesAnalysisOptions = {
  chart: {
    type: "area",
    height: 250,
    width: "100%",
    offsetX: -5,
    offsetY: 15,
    toolbar: {
      show: false,
    },
    events: {
      mounted: (chart) => {
        chart.windowResizeHandler();
      },
    },
  },
  stroke: {
    curve: "stepline",
    lineCap: "round",
    width: 2,
  },
  xaxis: {
    categories: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
  },
  yaxis: {
    show: false,
  },
  series: [
    {
      name: "Total",
      data: [10, 20, 15, 25, 10, 30, 20, 35, 25, 20, 15, 30],
    },
  ],
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "18%",
      endingShape: "rounded",
    },
  },
  grid: {
    borderColor: "#EEE",
  },
  fill: {
    type: "gradient",
    colors: ["#795DED", "#498CFF"],
    gradient: {
      opacityFrom: 0.5,
      opacityTo: 0.3,
      stops: [0, 70],
    },
  },
  dataLabels: {
    enabled: false,
  },
  plotOptions: {
    bar: {
      horizontal: false,
      borderRadius: 15,
      columnWidth: 35,
    },
  },
  colors: ["#795DED"],
  legend: {
    show: false,
  },
  tooltip: {
    y: {
      formatter: (val) => {
        return val + "$";
      },
    },
  },
};
const salesAnalysisChart = new ApexCharts(
  document.querySelector("#sales-analysis-chart"),
  salesAnalysisOptions
);
salesAnalysisChart.render();
