/**
* Created by tarena on 19-1-14.
*/
function next(flag) {
    $.ajax({
        url:'/next_page',
        type:'get',
        data: 'statu='+flag,
        success: function (data) {
            if(data==0){
                alert('这已经是首页了!');
            }
            if(data==2){
                alert('已是最后一页')
            }
            load();
        }
    })
}


function checkanw(cid) {
    if(!$("#in_a"+cid).val()){
        $("#ta"+cid).attr('type','button');
        return true
    }else{
        $("#ta"+cid).attr('type','submit');
        return false
    }
}

function to_answer(cid) {
    if(checkanw(cid)){
        return null
    }
    var anw = $("#in_a" +cid).val();
    $.ajax({
        url: "/answer",
        type: "post",
        data: {
            "anw": anw,
            "cid": cid,
        },
        success: function (data) {
            if (data == 1) {
                load();
            }
        }
    });
}

function answer(obj, f) {
    $.ajax({
        url:'/show_answer',
        type:"get",
        data:{'cid':obj.cid},
        dataType:'json',
        success:function (data) {
            var ans = "";
            ans += "<input class='answs' id='in_a"+obj.cid+"' type='text' placeholder='你的意见呢?'>";
            ans += "<button id='ta"+obj.cid+"' onclick='to_answer("+obj.cid+");'>评论</button>";
            $("#ta"+obj.cid).html(ans);
            if(data==0){
                $("#a"+obj.cid).html('无评论');
            }else{
                var html = "";
                $.each(data, function (i,obj2) {
                    html += "<h5 style='margin-bottom: -12px'>";
                    html += "第"+(i+1)+"楼的"+obj2.uname+"发表于:"+obj2.a_time;
                    html += "</h5>";
                    html += "<p style='font-size: 16px; margin-top: 10px;'>"+obj2.anw+"</p>";
                    html += "<div id='show_r"+obj2.id+"'></div>";

                    html += "<a onclick='wantReply("+obj2.id+","+f+")' ondblclick='closeReply("+obj2.id+")'>回复</a>";
                    html += "<p id='r"+obj2.id+"'></p>"

                    html += "<hr></hr>"
                });
                $("#a"+obj.cid).html(html);
            }
        }
    });
}

function load() {
    $(".chang_page").attr('style','');
    $("#reload").attr('onclick', 'load()');
     var xhr = createXhr();
     xhr.open('get','/get_comm',true);
     xhr.onreadystatechange = function () {
         if(xhr.readyState==4&&xhr.status==200){
             var res = xhr.responseText;
             //将res转换为JS对象再保存给res
             res = JSON.parse(res);
             //循环遍历res得到每一个对象以及数据
             var str = "";
             $.each(res,function(i,obj){
                 str += '<div class="comm">';
                 str += '<h4>';
                  str += "用户:"+obj.nickname+"&nbsp";
                  str += "于:"+obj.up_time;
                 str += '</h4>';
                 str += '<p>';
                  str += obj.text;
                 str += '</p>';
                 if(obj.image){
                    str += "<img class='comm_img' src='static/" + obj.image + "'>";
                 }
                 str += "<hr style='border: 3px groove yellow;'></hr>";
                 str += "<div id='a"+obj.cid+"'></div>";
                 str += "<p id='ta"+obj.cid+"'></p>";
                 answer(obj, 0);
                 str += '</div>';
             });
             $("#comm_ar").html(str);
             showReply();
         }
     };
     xhr.send(null);
}

// 我的记录功能
function my_history() {
    $(".chang_page").attr('style','display:none;');
    $("#reload").attr('onclick', 'my_history()');
    $.ajax({
        url:'/history',
        type:'get',
        dataType:'json',
        success: function (data) {
            var html = "";
            $.each(data.reverse(),function (i,obj) {
                html += '<div class="comm">';
                html += '<h4>';
                    html += obj.nickname + "发表于:" + obj.up_time;
                html += '</h4>';
                html += "<a href='javascript:void(0);' onclick='del_record("+obj.cid+");'>删除</a>";
                html += '<p>';
                    html += obj.text;
                html += '</p>';
                if(obj.image){
                    html += "<img class='comm_img' src='static/" + obj.image + "'>";
                }
                html += "<hr style='border: 3px groove rosybrown;'></hr>";
                html += "<div id='a"+obj.cid+"'></div>";
                html += "<p id='ta"+obj.cid+"'></p>";
                answer(obj, 1);
                html += '</div>';
            });
            $("#comm_ar").html(html);
            showReply();
        }
    });
    $("#title").text('我的记录');
}

// 即时显示被选图片
function show_image(f) {
    checknull();
    for (var i=0; i<f.length; i++){
        var reader = new FileReader();
        reader.readAsDataURL(f[i]);
        reader.onload = function (e) {
//                    e.target.resule获取到被选文件的路径
            $("#show").html("<img id='show1' src='"+e.target.result+"' >");
//                    显示图片后提示文字位置调整
            $("#word").attr('style',"position: relative; right: 135%;")
        }

    }
}

// 取消图片选择时,将显示图片和控件文件移除
function cancel() {
    $("#show").html("");
    $("#sele").val('');
    $("#text_in").val("");
    checknull();
}

// 检查发表文字和图片是否为空
function checknull() {
    if(!$("#text_in").val() && !$("#sele").val()){
        $("#btn_sub").attr('type','button');
        $("#btn_sub").attr('style','color:gray');
    }else{
        $("#btn_sub").attr('type','submit');
        $("#btn_sub").attr('style','color:black');
    }
}

// 删除指定记录
function del_record(cid) {
    $.ajax({
        url:'/del_record',
        type:'get',
        data:{"cid":cid},
        success: function (data) {
            if (data==1){
                console.log('完成函数触发');
                my_history();
            }
        }
    });
}

function checkIslog() {
    $.ajax({
        url:'/islog',
        type:'get',
        success: function (data) {
            if (data==1){
                $(".l_rlink").remove();
                console.log('已执行!')
            }
        }
    })
}


function wantReply(aid, f) {
    var html = '';
    html += "<input id='ri"+aid+"' type='text' name='reply'>";
    html += "<button onclick='backReply("+aid+","+f+")'>回复</button>";
    $("#r"+aid).html(html);
}

function closeReply(aid) {
    $("#r"+aid).html('');
}

function backReply(aid, f) {
    var reply = $("#ri"+aid).val();
    console.log(reply);

    $.ajax({
        url:'/reply',
        type:'get',
        data:{
            'reply': reply,
            'aid': aid
        },
        success: function (data) {
            if(f==0){
                load();
            }else{
                my_history();
            }
        }
    })
}

function showReply(where) {
    console.log('showR开始');
    $.ajax({
        url:'/getReply',
        type:'get',
        dataType: 'json',
        success: function (data) {
            $.each(data, function (i, obj) {
                var p = document.createElement('p');
                var html = '';
                html += obj.uname;
                html += ":";
                html += obj.rpl;
                p.innerHTML = html;
                console.log(p);
                $("#show_r"+obj.aid).append(p);
            });
            console.log('进入成功函数'+html);
        }
    });
    console.log('showR结束');
}










