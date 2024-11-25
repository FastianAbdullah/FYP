// Total Delivery Revenue Chart
const totalLogisticDeliveryRevenueOption = {
  series: [
    {
      name: "Revenue",
      data: [5, 30, 10, 25, 11, 30, 15, 28, 33],
    },
  ],
  chart: {
    type: "area",
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
  colors: ["#795DED"],
  stroke: {
    width: 1.2,
    curve: "smooth",
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
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.5,
      opacityTo: 0.2,
      stops: [0, 60],
    },
  },
};
const totalLogisticDeliveryRevenueChart = new ApexCharts(
  document.querySelector("#total-logistic-delivery-revenue-chart"),
  totalLogisticDeliveryRevenueOption
);
totalLogisticDeliveryRevenueChart.render();

// Total Delivery Cost Chart
const totalLogisticDeliveryCostOption = {
  series: [
    {
      name: "Cost",
      data: [33, 28, 15, 30, 11, 25, 10, 30, 5],
    },
  ],
  chart: {
    type: "area",
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
  colors: ["#FF4626"],
  stroke: {
    width: 1.2,
    curve: "smooth",
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
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.5,
      opacityTo: 0.2,
      stops: [0, 60],
    },
  },
};
const totalLogisticDeliveryCostChart = new ApexCharts(
  document.querySelector("#total-logistic-delivery-cost-chart"),
  totalLogisticDeliveryCostOption
);
totalLogisticDeliveryCostChart.render();

// Total Delivery Shipment Chart
const totalLogisticDeliveryShipmentOption = {
  series: [
    {
      name: "Shipment",
      data: [33, 28, 15, 30, 11, 25, 10, 30, 5],
    },
  ],
  chart: {
    type: "area",
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
  colors: ["#795DED"],
  stroke: {
    width: 1.2,
    curve: "smooth",
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
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.5,
      opacityTo: 0.2,
      stops: [0, 60],
    },
  },
};
const totalLogisticDeliveryShipmentChart = new ApexCharts(
  document.querySelector("#total-logistic-delivery-shipment-chart"),
  totalLogisticDeliveryShipmentOption
);
totalLogisticDeliveryShipmentChart.render();

