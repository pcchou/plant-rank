var state = 0;
$('#algotext').css('font-weight', 'bold');
$('h1').on('click touch touchstart', function () {
  switch (state) {
    case 0:
      $('#algotext').css('font-weight', '');
      $('#algotable').toggle();
      $('#algocounttext').css('font-weight', 'bold');
      $('#algocounttable').toggle();
      state++;
      break;
    case 1:
      $('#algocounttext').css('font-weight', '');
      $('#algocounttable').toggle();
      $('#counttext').css('font-weight', 'bold');
      $('#counttable').toggle();
      state++;
      break;
    case 2:
      $('#counttext').css('font-weight', '');
      $('#counttable').toggle();
      $('#algotext').css('font-weight', 'bold');
      $('#algotable').toggle();
      state = 0;
      break;
  }
})
