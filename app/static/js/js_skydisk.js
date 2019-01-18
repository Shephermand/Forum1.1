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

//上传文件
function uploadFiles(){

    var formData = new FormData();
    var isUpload = window.confirm("是否确认上传此文件");
    if(!isUpload){
        return 0;
    }
     formData.append("file",$("#uploadFile")[0].files[0]);//append()里面的第一个参数file对应permission/upload里面的参数file
     formData.append("path", $("#hidden").val());
     $("#pbar").attr('style','display:block');

     $.ajax({
        type:"post",
        async:true,  //这里要设置异步上传，才能成功调用myXhr.upload.addEventListener('progress',function(e){}),progress的回掉函数
        Accept:'text/html;charset=UTF-8',
        data:formData,
        contentType:"multipart/form-data",
        url: '/push_file',
        processData: false, // 告诉jQuery不要去处理发送的数据
        contentType: false, // 告诉jQuery不要去设置Content-Type请求头
        xhr:function(){
        myXhr = $.ajaxSettings.xhr();
        if(myXhr.upload){ // check if upload property exists
            myXhr.upload.addEventListener('progress',function(e){
                var loaded = e.loaded;                  //已经上传大小情况
                var total = e.total;                      //附件总大小
                var percent = Math.floor(100*loaded/total)+"%";     //已经上传的百分比
                console.log("已经上传了："+percent);
                $("#processBar").css("width",percent);
                $("#percen").html(percent)
            }, false); // for handling the progress of the upload
        }
        return myXhr;
        },
        success:function(data){
            console.log("上传成功!!!!");
            location.reload();
        },
        error:function(){
            alert("上传失败！");
        }
    });
}


function deleteFile() {
    console.log("进入函数");
    var v = $("#deldata").serializeArray();
    console.log(v);
    var form = new FormData();
    $.each(v, function (i,obj) {
        console.log('进入第二函数');
        console.log(this.name);
        console.log(this.value);
        form.append(this.name, this.value);
    });
    console.log(form);

    $.ajax({
        type:"post",
        url:"/delfiles",
        contentType: false,
        processData: false,
        data:form,
        success: function (data) {
            location.reload();
        }
    })
}






















