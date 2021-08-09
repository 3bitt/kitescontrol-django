const rootElement = document.getRootNode()
const rentalSettingsBtn = document.getElementsByClassName('rental-settings-icon');

rootElement.addEventListener('click', (event) =>{
  for (var btn of rentalSettingsBtn){
     if (event.target != btn.nextElementSibling &&
        !btn.nextElementSibling.getAttribute('hidden') &&
        event.target != btn){
          btn.nextElementSibling.setAttribute('hidden', 'true')
          // btn.nextElementSibling.removeAttribute('hidden')
        }
  }
});

for (var btn of rentalSettingsBtn){
  btn.addEventListener('click', (event) => {
    switchHidden(event.target);
  });
}

function switchHidden(target){
  const menu = document.getElementById(target.nextElementSibling.id)
  if (menu.getAttribute('hidden')){
    menu.removeAttribute('hidden')
  } else {
    menu.setAttribute('hidden', 'true')
  }
}