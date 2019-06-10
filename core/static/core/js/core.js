
$(this).ready(function () {
//Get all the variables on the page
var notification = $("#notification");


hideNotification  = function () {
  notification.addClass("bounceOut")
  setTimeout(function () {
    notification.removeClass("bounceOut")
    notification.css({"display":"none"})
  }, 700);
}

//Handle Events
$("#hide_notification_btn").click(function(e) {
  hideNotification();
  })

})
