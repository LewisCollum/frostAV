function handleUrlResponse(url, onUrlResponseText) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4)
            onUrlResponseText(this.responseText)
    }
    xhttp.open("GET", url, true);
    xhttp.send();
}


let controlPanel = new cpanel.Panel("controlPanel")
controlPanel.style = "Panel"
controlPanel.appendToParent(document.getElementById("control"))

let actionCategory = new cpanel.ToggleButtonCategory("Action")
actionCategory.addButton("Drive")
controlPanel.addCategory(actionCategory)
controlPanel.open()


let panel = new cpanel.Panel("panel")
panel.style = "Panel"
panel.appendToParent(document.getElementById("cameraContainer"))

let openButton = new cpanel.PanelOpenButton(panel)
openButton.style = "PanelOpenButton"
openButton.appendToParent(document.getElementById("cameraContainer"))

panel.addButtonChangeListener((change) => {
    var request = new XMLHttpRequest();
    request.open("POST", "/updateImageStream")
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    request.send(JSON.stringify(change))              
})


function addNamesToCategory(names, category) {
    names.forEach((name) => {
        category.addButton(name)
    })
}
function turnOnButtonsInCategory(names, category) {
    names.forEach((name) => {
        category.turnOnButton(name)
    })
}
const buttonFormatToCategoryType = {
    'toggle': cpanel.ToggleButtonCategory,
    'radio': cpanel.RadioButtonCategory
}
function createCategoryFromServerCategory(categoryName, serverCategory) {
    let buttonFormat = serverCategory.type
    let CategoryType = buttonFormatToCategoryType[buttonFormat]    
    let category = new CategoryType(categoryName)
    addNamesToCategory(serverCategory.names, category)
    turnOnButtonsInCategory(serverCategory.defaults, category)
    return category
}
function setupPanelFromServerCategories(panel, serverCategories) {
    for (let [categoryName, serverCategory] of Object.entries(serverCategories)) {
        let category = createCategoryFromServerCategory(categoryName, serverCategory)
        panel.addCategory(category)
    }
}
handleUrlResponse('/imageStreamChoices', (response) => {
    let serverCategories = JSON.parse(response)
    setupPanelFromServerCategories(panel, serverCategories)
})




window.addEventListener("gamepadconnected", function(e) {
    console.log("Gamepad connected at index %d: %s. %d buttons, %d axes.",
                e.gamepad.index, e.gamepad.id,
                e.gamepad.buttons.length, e.gamepad.axes.length);
})

const handleResponse = ({target}) => {
    console.log(target.responseText)
}

var steeringPrevious = null
var forwardPrevious = null
var reversePrevious = null
setInterval(function() {
    let gamepad = navigator.getGamepads()[0]
    if (gamepad) {
        let steering = gamepad.axes[0]
        let forward = gamepad.axes[4]
        let reverse = gamepad.axes[3]

        if (steering != steeringPrevious || forward != forwardPrevious || reverse != reversePrevious) {
            const xhr = new XMLHttpRequest()
            let update = JSON.stringify({
                'steering': steering,
                'forward': forward,
                'reverse': reverse})
            
            xhr.addEventListener('load', handleResponse)
            xhr.open('POST', '/gamepad')
            xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
            xhr.send(update)                                    

            steeringPrevious = steering
            forwardPrevious = forward
            reversePrevious = reverse
        }
    }
}, 50)
