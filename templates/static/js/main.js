$(document).ready(function () {
    $(".banner-carousel").owlCarousel({
      items: 1,
      loop: true,
      autoplay: true,
      autoplayTimeout: 7000, // 7 seconds
      nav: false,
      dots: false,
      slideSpeed: 1000,
      paginationSpeed: 1000,
      smartSpeed: 1000,
      autoplayHoverPause: false
    });
  });