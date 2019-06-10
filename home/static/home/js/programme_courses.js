/*PROGRAMME DETAILS SCRIPTS*/
//Author: Sage Lite off

//by default,hide every row the follows ".programmedetails" on this page
$("#programme_courses .row").hide()

//toggle(show,hide) .row then user clicks on the button(.toggler)
$(".toggler").click(function(e) {

  if ($(this).next(".row").css("display") == "none") {
    $(this).next(".row").slideDown();
    $(this).children(0).removeClass("fa-angle-down");
    $(this).children(0).addClass("fa-angle-up");

  }else{
      $(this).next(".row").slideUp();
      this.children[0].classList.remove("fa-angle-up");
      this.children[0].classList.add("fa-angle-down");
  }
})
