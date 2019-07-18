let file;
let video_show = false;

function file_upload() {
    file = $('#selected-file')[0].files[0];
    console.log(file);

    if (file) {
        let form = new FormData();
        let dataURL;

        let file_reader = new FileReader();
        file_reader.onloadend = function () {
            dataURL = file_reader.result;
            console.log(dataURL);
            form.append('file', file);
            

            let xmlHTTP = new XMLHttpRequest();
            xmlHTTP.onreadystatechange = function () {
                if (xmlHTTP.readyState === 4) {
                    if (xmlHTTP.status === 200) {
                        console.log('上传成功！');
                        let resp_text = xmlHTTP.responseText;
                        console.log(xmlHTTP.responseText);
                        let video = document.getElementById("result-video");
                        video.src = resp_text;
                    } else {
                        console.log("上传失败！");
                        console.log(xmlHTTP.responseText);
                    }
                }
            };
            xmlHTTP.open('post', 'UploadAudio');   
            // alert(dataURL;
            // xmlHTTP.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            console.log(form);
            xmlHTTP.send(form);
        };
        file_reader.readAsDataURL(file);

        //进度条
        file_reader.addEventListener("progress",e=>{
            document.querySelector('.progress').style.width=(e.loaded/e.total)*100+'%'
        });
        file_reader.addEventListener('error',err=>{
            throw err;
        });
    } else {
        alert('You must select an video!');
    }


}

function filename_update() {
    
    file = $('#selected-file')[0].files[0];
    console.log(file);
    let file_label = document.getElementById('file-label');
    if (file) {
        file_label.textContent = file.name;
    }
}