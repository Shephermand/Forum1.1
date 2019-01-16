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

function topath(index) {
    console.log(index);
}
