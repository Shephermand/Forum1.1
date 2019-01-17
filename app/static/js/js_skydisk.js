/**
 * Created by tarena on 19-1-15.
 */

function newdir(abs_path){
    filename = prompt('请输入文件名');
    $.ajax({
        url: '/makefile',
        type: 'get',
        data: {
            'flag':'mkdir',
            'abs_path':abs_path,
            'dirName':filename,
        },
        success: function (data) {
            if(data==1){
                location.reload();
            }
        }
    });
}

function nihao() {
    alert('你好');
}

function topath(index) {
    console.log(index);
}


// 导入文件
function goodfile(){
    console.log('进入处理!');
    // var exp = /.xls$|.xlsx$/;
    // if(exp.exec($(this).val())==null){
    //     $(this).val('');
    //     layer.msg('格式错误',{icon: 2});
    //     return false;
    // };
    // var data = new FormData();
    // data.append('file', $('#leading_in')[0].files[0]);
    // data.append('vote_id', $('input[name="vote_id"]').val());
    //
    // var file = this.files[0];
    // name = file.name;
    // size = file.size;
    // type = file.type;
    // url = window.URL.createObjectURL(file);
    //
    // $.ajax({
    //     url: 'index.php?c=Vote&a=importExcel',
    //     type: 'post',
    //     data: data,
    //     cache: false,
    //     contentType: false,
    //     processData: false,
    //     crossDomain: true,
    //     xhrFields: {withCredentials: true},
    //     dataType: 'json',
    //     beforeSend: function(){ },
    //     xhr: function(){
    //         myXhr = $.ajaxSettings.xhr();
    //         if(myXhr.upload){
    //             myXhr.upload.addEventListener('progress',progressHandlingFunction, false);
    //         }
    //         return myXhr;
    //         },
    //     success: function(res) {
    //         if (res.code == 200) {
    //             layer.msg('上传成功', {icon :1});
    //             setTimeout(function(){
    //                 location.reload();
    //             },1000);
    //         }else{
    //             layer.msg(res.msg, {icon: 2});
    //         }
    //     },
    // });
};

function progressHandlingFunction(e) {
    if (e.lengthComputable) {
        $('progress').attr({value : e.loaded, max : e.total});
        var percent = e.loaded/e.total*100;
        $('#progress').html(((e.loaded/1024)/1024).toFixed(2) + "/" + ((e.total/1024)/1024).toFixed(2)+" MB. " + percent.toFixed(2) + "%"); } }
