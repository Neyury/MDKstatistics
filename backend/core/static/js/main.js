'use strict;'
var chart = c3.generate({
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
