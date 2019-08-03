$(document).ready(function(){
    var categorydes=[];
    var category=[]
    
    function loadCategoryDes(){
        $.getJSON('/api/v1.0/category/child', function(data, status, xhr){
            for (var i = 0; i < data.length; i++ ) {
                categorydes.push(data[i].name);
            }
    });
    };

    function loadCategory(){
        $.getJSON('/api/v1.0/category/parent', function(data, status, xhr){
            for (var i = 0; i < data.length; i++ ) {
                category.push(data[i].name);
            }
    });
    };

    $(function(){
        $('#inlineFormInputDate').datepicker({
            dateFormat: "yy-mm-dd"
        });
    });
    
    loadCategoryDes();
    loadCategory()
    
    $('#categorydes').autocomplete({
        source: categorydes, 
        });

    $('#category').autocomplete({
        source: category, 
        });
    
    $(function() {
        $('input:radio[name=currency]').change(function()
            {
                if ($(this).is(':checked')) {
                    $('input:text[name^=balance_]').prop("disabled", true);
                    $('input:text[name=balance_'+$(this).attr('value')+']').prop("disabled", false);
                }
            });
        $('input:radio[name=currency]:first').attr('checked', 'checked').change();
    });
});
