
document.addEventListener('DOMContentLoaded', function() {
    console.log("Inicializando selects");
   const elems = document.querySelectorAll('select');
   const instances = M.FormSelect.init(elems, {});
});