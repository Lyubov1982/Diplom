let searchForm = document.getElementById('search');
let pagelink = document.querySelectorAll('.page-link');

if (searchForm) {
for(let i = 0; pagelink.length > i; i++){
  pagelink[i].addEventListener('click', function(e){
    e.preventDefault();

    let page = this.dataset.page;
    searchForm.innerHTML += `<input value=${page} name="page" type="hidden">`;

    searchForm.submit();
  })
}
}
