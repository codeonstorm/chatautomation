;(() => {
  // Create chatbot container
  var container = document.createElement("div")
  container.id = "ai-chatbot-container"
  container.style.position = "fixed"
  container.style.bottom = "20px"
  container.style.right = "20px"
  container.style.width = "300px"
  container.style.height = "400px"
  container.style.border = "1px solid #ccc"
  container.style.borderRadius = "10px"
  container.style.overflow = "hidden"

  // Create chatbot iframe
  var iframe = document.createElement("iframe")
  iframe.style.width = "100%"
  iframe.style.height = "100%"
  iframe.style.border = "none"

  // Get chatbot ID from script data attribute
  var script =
    document.currentScript ||
    (() => {
      var scripts = document.getElementsByTagName("script")
      return scripts[scripts.length - 1]
    })()
  var chatbotId = script.getAttribute("data-chatbot-id")

  // Set iframe source
  iframe.src = "https://your-chatbot-service.com/chat/" + chatbotId

  // Append iframe to container
  container.appendChild(iframe)

  // Append container to body
  document.body.appendChild(container)
})()

