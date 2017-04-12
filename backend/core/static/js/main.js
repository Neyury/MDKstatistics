'use strict;'
var chart = c3.generate({
    bindto: '#chart',
    data: {
        columns: [
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 130, 100, 140, 200, 150, 50]
        ],
        type: 'spline'
    }
});
var chart2 = c3.generate({
    bindto: '#chart2',
    data: {
        columns: [
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 130, 100, 140, 200, 150, 50]
        ],
        type: 'spline'
    }
});
var chart3 = c3.generate({
    bindto: '#chart3',
    data: {
        columns: [
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 130, 100, 140, 200, 150, 50]
        ],
        type: 'spline'
    }
});
var chart4 = c3.generate({
    bindto: '#chart4',
    data: {
        columns: [
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 130, 100, 140, 200, 150, 50]
        ],
        type: 'spline'
    }
});
function toggleClass(event, n, class_= "open") {
  var target = event.currentTarget;

  for (var i = 0; i < n - 1; i++) {
    target = target.parentNode;
  }

  target.classList.toggle(class_);

  return target;
}
