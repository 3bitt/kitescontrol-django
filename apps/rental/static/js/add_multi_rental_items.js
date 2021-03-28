const rentalItem = document.querySelector('.rental-item')
const addNewItemBtn = document.querySelector('.add-new-rental')
const removeLastItemBtn = document.querySelector('.remove-last-rental')
const rentItemList = document.querySelector('.select-rent-item')

// Currently user can rent max. 7 items

addNewItemBtn.addEventListener('click', function(e){
  let rentalItemsList = document.querySelectorAll('.rental-item')  
  if (rentalItemsList.length < rentItemList.length -1){
    addHTMLnode();
  } else {
    addHTMLnode();
    addNewItemBtn.style.pointerEvents = 'none' // hidden true
  }
  removeLastItemBtn.style.pointerEvents = 'auto' // remove hidden  
})

removeLastItemBtn.addEventListener('click', function(e){
  let rentalItemsList = document.querySelectorAll('.rental-item')  
  if (rentalItemsList.length > 1){
    rentalItemsList[rentalItemsList.length-1].remove()
    
    if (rentalItemsList.length === 2){
      removeLastItemBtn.style.pointerEvents = 'none' // hidden
    }
  }
  if (rentalItemsList.length === rentItemList.length){
    addNewItemBtn.style.pointerEvents = 'auto' //remove hidden
  }  
})

function addHTMLnode(){
  const newNode = rentalItem.cloneNode(deep=true)
  rentalItem.parentNode.insertBefore(newNode, rentalItem.nextSibling);
}