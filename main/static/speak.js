/**
* Created by Admin on 2017-11-20.
*/
function checkCompatibilty () {
    if(!('speechSynthesis' in window)){
        alert('Your browser is not supported. If google chrome, please upgrade!!');
    }
};

checkCompatibilty();

// var voiceOptions = document.getElementById('voiceOptions');
// var myText = document.getElementById('myText');
// var Text = document.getElementById("Text").innerHTML;


console.log(Text);

var voiceMap = [];

function loadVoices () {
    var voices = speechSynthesis.getVoices();
    for (var i = 0; i < voices.length; i++) {
        var voice = voices[i];
        var option = document.createElement('option');
        option.value = voice.name;
        option.innerHTML = voice.name;
        voiceMap[voice.name] = voice;
    };
};

window.speechSynthesis.onvoiceschanged = function(e){
    loadVoices();
};


function speak () {
    var msg = new SpeechSynthesisUtterance();
    msg.volume = 0.5;

    // msg.voice = voiceMap[voiceOptions.value];
    Text="hello to conference room"
    msg.text = Text;
    window.speechSynthesis.speak(msg);
};
