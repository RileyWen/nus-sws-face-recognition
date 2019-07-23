let file;
let file_name;
let video_show = false;
let language = "English";

function file_upload() {
    file = $('#selected-file')[0].files[0];
    console.log(file);

    if (file) {
        let file_reader = new FileReader();
        file_reader.onloadend = function () {
            let form = new FormData();
            let dataURL;


            dataURL = file_reader.result;
            console.log(dataURL);
            form.append('file_name', file_name);
            form.append('file', dataURL);


            let xmlHTTP = new XMLHttpRequest();
            xmlHTTP.onreadystatechange = function () {
                if (xmlHTTP.readyState === 4) {
                    if (xmlHTTP.status === 200) {
                        console.log('上传成功！');
                        let resp_text = xmlHTTP.responseText;
                        console.log(xmlHTTP.responseText);
                        if (resp_text) {
                            let data_to_base64 = 'data:application/octet-stream;charset=utf-8;base64,';
                            // data_to_base64 += window.btoa(resp_text);
                            data_to_base64 += resp_text;
                            let button = document.getElementById("button-download");
                            button.href = data_to_base64;
                            button.download = file_name.split('.')[0] + '.srt';
                            jQuery('#button-download').fadeIn(500);
                        }
                    } else {
                        console.log("上传失败！");
                        console.log(xmlHTTP.responseText);
                    }
                }
            };
            xmlHTTP.open('post', 'UploadAudio');
            console.log(form);
            xmlHTTP.send(form);
        };
        file_reader.readAsDataURL(file);

        //进度条
        file_reader.addEventListener("progress", e => {
            document.querySelector('.progress').style.width = (e.loaded / e.total) * 100 + '%'
        });
        file_reader.addEventListener('error', err => {
            throw err;
        });
    } else {
        alert('You must select an video!');
    }


}

function filename_update() {

    file = $('#selected-file')[0].files[0];
    console.log(file);
    jQuery('#button-download').fadeOut(500);
    let file_label = document.getElementById('file-label');
    if (file) {
        file_label.textContent = file.name;
        file_name = file.name;
    }
}

function translation_lang() {
    language = $('#select option:selected').val();
    console.log(language);
}