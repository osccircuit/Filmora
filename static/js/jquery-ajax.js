// Когда html документ готов (прорисован)
$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");
    var errorMessage = $("#jq-notification-error");

    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-collection", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        // var goodsInCartCount = $("#goods-in-cart-count");
        // var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var movie_id = $(this).data("movie-id");
        
        // Из атрибута href берем ссылку на контроллер django
        var add_to_collection_url = $(this).attr("href");
        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_collection_url,
            data: {
                movie_id: movie_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
                
                var movieContainer = $(".movie-container");
                movieContainer.html(data.button_add);

                var reviewForm = $(".review-form");
                reviewForm.html(data.review_form);
                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
                // cartCount++;
                // goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                // var cartItemsContainer = $("#cart-items-container");
                // cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении фильма в коллекцию");
            },
        });
    });

    $(document).on("click", ".delete-from-collection", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        var movie_id = $(this).data("movie-id");
        
        // Из атрибута href берем ссылку на контроллер django
        var delete_from_collection = $(this).attr("href");
        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: delete_from_collection,
            data: {
                movie_id: movie_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
                
                var movieContainer = $(".movie-container");
                movieContainer.html(data.button_add);

                var reviewForm = $(".review-form");
                reviewForm.html(data.review_form);

                var usersReviews = $(".reviews-list");
                usersReviews.html(data.users_reviews);

            },

            error: function (data) {
                console.log("Ошибка при удалении фильма из коллекции");
            },
        });
    });

    $(document).on("submit", ".add-review", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        var movie_id = $(this).data("movie-id-form");
        // console.log(movie_id);
        // Из атрибута href берем ссылку на контроллер django
        var url = $(this).attr("href");
        var formData = $(this).serialize();

        var review = $("[name=review]").val();
        var mark = $('input[name^="mark"]:checked').val();
        //var mark = $("[name=mark]").val();
        // var add_review = $(this).attr("href");
        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: url,
            data: {
                movie_id: movie_id,
                review: review,
                mark: mark,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
                
                var reviewForm = $(".review-form");
                reviewForm.html(data.review_handler);

                var usersReviews = $(".reviews-list");
                usersReviews.html(data.users_reviews);

            },

            error: function (data) {
                errorMessage.html(data.responseJSON.error);
                errorMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    errorMessage.fadeOut(400);
                }, 7000);
                // console.log("Отзыв или оценка уже есть");
            },
        });
    });

    $(document).ready(function () {
        $('.star-radio').on('click', function () {
            // Получаем индекс текущей звезды, к которой кликнули
            var index = $(this).prevAll('input').length; 
                
            // Убираем класс 'selected' с всех радиокнопок
            $('input[name^="mark"]').removeClass('selected');

            // Устанавливаем радиокнопку как выбранную
            $(this).addClass('selected');
        });
    });    

    $(document).on("click", ".remove-review", function (e) {
        e.preventDefault();

        var movie_id = $(this).data("movie-id");
        // console.log(movie_id);
        // Из атрибута href берем ссылку на контроллер django
        var url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: url,
            data: {
                movie_id: movie_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
                
                var usersReviews = $(".reviews-list");
                usersReviews.html(data.users_reviews);

                var formReview = $(".review-form");
                formReview.html(data.review_handler);
                // console.log(data.review_handler);
            },

            error: function (data) {
                errorMessage.html(data.responseJSON.error);
                errorMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    errorMessage.fadeOut(400);
                }, 7000);
                // console.log("Отзыв или оценка уже есть");
            },
        });
    });

    $(document).on("click", ".pay-sub", function (e) {
        e.preventDefault();

        var url = $(this).data("url");
        var level_sub = $(this).data("level-sub");
        console.log(level_sub);
        $.ajax({
            type: "POST",
            url: url,
            data: {
                level_sub: level_sub,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                setTimeout(function () {
                    window.location.href=data.redirect_url;
                }, 5);
            },
            error: function () {
            },
        });
    });
    
    $(document).on("click", ".pay-subscription", function (e) {
        e.preventDefault();

        var url = this.dataset.controllerUrl;
        var level_sub = $(this).data("level-subscription");
        $.ajax({
            type: "POST",
            url: url,
            data: {
                level: level_sub,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 5000);
                
                setTimeout(function () {
                    window.location.href=data.redirect_url;
                }, 5000);
            },
            error: function (data) {
                errorMessage.html(data.responseJSON.error);
                errorMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    window.location.href=data.responseJSON.redirect_url;
                }, 2000);
                // console.log("Отзыв или оценка уже есть");
            },
        });
    });
    // Ловим собыитие клика по кнопке удалить товар из корзины
   /* $(document).on("click", ".remove-from-cart", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Берем элемент счетчика в значке корзины и берем оттуда значение
        var goodsInCartCount = $("#goods-in-cart-count");
        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id корзины из атрибута data-cart-id
        var cart_id = $(this).data("cart-id");
        // Из атрибута href берем ссылку на контроллер django
        var remove_from_cart = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({

            type: "POST",
            url: remove_from_cart,
            data: {
                cart_id: cart_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Уменьшаем количество товаров в корзине (отрисовка)
                cartCount -= data.quantity_deleted;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });




    // Теперь + - количества товара 
    // Обработчик события для уменьшения значения
    $(document).on("click", ".decrement", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());
        // Если количества больше одного, то только тогда делаем -1
        if (currentValue > 1) {
            $input.val(currentValue - 1);
            // Запускаем функцию определенную ниже
            // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
            updateCart(cartID, currentValue - 1, -1, url);
        }
    });

    // Обработчик события для увеличения значения
    $(document).on("click", ".increment", function () {
        // Берем ссылку на контроллер django из атрибута data-cart-change-url
        var url = $(this).data("cart-change-url");
        // Берем id корзины из атрибута data-cart-id
        var cartID = $(this).data("cart-id");
        // Ищем ближайшеий input с количеством 
        var $input = $(this).closest('.input-group').find('.number');
        // Берем значение количества товара
        var currentValue = parseInt($input.val());

        $input.val(currentValue + 1);

        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue + 1, 1, url);
    });

    function updateCart(cartID, quantity, change, url) {
        $.ajax({
            type: "POST",
            url: url,
            data: {
                cart_id: cartID,
                quantity: quantity,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },

            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Изменяем количество товаров в корзине
                var goodsInCartCount = $("#goods-in-cart-count");
                var cartCount = parseInt(goodsInCartCount.text() || 0);
                cartCount += change;
                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            },
            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    }
*/
    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 7 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.fadeOut(500);
        }, 7000);
    }
