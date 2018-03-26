
document.addEventListener('DOMContentLoaded', function () {
  particleground(document.getElementById('particles'), {
    dotColor: '#d9d9d9',
    lineColor: '#eee'
  });
  var intro = document.getElementById('intro');
  intro.style.marginTop = '-200px';
}, false);

/*
// jQuery plugin example:
$(document).ready(function() {
  $('#particles').particleground({
    dotColor: '#5cbdaa',
    lineColor: '#5cbdaa'
  });
  $('.intro').css({
    'margin-top': -($('.intro').height() / 2)
  });
});
*/
$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();   
});
