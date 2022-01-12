// random id generator
const getRandomId = () => {
  const string = "abcdefghijklmnopqrstuvwxyz1234567890";
  let id = "";
  for (let i = 0; i < 6; i++) {
    id += string.charAt(Math.floor(Math.random() * string.length));
  }
  return id;
};

// Button click handler
document.getElementById("startBtn").addEventListener("click", () => {
  let id = getRandomId();
  let url = `${location.href}play/${id}/`;
  location.href = url;
});
