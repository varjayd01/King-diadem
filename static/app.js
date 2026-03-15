let deferredPrompt;

window.addEventListener("beforeinstallprompt", (e) => {

e.preventDefault();

deferredPrompt = e;

const installBtn = document.createElement("button");

installBtn.innerText = "Install KING DIADEM";

installBtn.style.position = "fixed";
installBtn.style.bottom = "20px";
installBtn.style.left = "50%";
installBtn.style.transform = "translateX(-50%)";
installBtn.style.padding = "12px 20px";
installBtn.style.background = "#111";
installBtn.style.color = "#fff";
installBtn.style.border = "1px solid #444";
installBtn.style.borderRadius = "8px";
installBtn.style.zIndex = "9999";

installBtn.onclick = async () => {

installBtn.remove();

deferredPrompt.prompt();

};

document.body.appendChild(installBtn);

});
