const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))

const root = document.getElementById('root')

document.querySelectorAll('.leftnav-toggler').forEach(e => {
    e.addEventListener('click', () => {
        window.innerWidth < 992 || !root.classList.contains('leftnav-shown') ? root.classList.toggle('leftnav-shown') : root.classList.toggle('leftnav-shown')
    })
})

document.addEventListener('click', e => {
    e.target.classList.contains('root') && root.classList.remove('leftnav-shown')
})
