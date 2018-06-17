$(function(){
    $('#inlineFormInputDate').daterangepicker({
     singleDatePicker: true,
     locale: {
        format: 'YYYY-MM-DD'
     }
    });
   });

$('#list-subcategory a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
  })