'use strict';





function toggleClass(event, n, class_name="open") {
  var target = event.currentTarget;

  for (var i = 0; i < n - 1; i++) {
    target = target.parentNode;
  }

  target.classList.toggle(class_name);

  return target;
}

// https://api.vk.com/method/wall.getById?posts=-1_340393&v=5.63
function GET(url, data='') {
  return new Promise(function(resolve, reject) {
    var params = ''
    if(data){
        params += '?'
        for(var i = 0; i < data.length; i++){
            params += `post=${data[i]}&`
        }
    }
    var xhr = new XMLHttpRequest();
    xhr.open('GET', `${url}` + params, true);

    xhr.onload = function() {
      if (this.status == 200) {
        resolve(this.response);
      } else {
        var error = new Error(this.statusText);
        error.code = this.status;
        reject(error);
      }
    };

    xhr.onerror = function() {
      reject(new Error("Network Error"));
    };

    xhr.send(data);
  });
}



Vue.component('post-item', {
  props: ['post', 'statistics'],
  template: '\
    <div class="post">\
      <div class="post__head" >\
        <ul class="post__meta">\
          <li><span>id</span>{{post.id}}</li>\
          <li>{{datetime_for_humans}}</li>\
        </ul>\
\
        <ul class="post__info">\
          <li title="Лайки">\
            <span><svg class="icon"  ><use  xlink:href="#ei-heart-icon"></use></svg></span>\
          </li>\
          <li title="Комментарии">\
            <span><svg class="icon"  ><use  xlink:href="#ei-comment-icon"></use></svg></span>\
          </li>\
          <li title="репосты">\
            <span><svg class="icon"  ><use  xlink:href="#ei-external-link-icon"></use></svg></span>\
          </li>\
          <li title="Просмотры">\
            <span><svg class="icon"  ><use  xlink:href="#ei-eye-icon"></use></svg></span>\
          </li>\
        </ul>\
      </div>\
      <div class="post__content">\
        <div class="post__text">{{response}}<div class="toggle" onclick="toggleClass(event, 2)"><svg class="icon"  ><use  xlink:href="#ei-chevron-down-icon"></use></svg></div>\
        \
        </div>\
        <div class="post__chart" >\
          <div :id="`chart_`+post.id"></div>\
        </div>\
      </div>\
    </div>\
  ',
  computed: {
    datetime_for_humans: function () {
      var date = new Date(this.post.date*1000);
      var options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
      };
      return date.toLocaleString("ru", options);
    },
      response: function () {
        for(var i = 0; i < this.statistics.length; i++){
          if(this.statistics[i].id == this.post.id){
              return this.statistics[i]
          }
        }
      }
  },
  mounted: function () {
    this.post.chart = c3.generate({
      bindto: `#chart_${this.post.id}`,
      data: {
          columns: [
              ['Лайки', ],
              ['Комментарии',],
              ['репосты', ]
          ],
      }
      });
  },
  updated: function () {
      for(var i = 0; i < this.statistics.length; i++){
          if(this.statistics[i].id == this.post.id){
              this.post.chart.load({
                  columns: [
                      this.statistics[i].data[1],
                      this.statistics[i].data[2],
                      this.statistics[i].data[3]
                  ]
              });
          }
      }
  }
});

var content = new Vue({
  el: '#content',
  data: {
    list_posts: [],
    statistics: []
  },
    methods: {
        load_posts: function (event) {
            var post_id = this.list_posts[this.list_posts.length - 1].id
            GET('/board/posts', [post_id]).then(
                function (response) {
                    content.list_posts = content.list_posts.concat(JSON.parse(response))
                },
                function (error) {

                }
            )
        }
    }
});





GET('/board/posts').then(
    function (response) {
        content.list_posts = content.list_posts.concat(JSON.parse(response))
    },
    function (error) {

    }
);

// GET('statistics').then(
//     function (response) {
//     },
//     function (error) {
//
//     }
// );





setInterval(function() {
  GET('/board/statistics', [12823762, 12823335, 12822879]).then(
        function (response) {
            console.log('good');
            content.statistics = JSON.parse(response)
        },
        function (error) {
            console.log('error')
        }
    );
}, 3000);



















//
