$(document).ready(function(){
$(".content-markdown").each(function(){
  var content=$(this).text()
  var markedContent=marked(content)
  $(this).html(markedContent)
})
$(".post-content img").each(function(){
$(this).addClass("img-fluid")
})
//preview title
var inputTitle=$("#id_title");
function setTitle(value){
  $("#preview-title").text(value);
}
setTitle(inputTitle.val());
inputTitle.keyup(function(){
  setTitle($(this).val())
})
console.log(inputTitle.val(),$("#preview-title").val())
//preview content
var inputContent=$("#id_content");

function setContent(value){
$("#preview-content").html(marked(value));
$("preview-content img").each(function(){
 $(this).addClass("img-fluid");
})
}
setContent(inputContent.val());
inputContent.keyup(function(){
setContent($(this).val())
})

})

document.querySelector('.reply-btn').addEventListener('click',function(event){
  event.preventDefault();
  document.querySelector('.comment-reply').style='display:block;';
},false);
