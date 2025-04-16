document.addEventListener('DOMContentLoaded', function() {
    const dateElements = document.querySelectorAll('.date');
    
    dateElements.forEach(dateElement => {
        const dateString = dateElement.textContent.trim();
        const localDate = new Date(dateString);
        if (isNaN(localDate.getTime())) {
          console.error('Неверный формат даты:', dateString);
          return;
        }

        const formattedDate = dateFns.format(localDate, "d MMMM yyyy, HH:mm", {
          locale: dateFns.locale.ru,
        });
        dateElement.textContent = formattedDate;
    })
});