const parentListElement = Array.from(document.getElementById('id_student').children)
const searchInput = document.getElementById('student_search_input');

// Actual search engine - fired every time user inputs character in search field
searchInput.addEventListener('input', (event) => {
  var value = event.target.value;

  if (value && value.trim().length > 0) {
    value = value.trim().toLowerCase();
    setList(parentListElement.filter(person => {
      if (!person.innerText.trim().toLowerCase().includes(value)) {
        person.setAttribute('hidden', true)
      } else {
        person.removeAttribute('hidden')
      }
    }));
  } else {
    clearOrigList()
  }
})

// Append matched results to HTML list item
function setList(group){

  for (const person of group){
    parentListElement.appendChild(person)
  }
  if (group.length === 0){
    setNoResults()
  }
}
function clearOrigList(){
  parentListElement.forEach((item) => item.removeAttribute('hidden'))
}

// Set HTML list item to show No Results in case of zero matches
function setNoResults(){
  const item = document.createElement('li');
  const text = document.createTextNode('Brak wyników');
  item.appendChild(text);
  parentListElement.push(item)
}


