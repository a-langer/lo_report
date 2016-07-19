// инициализация chosen http://jsfiddle.net/emamut/CBjmj/4/

    var config = {
      // конфигурируем настройку для своего списка chosen-cft
      '.chosen-cft'              : { no_results_text: "Такая схема не предусмотрена!",
                                     //allow_single_deselect: true, // пиктограмма "удалить"
                                     width:"100%" // заполнять все по ширине
                                   },
      '.chosen-select'           : {},
      '.chosen-select-deselect'  : {allow_single_deselect:true},
      '.chosen-select-no-single' : {disable_search_threshold:10},
      '.chosen-select-no-results': {no_results_text:'No result match'},
      '.chosen-select-width'     : {width:"95%"}
    }
    for (var selector in config) {
      $(selector).chosen(config[selector]);
    }