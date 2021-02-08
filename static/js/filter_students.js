const mydata = JSON.parse(JSON.parse(document.getElementById('data').textContent))

const searchInput = document.getElementById('student_search_input');
const list = document.getElementById('search_result_list')
console.log(mydata);

// Append matched results to HTML list item
function setList(group){
  clearList()
  for (const person of group){
    const item = document.createElement('li');
    item.classList.add('search-result-item');
    const text = document.createTextNode(person.fields.name + ' ' + person.fields.surname);
    item.appendChild(text)
    list.appendChild(item)

  }
  if (group.length === 0){
    setNoResults()
  }
}

function clearList(){
  while (list.firstChild){
    list.removeChild(list.firstChild)
  }
}

// Set HTML list item to show No Results in case of zero matches
function setNoResults(){
  const item = document.createElement('li');
  item.classList.add('search-result-item');
  const text = document.createTextNode('Brak wyników');
  item.appendChild(text);
  list.appendChild(item);
}

// Actual search engine - fired every time user inputs character in search field
searchInput.addEventListener('input', (event) => {
  var value = event.target.value;
  if (value && value.trim().length > 0){
    value = value.trim().toLowerCase();
    setList(mydata.filter(person => {
      if (person.fields.name.toLowerCase().includes(value) || person.fields.surname.toLowerCase().includes(value)){
        return person;
      }      
      }));

  } else {
    clearList();
  }
  
}
)


