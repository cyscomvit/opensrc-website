const card = document.querySelectorAll(".circle");
const targets = document.querySelectorAll(".target");
card.forEach((btn) => {
  btn.addEventListener("click", () => {
    btn.parentElement.classList.toggle('change')
  });
});
