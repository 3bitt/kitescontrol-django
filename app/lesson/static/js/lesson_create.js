const instructors_source_list = Array.from(document.getElementById('id_instructor').children);
const instructor_picked_list = document.querySelector('.instructor-picked-list');
const instructor_is_empty_div = document.querySelector('.instructor-not-picked');

const students_source_list = Array.from(document.getElementById('id_student').children);
const student_picked_list = document.querySelector('.student-picked-list');
const student_is_empty_div = document.querySelector('.student-not-picked');

instructors_source_list.forEach((instructor) => {
  if (instructor.nodeType === 1) {
    instructor.addEventListener('change', (e) => {
      if (e.target.checked){
        pickInstructor(instructor);
      }
      else if (!e.target.checked){
        removePickedInstructor(instructor);
      }
    });
  }
})

students_source_list.forEach((student) => {
  if (student.nodeType === 1) {
    student.addEventListener('change', (e) => {
      if (e.target.checked) {
        pickStudent(student);
      }
      else if (!e.target.checked) {
        removePickedStudent(student);
      }
    });
  }
})



// Instructor functions
function pickInstructor(instr){
  new_instr_div = createInstructorElement(instr);
  instructor_is_empty_div.setAttribute('hidden', 'true');
  instructor_picked_list.appendChild(new_instr_div);
}

function removePickedInstructor(instr){
  const target_instr_div = document.querySelector(`.${instr.firstChild.htmlFor}`);
  target_instr_div.remove();

  const instr_checkbox = document.getElementById(`${instr.firstChild.htmlFor}`);
  instr_checkbox.checked = false;
  checkInstrListIfEmpty();

}

function checkInstrListIfEmpty(){
  if (instructor_picked_list.children.length == 1){
    instructor_is_empty_div.removeAttribute('hidden')
  }
}

function createInstructorElement(instr){
  const new_div = document.createElement('div');
  new_div.classList.add('instructor-picked', `${instr.firstChild.htmlFor}`);
  text = document.createTextNode(instr.innerText);

  const icon = document.createElement('i')
  icon.classList.add('fas', 'fa-times', 'remove-icon')

  icon.addEventListener('click', (e) => {
    removePickedInstructor(instr);
  })

  new_div.appendChild(text);
  new_div.appendChild(icon);
  return new_div
}

// -----------------
// Student functions
// -----------------

function pickStudent(student) {
  new_student_div = createStudentElement(student);
  student_is_empty_div.setAttribute('hidden', 'true');
  student_picked_list.appendChild(new_student_div);
}

function removePickedStudent(student) {
  const target_student_div = document.querySelector(`.${student.firstChild.htmlFor}`);
  target_student_div.remove();

  const student_checkbox = document.getElementById(`${student.firstChild.htmlFor}`);
  student_checkbox.checked = false;
  checkStudentListIfEmpty();

}

function checkStudentListIfEmpty() {
  if (student_picked_list.children.length == 1) {
    student_is_empty_div.removeAttribute('hidden')
  }
}

function createStudentElement(student) {
  const new_div = document.createElement('div');
  new_div.classList.add('student-picked', `${student.firstChild.htmlFor}`);
  text = document.createTextNode(student.innerText);

  const icon = document.createElement('i')
  icon.classList.add('fas', 'fa-times', 'remove-icon')

  icon.addEventListener('click', (e) => {
    removePickedStudent(student);
  })

  new_div.appendChild(text);
  new_div.appendChild(icon);
  return new_div
}