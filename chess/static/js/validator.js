function validateForm() {
    var result = [];
    var element = document.getElementById("players_selector");
    for (var i=0; i < element.options.length; i++){
        if (element.options[i].selected==true) {
            result.push(element.options[i].value);}
            document.getElementById('players').value = result;
    }
    if (result.length < 2) {
        var $el = document.getElementById('users');
        var err = document.createElement('p');
        err.innerHTML = '<span>There must be at least three participants in the tournament.</span>';
        err.style.fontSize = '10px';
        err.style.color = 'red';
        $el.appendChild(err);
        return false;
    }
    return true;
}
