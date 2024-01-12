let layer = document.getElementById("l")
let layer1 = document.getElementById("l1")
let layer2 = document.getElementById("l2")
let layer3 = document.getElementById("l3")
let layer4 = document.getElementById("l4")
let olayer = document.getElementById("ol")
let team = document.getElementById("teamtext")
let actualbody = document.getElementsByClassName("container")




if(team)
{
    console.log("team found");
}
console.log("wokin da pundaaaaaaaaaaaaaaaaaaa")

window.addEventListener('scroll', function(){
    var value = window.scrollY;

    layer3.style.right = value*0.2 + 'px';
    layer2.style.top = value*0.5 + 'px';
    layer1.style.left = -value*0.5 + 'px';
    olayer.style.top = -value*2+ 'px';
    layer4.style.top = -value + 'px';
    team.style.marginTop = value*2 + 200 + 'px';
})