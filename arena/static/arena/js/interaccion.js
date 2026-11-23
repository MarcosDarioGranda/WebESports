$(function () {

  //EFECTOS
  $('#lista').hide().fadeIn(400);
  $('.tarjetas li').hide().fadeIn(600);

  //EVENTO input
  var $buscador = $('#buscador');
  var $items = $('#lista > li');
  var $contador = $('#contador');

  function filtrar() {
    var texto = $buscador.val().trim().toLowerCase();
    var visibles = 0;

    $items.each(function () {
      // solo el texto de los enlaces directos del elemento
      var contenido = $(this).children('a').text().toLowerCase();
      var coincide = contenido.indexOf(texto) !== -1;
      $(this).toggle(coincide);
      if (coincide) {
        visibles++;
      }
    });

    $contador.text(visibles + ' de ' + $items.length + ' resultados');
  }

  if ($buscador.length) {
    $buscador.on('input', filtrar);
    filtrar();
  }

  //EVENTO click + AJAX
  $('#lista').on('click', '.ver-equipos', function () {
    var $boton = $(this);
    var $panel = $boton.siblings('.equipos-ajax');

    //Si ya está abierto, se cierra
    if ($panel.is(':visible')) {
      $panel.slideUp();
      $boton.text('Ver equipos');
      return;
    }

    //Si ya se cargó antes, solo se vuelve a abrir
    if ($panel.children().length > 0) {
      $panel.slideDown();
      $boton.text('Ocultar equipos');
      return;
    }

    //Primera vez: petición AJAX al servidor
    $boton.text('Cargando...');
    $.getJSON($boton.data('url'))
      .done(function (datos) {
        $.each(datos.equipos, function (i, equipo) {
          var $enlace = $('<a>').attr('href', equipo.url).text(equipo.nombre);
          $panel.append($('<li>').append($enlace));
        });
        if (datos.equipos.length === 0) {
          $panel.append($('<li>').text('Sin equipos.'));
        }
        $panel.slideDown();
        $boton.text('Ocultar equipos');
      })
      .fail(function () {
        $boton.text('Ver equipos');
        alert('No se pudieron cargar los equipos.');
      });
  });

});