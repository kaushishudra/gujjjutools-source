document.body.insertAdjacentHTML("afterbegin", `
<div class="navbar">
    <div class="logo">
    <img src="/img/Comp_logo.png" alt="GujjuTools">
    
</div>


    <div class="hamburger" onclick="toggleMenu()">☰</div>

    <div class="menu" id="menu">

        <a href="index.html">Home</a>

        <!-- FILE TOOLS -->
        <div class="dropdown">
            <span class="dropbtn">File Tools</span>
            <div class="dropdown-content">
                <a href="merge.html">Merge PDF</a>
                <a href="split.html">Split PDF</a>
                <a href="pdfjpg.html">PDF → JPG</a>
                <a href="jpg-to-pdf.html">JPG → PDF</a>
            </div>
        </div>

        <!-- UTILITIES -->
        <div class="dropdown">
            <span class="dropbtn">Utilities</span>
            <div class="dropdown-content">
                <a href="calculator.html">Calculator</a>
                <a href="unit-converter.html">Unit Converter</a>
                <a href="password-generator.html">Password Generator</a>
                <a href="qr.html">QRCode Generator</a>
            </div>
        </div>

        <!-- DOWNLOAD -->
        <div class="dropdown">
            <span class="dropbtn">Download</span>
            <div class="dropdown-content">
                <a href="#" onclick="comingSoon(event)">Android</a>
                <a href="#" onclick="comingSoon(event)">iOS</a>
            </div>
        </div>

        <a href="about.html">About</a>

    </div>
</div>
`);

function toggleMenu(){
    document.getElementById("menu").classList.toggle("show");
}

document.querySelectorAll(".dropbtn").forEach(btn=>{
    btn.addEventListener("click", function(){
        this.nextElementSibling.classList.toggle("showDrop");
    });
});


function comingSoon(event){
    event.preventDefault();   // stop page navigation
    alert("Come in Future");
}
