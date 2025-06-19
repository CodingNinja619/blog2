let displayed = false;
$("#profile-image").on("click", function() {
  if (!displayed) {
    $(".dropdown-menu").css({
      "display": "-webkit-box",
      "display": "-ms-flexbox",
      "display": "flex",
      "-webkit-box-orient": "vertical",
      "-webkit-box-direction": "normal",
      "-ms-flex-direction": "column",
    "flex-direction": "column",
    });
  }
  else {
    $(".dropdown-menu").css({
      "display": "none"
    });
  }
  displayed = !displayed;
})