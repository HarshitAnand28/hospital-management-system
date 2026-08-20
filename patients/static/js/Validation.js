let flag=false
    $('.lostfocus').on('focusout', function(){
        v=$(this).val();
        if(v.length==0)
        {
            flag=true
            $(this).val("This field is mandatory*");
            $(this).css({"border":"2px solid red", "color":"red"});
        }
    });
    $('.photo').on('focusout', function () {

    if (this.files.length === 0) {

        flag = true;

        $(this).css({
            "border": "2px solid red"
        });

        $(this).next('.s').text("This field is mandatory*");

    } else {

        flag = false;

        $(this).css({
            "border": ""
        });

        $(this).next('.s').text("");
    }
});
    // $('.photo').on('focusout', function(){
    //     v=$(this).val();
    //     if(v.length==0)
    //     {
    //         flag=true
    //         $(this).val("This field is mandatory*");
    //         $(this).css({"border":"2px solid red", "color":"red"});
    //     }
    // });
    // function lostfocus(a)
    // {
    //     if($(a).val().length==0)
    //     {
    //         $(a).val("This field is mandatory*");
    //         $(a).css({"border":"2px solid red", "color":"red"});
    //     }
    // }
    
    
    function gainedfocus(a)
    {
        v=$(a).val();
        if(v=="This field is mandatory*")
        {
            flag=false
            $(a).val("");
            $(a).css({"border":"", "color":""});
        }
    }
    $('.onlydigits').on('keypress', function(e){
        ch=e.which
        $(this).siblings('span').text("");
        v=$(this).val();
        $(this).siblings('span').css('color','red');
        if(this.selectionStart===0 && (ch==48 || ch==32))
        {
            $(this).siblings('span').text("At first position zero or space are not allowed");
            return false;
        }
        else if(!(ch>=48 && ch<=57))
        {
            $(this).siblings('span').text("Only digits are allowed");
            return false;
        }
        else if(v.length==10)
        {
            $(this).siblings('span').text("Only 10 digits are allowed");
            return false;
        }
    })
    $(".verifychar").on('keypress', function(e){
        ch=e.which
        $(this).siblings('span').text("");
        v=$(this).val();
        $(this).siblings('span').css('color','red')
        if(this.selectionStart===0 && ch==32)
        {
            $(this).siblings('span').text("*At first position space is not allowed");
            return false;
        }
        else if(v.slice(-1)==' ' && ch==32)
        {
            $(this).siblings('span').text("*Consecutive space is not allowed");
            return false;
        }
        else if(!((ch>=65 && ch<=90) || (ch>=97 && ch<=122) || ch==32))
        {
            $(this).siblings('span').text("*Only alphabets and space allowed");
            return false;
        }
    })
    // function disp(p)
    // {   
    //     x=['t1','t2']
    //     for(n in x)
    //     {
    //         lostfocus(x[n]);
    //     }
    //     if(flag==false)
    //     {
    //         a=parseFloat(document.getElementById('t1').value);
    //         b=parseFloat(document.getElementById('t2').value);
    //         if(p==1)
    //             r=a+b;
    //         else if(p==2)
    //             r=a-b;
    //         else if(p==3)
    //             r=a*b;
    //         else
    //             r=a/b;
    //         document.getElementById('res').innerHTML="Your result is "+r
    //     }
    // }