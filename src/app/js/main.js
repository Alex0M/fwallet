$(function(){
    $('#inlineFormInputDate').daterangepicker({
     singleDatePicker: true,
     locale: {
        format: 'YYYY-MM-DD'
     }
    });
   });

$('#myList a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
  })