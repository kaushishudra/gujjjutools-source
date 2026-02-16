/* create transition layer */
const transition = document.createElement("div");
transition.id = "page-transition";
document.body.appendChild(transition);

/* click navigation animation */
document.addEventListener("click", function(e){
    const link = e.target.closest("a");

    if(!link) return;

    const url = link.getAttribute("href");

    if(!url || url.startsWith("#") || url.startsWith("javascript")) return;

    e.preventDefault();

    transition.classList.add("active");

    setTimeout(()=>{
        window.location.href = url;
    },300);
});

/* FIX BACK BUTTON WHITE SCREEN */
window.addEventListener("pageshow", function(){
    transition.classList.remove("active");
});
