'use strict';

// Компонент, описывающий пост и его поведение
Vue.component('post-item', {
    props: ['post', 'range'], // Входные параметры, передаваемые родительским vue компонентом (page0
    template: `

    <div class="post" :class="{ads: isAds}">
      <div class="post__head" >
        <ul class="post__meta">
          <li><span>id</span><a :href="'https://vk.com/mudakoff?w=wall'+post.owner_id + '_' + +post.id" target="blank_">{{post.id}}</a></li>
          <li>{{datetime_for_humans}}</li>
        </ul>

        <ul class="post__info">
          <li title="Лайки">
            <span><svg class="icon"><use xlink:href="#ei-heart-icon"></use></svg></span>{{ likes }}
          </li>
          <li title="Комментарии">
            <span><svg class="icon"><use xlink:href="#ei-comment-icon"></use></svg></span>{{ comments }}
          </li>
          <li title="репосты">
            <span><svg class="icon"><use xlink:href="#ei-external-link-icon"></use></svg></span>{{ reposts }}
          </li>
          <li title="Просмотры">
            <span><svg class="icon"><use xlink:href="#ei-eye-icon"></use></svg></span>{{ views }}
          </li>
        </ul>
      </div>
      <div class="post__content">
        <div class="post__chart" >
          <div :id="'chart-'+post.id"></div>
          <div class="modal loader" v-if="!post.statistics"></div>
        </div>
      </div>
    </div>
    `,
    computed: { // вычисляемые свойства
        datetime_for_humans: function() {
            let date = new Date(this.post.date * 1000);
            let options = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric'
            };
            return date.toLocaleString("ru", options);
        },
        likes: function() {
            if (this.post.statistics) {
                if (this.post.statistics[0]) {
                    return this.post.statistics[0].likes;
                }
            } else {
                return '';
            }
        },
        comments: function() {
            if (this.post.statistics) {
                if (this.post.statistics[0]) {
                    return this.post.statistics[0].comments;
                }
            } else {
                return '';
            }
        },
        reposts: function() {
            if (this.post.statistics) {
                if (this.post.statistics[0]) {
                    return this.post.statistics[0].reposts;
                }
            } else {
                return '';
            }
        },
        views: function() {
            if (this.post.statistics) {
                if (this.post.statistics[0]) {
                    return this.post.statistics[0].views;
                }
            } else {
                return '';
            }
        },
        isAds: function() {
            return this.post.marked_as_ads;
        }
    },
    mounted: function() { // вызывается при монтировании компонента в DOM
        this.post.chart = c3.generate({
            bindto: `#chart-${this.post.id}`,
            data: {
                x: 'date_unixtime',
                json: [],
            },
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        format: function(x) {
                            let date = new Date(x * 1000);
                            let options = {
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric',
                                hour: 'numeric',
                                minute: 'numeric',
                                second: 'numeric'
                            };
                            return date.toLocaleString("ru", options);
                        }
                    }
                }
            }
        });

    },
    updated: function() { // Вызывается при изменении связанных данных (post, переданный в props)
        if (this.post.statistics) {
            this.post.chart.load({
                json: this.post.statistics,
                keys: {
                    value: ['date_unixtime', 'likes', 'comments', 'reposts'],
                }
            });
        }
    }
});


// Корневой элемент
let page = new Vue({
    el: '#page',
    data: {
        posts: [], // список постов, на основе которых рендерятся компоненты post-item
        visible_posts: [], // список постов в поле видимости (для ограничения загружаемых данных)
        open_setting_menu: false,
        range: 'all',
        can_load_posts: true,
    },
    methods: {
        load_posts: function() { // Загрузка постов, вызывается при нажатии на "следующие посты"
            if (this.posts.length) {
                let post_id = this.posts[this.posts.length - 1].id;
                if (this.can_load_posts) {
                    GET('/board/posts', [post_id]).then(
                        function(response) {
                            page.posts = page.posts.concat(JSON.parse(response));
                            page.can_load_posts = true;
                        },
                        function(error) {

                        }
                    )
                }
            }
            this.can_load_posts = false;
        },
        update_visible_posts: function() { // обновляет список постов в области видимости
            let list = [];
            for (let i = 0; i < this.$children.length; i++) {
                let offset_size = 0;
                let coords = this.$children[i].$el.getBoundingClientRect();

                let windowHeight = document.documentElement.clientHeight;


                let topVisible = coords.top > -offset_size && coords.top < windowHeight + offset_size;
                let bottomVisible = coords.bottom < windowHeight + offset_size && coords.bottom > -offset_size;

                if (topVisible || bottomVisible) {
                    list.push(this.$children[i].post.id)
                }
            }
            this.visible_posts = list;
        }
    },
    updated: function() {
        this.update_visible_posts(); // обновление списка видимых постов при их добавлении в posts
    }
});


function GET(url, posts = '') {
    return new Promise(function(resolve, reject) {
        let params = `?range=${page.range}`;
        if (posts) {
            for (let i = 0; i < posts.length; i++) {
                params += `&post=${posts[i]}`
            }
        }
        let xhr = new XMLHttpRequest();
        xhr.open('GET', `${url}${params}`, true);

        xhr.onload = function() {
            if (this.status == 200) {
                resolve(this.response);
            } else {
                let error = new Error(this.statusText);
                error.code = this.status;
                reject(error);
            }
        };

        xhr.onerror = function() {
            reject(new Error("Network Error"));
        };

        xhr.send();
    });
}

// Первоначальная загрузка постов
GET('/board/posts').then(
    function(response) {
        page.posts = page.posts.concat(JSON.parse(response));
    },
    function(error) {
        alert('Ошибка загрузки ленты')
    }
);


// Обнавление данных для постов в поле видисоти
setInterval(function() {
    let list = page.visible_posts;

    GET('/board/statistics', list).then(
        function(response) {
            let statistics = JSON.parse(response);

            if (statistics) {
                for (let i = 0; i < page.posts.length; i++) {
                    for (let j = 0; j < statistics.length; j++) {
                        if (page.posts[i].id == statistics[j].id) {
                            Vue.set(page.posts[i], 'statistics', statistics[j].data)
                        }
                    }
                }
            }
        },
        function(error) {
            console.log('Ошибка загрузки данных');
        }
    );
}, 1000);

// Обновлять список видимых постов при скроле
window.onscroll = function() {
    page.update_visible_posts();
};