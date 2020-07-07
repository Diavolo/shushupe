$(document).ready(function(){
  // Dropdown
  $('.ui.dropdown')
    .dropdown()
  ;

  $('.ui.dropdown.social')
    .dropdown({
      on: 'hover'
    })
  ;

  // toogle
  // https://ehkoo.github.io/semantic-ui-examples/navbar/
  /*$('.right.menu.open').on("click",function(e){
    e.preventDefault();
    $('.ui.vertical.menu').toggle();
  });*/

  // Popup
  $('.browse.item')
    .popup({
      inline     : true,
      hoverable  : true,
      position   : 'bottom left',
      // lastResort: 'bottom left',
      delay: {
        show: 300,
        hide: 800
      }
    })
  ;

  $('.browse.item.project')
    .popup({
      inline     : true,
      hoverable  : true,
      position   : 'bottom left',
      lastResort: 'bottom left',
      delay: {
        show: 300,
        hide: 800
      }
    })
  ;
 
  // https://jsfiddle.net/ynaLoe4z/3/
  /*$('.teal.button')
  .popup({
    on: 'click'
  });
  $('input')
  .popup({
    on: 'focus'
  });*/

});