/*
    // При клике по значку корзины открываем всплывающее(модальное) окно
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    // Собыите клик по кнопке закрыть окна корзины
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });

    // Обработчик события радиокнопки выбора способа доставки
    $("input[name='requires_delivery']").change(function () {
        var selectedValue = $(this).val();
        // Скрываем или отображаем input ввода адреса доставки
        if (selectedValue === "1") {
            $("#deliveryAddressField").show();
        } else {
            $("#deliveryAddressField").hide();
        }
    });

    // Форматирования ввода номера телефона в форме (xxx) xxx-хххx
    document.getElementById('id_phone_number').addEventListener('input', function (e) {
        var x = e.target.value.replace(/\D/g, '').match(/(\d{0,3})(\d{0,3})(\d{0,4})/);
        e.target.value = !x[2] ? x[1] : '(' + x[1] + ') ' + x[2] + (x[3] ? '-' + x[3] : '');
    });

    // Проверяем на стороне клинта коррекность номера телефона в форме xxx-xxx-хх-хx
    $('#create_order_form').on('submit', function (event) {
        var phoneNumber = $('#id_phone_number').val();
        var regex = /^\(\d{3}\) \d{3}-\d{4}$/;

        if (!regex.test(phoneNumber)) {
            $('#phone_number_error').show();
            event.preventDefault();
        } else {
            $('#phone_number_error').hide();

            // Очистка номера телефона от скобок и тире перед отправкой формы
            var cleanedPhoneNumber = phoneNumber.replace(/[()\-\s]/g, '');
            $('#id_phone_number').val(cleanedPhoneNumber);
        }
    });*/
});