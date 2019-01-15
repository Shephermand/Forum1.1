/**
 * Created by tarena on 19-1-15.
 */

function newdir(){
    filename = prompt('请输入文件名');
    $.ajax({
        url: '/makefile',
        type: 'get',
        data: {
            'flag':'mkdir',
            'dirName':filename,
        },
        success: function (data) {
            if(data==1){
                alert('创建成功!')
            }
        }
    });
}

function topath(index) {
    console.log(index);
}
