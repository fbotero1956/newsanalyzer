function myTest(){
    console.log('Hello Felipe from JS');
 }

 function getRSS(rss_url, rss_desc) {
    var text = rss_url;
    var desc = rss_desc;
    document.getElementById("demo").innerHTML = "Feed analysis in progress, please wait...";
    console.log(text);
    var response = "";
    $.ajax({
        type: "POST",
        url: 'my-ajax-test/',
        data: {addcsrfmiddlewaretoken: '{{ csrf_token }}', text: text, desc: desc, },  
        success: function callback(response){
                  console.log('back in JS ');  
                  document.getElementById("demo").innerHTML = "Feed analysis successfully completed!";  
    
                }
    });
    console.log(response);
}
