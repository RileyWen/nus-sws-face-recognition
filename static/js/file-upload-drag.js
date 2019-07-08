function file_upload() {
    let file_label = document.getElementById('file-label');
    let file = $('#selected-file')[0].files[0];
    if (file) {
        file_label.textContent = file.name;

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
                        // alert(xmlHTTP.responseText);
                        console.log(xmlHTTP.responseText);
                    } else {
                        // alert(xmlHTTP.responseText);
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
    }
}