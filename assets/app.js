var state = 0;
$('h1').on('click', function () {
  switch (state) {
    case 0:
      $('#algotable').toggle();
      $('#algocounttable').toggle();
      state++;
      break;
    case 1:
      $('#counttable').toggle();
      $('#algocounttable').toggle();
      state++;
      break;
    case 2:
      $('#counttable').toggle();
      $('#algotable').toggle();
      state = 0;
      break;
  }
})
