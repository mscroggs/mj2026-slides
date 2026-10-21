var nslides = {nslides}
var cSlide = 0

document.addEventListener('keydown', function(event){
    const currentCode = event.which || event.code;
    var currentKey = event.key;
    if (!currentKey) {
        currentKey = String.fromCharCode(currentCode);
    }
    const keyName = "" + currentKey
    process_key(keyName)
});

function process_key(keyName){
    document.getElementById("slide"+cSlide).style.display = "none"
    if((keyName == "ArrowRight" || keyName == "PageDown") && cSlide + 1 < nslides){
        if(exit_fs[cSlide] !== false){
            exit_fs[cSlide]()
        }
        cSlide++
        if(enter_fs[cSlide] !== false){
            enter_fs[cSlide]()
        }
    }
    if((keyName == "ArrowLeft" || keyName == "PageUp") && cSlide > 0){
        if(exit_fs[cSlide] !== false){
            exit_fs[cSlide]()
        }
        cSlide--
        if(enter_fs[cSlide] !== false){
            enter_fs[cSlide]()
        }
    }
    document.getElementById("slide"+cSlide).style.display = "block"
}
