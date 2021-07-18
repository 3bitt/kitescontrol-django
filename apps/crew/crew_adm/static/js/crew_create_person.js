var create_user_form_zone = document.querySelector('.create-user-form-zone');
var user_profile_choice = document.getElementById('user_profile');
var is_instructor_html_section = document.querySelector('.is-instructor-question');

var is_instructor_radios = document.getElementsByName('manager_is_instructor');

user_profile_choice.addEventListener('change', switchProfileContext);


function switchProfileContext(dropdown){
  var profile = dropdown.target.value;
  if (profile === ''){
    create_user_form_zone.innerHTML = null
    is_instructor_html_section.setAttribute('hidden', true);
    is_instructor_radios.forEach(radio => { radio.checked = false; radio.removeEventListener('change', switchManagerForm, true) });
  }
  else if (profile == 'MANAGER' ){
    create_user_form_zone.innerHTML = null
    is_instructor_html_section.removeAttribute('hidden');
    is_instructor_radios.forEach(radio => { radio.addEventListener('change', switchManagerForm)});
  } else {
    is_instructor_html_section.setAttribute('hidden', true);
    is_instructor_radios.forEach(radio => { radio.checked = false; radio.removeEventListener('change', switchManagerForm, true)});
    getUserForm(profile)
  }
}

function switchManagerForm(is_instructor_radio){
  if (is_instructor_radio.target.value == 'True'){
    // Manager with instructor record
    getUserWithInstructorForm(user_type='MANAGER')
  } else {
    // Manager without instructor record
    getUserWithoutInstructorForm(user_type='MANAGER')
  }

}

function getUserForm(user_type){
  if (user_type == 'CLERK'){
    getUserWithoutInstructorForm(user_type)
  } else if (user_type = 'INSTRUCTOR') {
    getUserWithInstructorForm(user_type)
  }
}


function getUserWithInstructorForm(user_type){
  axios.get(`create-user-instructor/`, {
    params: {
      userType: user_type
    }
  })
    .then(response => { create_user_form_zone.innerHTML = response.data });
}

function getUserWithoutInstructorForm(user_type){
  axios.get(`/auth/create-user/`, {
    params: {
      userType: user_type
    }
  })
    .then(response => { create_user_form_zone.innerHTML = response.data });
}
