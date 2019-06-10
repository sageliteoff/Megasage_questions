vendors_label = $("#vendors_label")
vendors = $("#vendors")
vodafone_token = $("#vodafone_token")

$(document).ready(function() {
  vendors.change(function(e) {
    css_classes = ["bg-mtn","bg-tigo","bg-vodafone","bg-airtel"]
    vendors_label.removeClass(css_classes)
    current_css_class = "bg-"+$(this).val()
    vendors_label.addClass(current_css_class)

    if ($(this).val() == "vodafone"){
      vodafone_token.css('display', 'block');
    }else{
        vodafone_token.css('display', 'none');
    }
  });

});
