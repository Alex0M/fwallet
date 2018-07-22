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
});
