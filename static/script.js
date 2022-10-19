
const searchInput = document.querySelector("[data-search]")

const header = document.querySelectorAll("[data-header]")

searchInput.addEventListener("input", e => {
    const value = e.target.value
    var listArray = [...header]
    listArray.forEach(recipe => {
        recipe.hidden = false
        const isVisible = recipe.children[0].children[0].children[0].children[0].value.includes(value)
        if(!isVisible){
            
            recipe.hidden = true;
        }
        
    })
})
;