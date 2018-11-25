function activateJustificativaTextArea(checkboxElem) {
    const textarea = document.getElementById('id_justificativa');

    if (checkboxElem.checked) {
        textarea.disabled = true;
        console.log("removing hiddendiv");
    } else {
        textarea.disabled = false;
        console.log("adding hiddendiv");
    }
}