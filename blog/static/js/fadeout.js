window.addEventListener("DOMContentLoaded", () => {
  let messages = document.querySelector(".messages");

  if (messages) {
    messages.classList.add("fadeout");
    let promise = new Promise(function(resolve) {
      setTimeout(() => {
        messages.style.display = "none";
        resolve();
      }, 3000);
    });
    
    promise.then(res => {
      messages.remove();
    });
  }
});

let intervalId = setInterval(function() {
  let messages = $(".messages")[0];
  if (messages) {
    messages.classList.add("fadeout");
    let promise = new Promise(function(resolve) {
      setTimeout(() => {
        messages.style.display = "none";
        resolve();
      }, 3000);
    });
    
    promise.then(res => {
      messages.remove();
    });
  }
}, 1000);