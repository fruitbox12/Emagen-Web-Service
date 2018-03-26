function showPassword() {
    
    var key_attr = $('#lpassword').attr('type');
    
    if(key_attr != 'text') {
        
        $('.checkbox').addClass('show');
        $('#lpassword').attr('type', 'text');
        
    } else {
        
        $('.checkbox').removeClass('show');
        $('#lpassword').attr('type', 'password');
        
    }
    
}
