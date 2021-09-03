function myTest(){
    // console.log('Hello Felipe from JS');
    Pass 
 }
//
//This JS function calls the analyzer using an ajax request passing two parameters
//
 function getRSS(rss_url, rss_desc) {
    var text = rss_url;
    var desc = rss_desc;
    document.getElementById("demo").style.backgroundColor = "red";
    document.getElementById("demo").innerHTML = "Feed analysis in progress, please wait...";
    // console.log(text);
    var response = "";
    $.ajax({
        type: "POST",
        url: 'my-ajax-test/',
        data: {addcsrfmiddlewaretoken: '{{ csrf_token }}', text: text, desc: desc, },  
        success: function callback(response){
                  // console.log('back in JS ');  
                  document.getElementById("demo").style.animationIterationCount = 0;
                  document.getElementById("demo").style.backgroundColor = "green";
                  document.getElementById("demo").style.color = "white";
                  document.getElementById("demo").innerHTML = "Feed analysis successfully completed!";  
    
                }
    });
    // console.log(response);
}
