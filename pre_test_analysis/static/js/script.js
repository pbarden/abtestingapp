document.addEventListener('DOMContentLoaded', function() {
    let dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    
    dropdownToggles.forEach(function(toggle) {
        toggle.addEventListener('click', function() {
            let dropdownMenu = this.nextElementSibling; 
            dropdownMenu.classList.toggle('show-dropdown');
        });
    });
});

function toggleNav() {
    let navLinks = document.getElementById("navLinks");
    navLinks.classList.toggle('show');
}

function openDropdown(element) {
    clearTimeout(element.delay);
    let dropdownContent = element.querySelector('.dropdown-content');
    dropdownContent.style.display = 'block';
    setTimeout(() => dropdownContent.style.opacity = 1, 10);
}

function closeDropdown(element) {
    let dropdownContent = element.querySelector('.dropdown-content');
    dropdownContent.style.opacity = 0;
    element.delay = setTimeout(() => {
        dropdownContent.style.display = 'none';
    }, 500); 
}

document.querySelectorAll('.neu-button').forEach(button => {
    button.addEventListener('mousedown', () => {
        button.classList.add('button-clicked');
    });

    button.addEventListener('mouseup', () => {
        button.classList.remove('button-clicked');
    });

    button.addEventListener('mouseleave', () => {
        button.classList.remove('button-clicked');
    });
});
