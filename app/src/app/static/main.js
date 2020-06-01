$(document).ready(function(){
    var categorydes=[];
    var category=[]
    
    function loadCategoryDes(){
        $.getJSON('/api/v1/category/child', function(data, status, xhr){
            for (var i = 0; i < data.length; i++ ) {
                categorydes.push(data[i].name);
            }
    });
    };

    function loadCategory(){
        $.getJSON('/api/v1/category/parent', function(data, status, xhr){
            for (var i = 0; i < data.length; i++ ) {
                category.push(data[i].name);
            }
    });
    };

    $(function(){
        $('.inlineFormInputDate').datepicker({
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
        $('form[name=add-exp-form] #inlineFormInputAccount').change(function()
        {   
            var currency_id ="";
            $.getJSON('api/v1/accounts/'+this.value, function(data, status, xhr){
                $('form[name=add-exp-form] span.input-group-text').css('display', 'none');
                $('form[name=add-exp-form] span[data-id='+data.currency_id+']').css('display', 'block');
                $('form[name=add-exp-form] input[name=currency-id]').val(data.currency_id);
            });
        });
        $('form[name=add-exp-form] #inlineFormInputAccount option:first').attr('checked', 'checked').change();
    });

    $(function() {
        $('#ModalNewAccount input:radio[name=currency]').change(function()
            {
                if ($(this).is(':checked')) {
                    $('#ModalNewAccount input:text[name^=balance_]').prop("disabled", true);
                    $('#ModalNewAccount input:text[name=balance_'+$(this).attr('value')+']').prop("disabled", false);
                }
            });
        $('#ModalNewAccount input:radio[name=currency]:first').attr('checked', 'checked').change();
    });


    $(function() {
        $('#ModalEditAccount input:radio[name=currency]').change(function()
            {
                if ($(this).is(':checked')) {
                    $('#ModalEditAccount input:text[name^=balance_]').val('');
                    $('#ModalEditAccount input:text[name=balance_'+$(this).attr('value')+']').val($('#ModalEditAccount input[name=account-balance]').val());
                }
            });
    });


    $('#ModalEditAccount').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget)
        let accountId = button.data('account-id')
        let accountName = button.data('account-name')
        let accountType = button.data('account-type')
        let accountCurrency = button.data('account-currency')
        let accountBalance = button.data('account-balance')
        let modal = $(this)

        modal.find('.modal-body input[name=account-id]').val(accountId)
        modal.find('.modal-body input[name=account-balance]').val(accountBalance);
        modal.find('.modal-title').text('Изменить текущий счет: ' + accountName)
        modal.find('.modal-body input[name=name]').val(accountName)
        modal.find('.modal-body select[name=group]').val(accountType);
        modal.find('.modal-body input:text[name^=balance_]').val('');
        modal.find('.modal-body input:text[name=balance_'+accountCurrency+']').val(accountBalance);
        modal.find('.modal-body input:radio[name=currency]').attr('checked', false);
        $('#ModalEditAccount input:radio[name=currency][value='+accountCurrency+']').attr('checked', 'checked').change();
    })
});
