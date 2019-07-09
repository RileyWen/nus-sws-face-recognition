let file;

function file_upload() {
    if (file) {
        let form = new FormData();
        let dataURL;

        let file_reader = new FileReader();
        file_reader.onloadend = function () {
            dataURL = file_reader.result;
            form.append('image', dataURL);

            let xmlHTTP = new XMLHttpRequest();
            xmlHTTP.onreadystatechange = function () {
                if (xmlHTTP.readyState === 4) {
                    if (xmlHTTP.status === 200) {
                        let resp_text = xmlHTTP.responseText;
                        console.log(xmlHTTP.responseText);

                        let img = document.getElementById("result-img");
                        img.src = resp_text;
                    } else {
                        console.log(xmlHTTP.responseText);
                    }
                }
            };
            xmlHTTP.open('post', 'UploadPic');
            // alert(dataURL;
            // xmlHTTP.setRequestHeader("Content-type","application/x-www-form-urlencoded");
            xmlHTTP.send(form);
        };
        file_reader.readAsDataURL(file);
    } else {
        alert('You must select an image!');
    }
}

function filename_update() {
    file = $('#selected-file')[0].files[0];
    let file_label = document.getElementById('file-label');
    if (file) {
        file_label.textContent = file.name;
    }
}