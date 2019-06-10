
var nav =$("#nav");
var overlay = $("#overlay")
var body = $("body")

//if btn_open_nav is clicked, show the navbar and the overlay container
$("#btn_open_nav").click(function(e) {
  nav.slideDown(500,"swing",function(){});

  overlay.slideDown();
  overlay.css(
    {"min-width": body.width(),
      "min-height": Math.max(body.height(),window.innerHeight),
      "background-color":"rgb(0,0,0)",
      "opacity": "0.6"
  })

})

//if btn_close_nav is clicked, hide the navbar and the overlay container
$("#btn_close_nav").click(function(e) {
  nav.slideUp();
  overlay.fadeOut(800);
})

//if overlay container is clicked, call btn_close_nav
overlay.click(function(e) {
  $("#btn_close_nav").click();
})
