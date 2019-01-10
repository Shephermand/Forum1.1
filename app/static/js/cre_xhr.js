/**
 * Created by tarena on 19-1-7.
 */
document.write("<script language=javascript src='/static/js/jquery-1.11.3.js'></script>");
function createXhr() {
    if(window.XMLHttpRequest){
        var xhr = new XMLHttpRequest();
    }else{
        var xhr = new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xhr;
}


// function load() {
//      var xhr = createXhr();
//      xhr.open('get','/get_comm',true);
//      xhr.onreadystatechange = function () {
//          if(xhr.readyState==4&&xhr.status==200){
//              var res = xhr.responseText;
//              //将res转换为JS对象再保存给res
//              res = JSON.parse(res);
//              //循环遍历res得到每一个对象以及数据
//              str = ""
//              $.each(res,function(i,obj){
//                  str += '<h4>';
//                   str += "用户:"+obj.uname+"&nbsp";
//                   str += "于:"+obj.up_time;
//                  str += '</h4>';
//                  str += '<p style="margin-left: 20px">';
//                   str += obj.text;
//                  str += '</p>';
//              });
//              $("#comm_ar").html(str)
//          }
//      }
//      xhr.send(null);
//    }



