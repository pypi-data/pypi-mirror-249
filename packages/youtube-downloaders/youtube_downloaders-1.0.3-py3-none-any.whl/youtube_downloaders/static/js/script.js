let select_checkbox = (index) => {
    let vid = document.getElementById(index)
    console.log(vid)
    if (vid.checked ){
        vid.checked = false
    }
    else{
        vid.checked = true
    }
}

let select_allcheckbox = () => {
    let SelectAll = document.getElementById("all")
    let allVid =  document.querySelectorAll(".video")
    if (SelectAll.checked ){
        SelectAll.checked = false
        for (var vid = 0; vid < allVid.length; vid++){
            allVid[vid].checked = false
        }
    }
    else{
        SelectAll.checked = true
        for (var vid = 0; vid < allVid.length; vid++){
            allVid[vid].checked = true
        }
    }
}

let select_onbox = () => {
    let SelectAll = document.getElementById("all")
    let allVid =  document.querySelectorAll(".video")
    if (SelectAll.checked ){
        for (var vid = 0; vid < allVid.length; vid++){
            allVid[vid].checked = true
        }
        console.log("Uncheck")
    }
    else{
        for (var vid = 0; vid < allVid.length; vid++){
            allVid[vid].checked = false
        }
        console.log("check")
    }
}

let form1_sumbit = () => {
    document.getElementById('loading').style.display = 'block';
    form = document.getElementById("form1");
    setTimeout(function () {
        document.getElementById('loading').style.display = 'none';
        form.submit();
    }, 10000);
}


let form2_sumbit = () => {
    document.getElementById('loading').style.display = 'block';
    form = document.getElementById("form2");
    setTimeout(function () {
        document.getElementById('loading').style.display = 'none';
        form.submit();
    }, 20000);
}
