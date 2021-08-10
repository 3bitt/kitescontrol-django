
const show_link = document.getElementById('show_collapse_parent')

show_link.addEventListener('click', e => {
  show()
})

function show(){
  var collapseElementList = [].slice.call(document.querySelectorAll('.summary_details'))
  var collapseList = collapseElementList.map(function (collapseEl) {
    return new bootstrap.Collapse(collapseEl)
  });
}
