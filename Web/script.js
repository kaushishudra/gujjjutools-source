const API="http://127.0.0.1:8000";
function showLoader(){
    document.getElementById("loader").style.display="flex";
}
function hideLoader(){
    document.getElementById("loader").style.display="none";
}

/* get selected files */
function getInput(){
    const input=document.getElementById("files");
    if(!input || input.files.length===0){
        alert("Please select file first");
        return null;
    }
    return input;
}

/* helper download */
async function download(res,name){

    if(!res.ok){
        hideLoader();
        alert("Processing failed");
        return;
    }

    const blob=await res.blob();
    const url=window.URL.createObjectURL(blob);

    const a=document.createElement("a");
    a.href=url;
    a.download=name;
    a.click();

    hideLoader();
}


/* MERGE */
async function merge(){
    const input=getInput(); if(!input) return;
    showLoader();

    const form=new FormData();
    for(let i=0;i<input.files.length;i++){
        form.append("files", input.files[i]);
    }

    const res=await fetch(API+"/merge",{method:"POST",body:form});
    download(res,"merged.pdf");
}


/* SPLIT */
async function splitPDF(){
    const input=getInput(); if(!input) return;
    showLoader();

    const form=new FormData();
    form.append("file", input.files[0]);   // important: file NOT files

    const res=await fetch(API+"/split",{method:"POST",body:form});
    download(res,"split.zip");
}



/* PDF → JPG */
async function pdfToJpg(){
    const input=getInput(); if(!input) return;
    showLoader();

    const form=new FormData();
    form.append("file", input.files[0]);

    const res=await fetch(API+"/pdf-to-jpg",{method:"POST",body:form});
    download(res,"images.zip");
}


/* JPG → PDF */
async function jpgToPdf(){
    const input=getInput(); if(!input) return;
    showLoader();

    const form=new FormData();
    for(let i=0;i<input.files.length;i++){
        form.append("files", input.files[i]);
    }

    const res=await fetch(API+"/jpg-to-pdf",{method:"POST",body:form});
    download(res,"converted.pdf");
}