// Delivery Overview
const logisticDeliveryOverviewOption = {
  series: [1754, 1234, 878],
  labels: ["Order Done", "Revenue", "Total Cost"],
  chart: {
    height: 300,
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
        size: "50%",
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
  colors: ["#763FF9", "#66CC33", "#FF4626"],
};
const logisticDeliveryOverviewChart = new ApexCharts(
  document.querySelector("#logistic-delivery-overview-chart"),
  logisticDeliveryOverviewOption
);
logisticDeliveryOverviewChart.render();

// Total Shipment Chart
const totalLogisticShipmentOption = {
  series: [
    {
      name: "Shipment",
      data: [50, 20, 22, 50, 25, 20, 39, 45, 85, 75, 40, 60],
    },
    {
      name: "Delivery",
      data: [65, 50, 39, 75, 45, 58, 56, 55, 80, 30, 75, 45],
    },
  ],
  chart: {
    type: "bar",
    height: "360",
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
  plotOptions: {
    bar: {
      horizontal: false,
      columnWidth: "40%",
      borderRadius: 5,
      borderRadiusApplication: "end",
    },
  },
  dataLabels: {
    enabled: false,
  },
  grid: {
    borderColor: "#EEE",
    strokeDashArray: 5,
  },
  stroke: {
    show: false,
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
  fill: {
    colors: ["#76D466", "#795DED"],
    opacity: 1,
  },
  legend: {
    position: "top",
    horizontalAlign: "left",
    offsetX: -30,
    offsetY: 0,
    markers: {
      width: 20,
      height: 8,
      radius: 0,
      fillColors: ["#76D466", "#795DED"],
      offsetX: -3,
      offsetY: -1,
    },
    itemMargin: {
      horizontal: 20,
    },
  },
  tooltip: {
    y: {
      formatter: (val) => {
        return val + "k";
      },
    },
  },
};

const totalLogisticShipmentChart = new ApexCharts(
  document.querySelector("#total-logistic-shipment-chart"),
  totalLogisticShipmentOption
);
totalLogisticShipmentChart.render();

// Delivery By Country
const markers = [
  {
    name: "Russia",
    coords: [55.75, 37.61],
  },
  {
    name: "Canada",
    coords: [56.1304, -106.3468],
  },
  {
    name: "Singapore",
    coords: [1.3, 103.8],
  },
];
new jsVectorMap({
  selector: "#logistic-delivery-by-country-chart",
  map: "world_merc",
  markersSelectable: true,
  // zoomOnScroll: false,
  zoomButtons: false,
  labels: {
    markers: {
      render: function (marker) {
        return marker.name;
      },
    },
  },
  markers: markers,
  markerStyle: {
    initial: {
      image: "assets/images/icons/location.svg",
    },
  },
  regionStyle: {
    initial: {
      fill: "#F4ECFF",
      stroke: "#B39EF9",
      strokeWidth: 1,
      fillOpacity: 1,
    },
  },
  onMarkerSelected(index, isSelected, selectedMarkers) {
    console.log(index, isSelected, selectedMarkers);
  },
});

// Delivery By Truck Chart
const logisticDeliveryByTruckOptions = {
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
  xaxis: {
    categories: ["Vehicle", "Textile", "Argo", "Energy", "Metals"],
  },
  yaxis: {
    min: 10,
    max: 90,
    tickAmount: 4,
    labels: {
      formatter: (val) => val + "k",
    },
  },
  series: [
    {
      name: "Achive",
      data: [30, 75, 55, 76, 40],
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
  dataLabels: {
    enabled: false,
  },
  stroke: {
    colors: ["#795DED"],
    width: 2,
  },
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.4,
      opacityTo: 0.15,
      stops: [0, 60],
    },
  },
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

const logisticDeliveryByTruck = new ApexCharts(
  document.querySelector("#logistic-delivery-by-truck-chart"),
  logisticDeliveryByTruckOptions
);
logisticDeliveryByTruck.render();

// Delivery By Ship Chart
const logisticDeliveryByShipOptions = {
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
  xaxis: {
    categories: ["Vehicle", "Textile", "Argo", "Energy", "Metals"],
  },
  yaxis: {
    min: 10,
    max: 90,
    tickAmount: 4,
    labels: {
      formatter: (val) => val + "k",
    },
  },
  series: [
    {
      name: "Achive",
      data: [10, 20, 30, 40, 50],
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
  dataLabels: {
    enabled: false,
  },
  stroke: {
    colors: ["#795DED"],
    width: 2,
  },
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.4,
      opacityTo: 0.15,
      stops: [0, 60],
    },
  },
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

const logisticDeliveryByShip = new ApexCharts(
  document.querySelector("#logistic-delivery-by-ship-chart"),
  logisticDeliveryByShipOptions
);
logisticDeliveryByShip.render();

// Delivery By Ship Chart
const logisticDeliveryByFlyOptions = {
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
  xaxis: {
    categories: ["Vehicle", "Textile", "Argo", "Energy", "Metals"],
  },
  yaxis: {
    min: 10,
    max: 90,
    tickAmount: 4,
    labels: {
      formatter: (val) => val + "k",
    },
  },
  series: [
    {
      name: "Achive",
      data: [90, 80, 70, 60, 50],
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
  dataLabels: {
    enabled: false,
  },
  stroke: {
    colors: ["#795DED"],
    width: 2,
  },
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.4,
      opacityTo: 0.15,
      stops: [0, 60],
    },
  },
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

const logisticDeliveryByFly = new ApexCharts(
  document.querySelector("#logistic-delivery-by-fly-chart"),
  logisticDeliveryByFlyOptions
);
logisticDeliveryByFly.render();

// Delivery By Train Chart
const logisticDeliveryByTrainOptions = {
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
  xaxis: {
    categories: ["Vehicle", "Textile", "Argo", "Energy", "Metals"],
  },
  yaxis: {
    min: 10,
    max: 90,
    tickAmount: 4,
    labels: {
      formatter: (val) => val + "k",
    },
  },
  series: [
    {
      name: "Achive",
      data: [20, 40, 100, 40, 20],
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
  dataLabels: {
    enabled: false,
  },
  stroke: {
    colors: ["#795DED"],
    width: 2,
  },
  fill: {
    type: "gradient",
    gradient: {
      opacityFrom: 0.4,
      opacityTo: 0.15,
      stops: [0, 60],
    },
  },
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

const logisticDeliveryByTrain = new ApexCharts(
  document.querySelector("#logistic-delivery-by-train-chart"),
  logisticDeliveryByTrainOptions
);
logisticDeliveryByTrain.render();
