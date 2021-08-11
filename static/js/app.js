function myTest(){
    console.log('Hello Felipe from JS');
 }

 function getRSS(rss_url) {
    var text = rss_url;
    console.log(text);
    var response = ""
    $.ajax({
        type: "POST",
        url: 'my-ajax-test/',
        data: {addcsrfmiddlewaretoken: '{{ csrf_token }}', text: text, },  
        success: function callback(response){
                   console.log('back in JS ');
                  // console.log(response);
                  // alert(response);            
                }
    });
    console.log(response)
}
