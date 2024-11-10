{{-- <!DOCTYPE html> --}}
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Modern AI Landing HTML Template">
  <meta name="keywords" content="bootstrap 5, saas, landing page">
  <meta name="author" content="Themetags">
  <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.3/gsap.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.3/ScrollTrigger.min.js"></script> -->
  <title>Social Mind - Modern AI Landing HTML Template</title>

  <!-- Update the paths for stylesheets -->
  <link rel="stylesheet" href="/css/fonts/ff-1.css">
  <link rel="stylesheet" href="/css/fonts/ff-3.css">
  <link rel="stylesheet" href="/css/fonts/bootstrap-icons.css">
  <link rel="icon" href="/img/favicon.png" type="image/png">
  <link rel="stylesheet" href="/css/plugins.min.css">
  <link rel="stylesheet" href="/css/style.min.css">
  <meta name="csrf-token" content="{{ csrf_token() }}">

  @vite(['resources/js/app.js'])
</head>
<body class="bg-black body-clip">
  <div id="app"></div>
  @vite(['resources/js/legacy/plugins.js','resources/js/legacy/app.js','resources/js/legacy/animatedt-title.js'])
</body>
</html>
