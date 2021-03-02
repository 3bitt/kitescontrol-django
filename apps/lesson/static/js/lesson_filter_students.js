const parentListElement = Array.from(document.getElementById('id_student').children)
const dupa = document.getElementById('id_student').children
// const initialListElements = parentListElement.cloneNode(true)
console.log(dupa);

const searchInput = document.getElementById('student_search_input');
const studentTakenList = document.getElementById('search_result_list');

// const list = document.getElementById('search_result_list')
// initialListElements.childNodes.forEach((item) => {
//   if (item.nodeType === 1) {
//     initialStudentsList.push(item)
//   }
// })
var students = []

parentListElement.forEach((item) => {
  if (item.nodeType === 1) {
    item.addEventListener('change', (event) =>{
      if (event.target.checked) {
        addStudent(item)
      } else {
        
        for (let node of studentTakenList.children) {
          if (node.innerText.trim() === item.innerText.trim()) {
            studentTakenList.removeChild(node)
            
          }
          
        }
      }   
    })
  }
})

// Append matched results to HTML list item
function setList(group){
  // clearList()
  // clearOrigList()
  for (const person of group){
    // const item = document.createElement('li');
    // person.classList.add('search-result-item');
    // const text = document.createTextNode(person.fields.name + ' ' + person.fields.surname);
    parentListElement.appendChild(person)
    // list.appendChild(item)

  }
  if (group.length === 0){
    setNoResults()
  }
}
function clearOrigList(){
  parentListElement.forEach((item) => item.removeAttribute('hidden'))
}
function addStudent(obj){
  const liItem = document.createElement('li');
  liItem.classList.add('student-picked')
  const text = document.createTextNode(obj.innerText);

  liItem.appendChild(text)
  studentTakenList.appendChild(liItem)
}
function returnOrigList(){
  clearOrigList()
  for (const listItem of initialStudentsList) {
    parentListElement.appendChild(listItem)
  }

}
// Set HTML list item to show No Results in case of zero matches
function setNoResults(){
  const item = document.createElement('li');
  // item.classList.add('search-result-item');
  const text = document.createTextNode('Brak wyników');
  item.appendChild(text);
  // parentListElement.appendChild(item);
  parentListElement.push(item)
}

// while (parentListElement.hasChildNodes()) {
//   parentListElement.removeChild(parentListElement.firstChild)
  
// }

// Actual search engine - fired every time user inputs character in search field
searchInput.addEventListener('input', (event) => {
  var value = event.target.value;

  if (value && value.trim().length > 0){
    // clearOrigList()
    value = value.trim().toLowerCase();
    setList(parentListElement.filter(person => {
      if (!person.innerText.trim().toLowerCase().includes(value)){
        person.setAttribute('hidden', true)
        // return person;
      } else {
        person.removeAttribute('hidden')
      }      
    }));

  } else {
    clearOrigList()
    
    // clearOrigList();
    // returnOrigList();
  }
})
