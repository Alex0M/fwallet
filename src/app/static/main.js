$(document).ready(function(){
    var countries=[];
    
    function loadCategoryDes(){
        $.getJSON('/catdesdic', function(data, status, xhr){
            for (var i = 0; i < data.length; i++ ) {
                countries.push(data[i].name);
            }
    });
    };

    $(function(){
        $('#inlineFormInputDate').datepicker({
            dateFormat: "dd-mm-yy"
        });
    });
    
    loadCategoryDes();
    
    $('#categorydes').autocomplete({
        source: countries, 
        });
});
