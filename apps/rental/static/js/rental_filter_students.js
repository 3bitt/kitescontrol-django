const parentListElement = Array.from(document.getElementById('id_student').children)
const searchInput = document.getElementById('student_search_input');
const studentTakenList = document.getElementById('search_result_list');
const disabledStudentField = document.querySelector('.picked-student-disabled-field')

parentListElement.forEach((item) => {
  if (item.nodeType === 1) {
    item.addEventListener('change', (event) =>{
      if (event.target.checked) {
        addStudentToList(item)
      }  
    });
  }
});

// Append matched results to HTML list item
function setList(group){
  for (const person of group){
    parentListElement.appendChild(person)
  }
}

function clearOrigList(){
  parentListElement.forEach((item) => item.removeAttribute('hidden'))
}

function addStudentToList(obj){
  disabledStudentField.value = obj.innerText
}

// Actual search engine - fired every time user inputs character in search field
searchInput.addEventListener('input', (event) => {
  var value = event.target.value;

  if (value && value.trim().length > 0){
    value = value.trim().toLowerCase();
    setList(parentListElement.filter(person => {
      if (!person.innerText.trim().toLowerCase().includes(value)){
        person.setAttribute('hidden', true)
      } else {
        person.removeAttribute('hidden')
      }      
    }));
  } else {
    clearOrigList()
  }
})
