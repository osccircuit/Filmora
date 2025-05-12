document.addEventListener('DOMContentLoaded', () => {
	const btnMobileNav = document.querySelector('.btn-mobile-nav')
	const navBlock = document.querySelector('.main-nav-block')
	const menuIcon = document.querySelector('.icon-mobile-nav[name="menu"]')
	const closeIcon = document.querySelector(
		'.icon-mobile-nav[name="close"]'
	)

	// Устанавливаем начальное состояние иконок
	menuIcon.style.display = 'block'
	closeIcon.style.display = 'none'

	// Обработчик клика на кнопку-бургер
	btnMobileNav.addEventListener('click', () => {
		navBlock.classList.toggle('open')
		const isOpen = navBlock.classList.contains('open')
		menuIcon.style.display = isOpen ? 'none' : 'block'
		closeIcon.style.display = isOpen ? 'block' : 'none'
	})
})