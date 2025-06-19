$(function() {
  $("#read-later-button").click(function (e) {
    
    let post_id = $(this).data("post-id"); 
    if (!post_id) {
      let parents = $(this).parents();
      for (let parent of parents) {
        if (parent.data("post-id")) {
          post_id = $(this).data("post-id");
          break;
        }
      }
    }
   
    $.ajax({
      type: "POST",
      url: "add-in-read-later/",
      data: {"post_id": post_id},
      dataType: "json",
      success: function (response) {
        console.log(response);
        if (!$(".messages").length) {
          $("#content").prepend(`
              <ul class="messages">

              </ul>
            `);
        }
        $(".messages").append(`<li class="success">Post ${response.post_title} was added to read later</li>`);
      }
    })
  }) 
});
