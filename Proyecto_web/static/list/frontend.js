$('.button-collapse').sideNav({
      menuWidth: 250, // Default is 300
     // Choose the horizontal origin
      closeOnClick: true, // Closes side-nav on <a> clicks, useful for Angular/Meteor
      draggable: true, // Choose whether you can drag to open on touch screens
    }
  );

 $(document).ready(function(){
      $('.carousel').carousel({
      	duration: 150,
      });
    });

