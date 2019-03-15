var bIsChinese = true; // 是否是中文
var vm = new Vue({
    el: ".wrap-body",
    data: {
        host,
        sEmail_address,
        sPhone_number,
        movie_list: {},
        cate_list: [],
        cate_select_id: 'all',
        click_rank_list: [],
        tags_list: [],
        evaluate_movie_list: [],
        movie_list_news: [],
        friend_links_list_1: [],
        friend_links_list_2: [],
        movie_detail: {},
        evaluate_detail: '',
        cates_post_list: [],
        post_related_movie_page: 1,
        post_related_movie_list: []

    },
    methods: {
        // 获取 电影推荐的列表
        get_movie_related: function (page) {
            parms = this.cates_post_list.join('-');
            axios.get(this.host + '/realtedmovie/cateid=' + parms + '/' + '?page=' + page, {
                responseType: 'json'
            })
                .then(response => {
                    //处理数据
                    m = response.data['results'];
                    for (var i = 0; i < m.length; i++) {
                        m[i]['m_detail_url'] = 'single.html?mv=' + m[i]['id']
                    }
                    this.post_related_movie_list=m;
                    this.post_related_movie_page = 1 + this.post_related_movie_page;
                })
                .catch(error => {
                    this.get_movie_related(1);
                });
        },
        // 获取 网址的参数的方法
        getUrlParam: function (name) {
            var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)"); //构造一个含有目标参数的正则表达式对象
            var r = window.location.search.substr(1).match(reg);  //匹配目标参数
            if (r != null) {
                return unescape(r[2]);
            } else {
                return null;
            }  //返回参数值
        },
        // 获取 电影详情页

        get_movie_detail: function () {
            id = this.getUrlParam('mv');
            axios.get(this.host + '/movies/' + id + '/', {
                responseType: 'json'
            })
                .then(response => {
                    this.movie_detail = response.data;
                    this.evaluate_detail = 'images/star' + Math.round(this.movie_detail['mevaluate']) + '.png';

                    for (var i = 0; i < this.movie_detail['categorys'].length; i++) {
                        this.cates_post_list.push(this.movie_detail['categorys'][i]['cate_id'])
                    }
                    this.get_movie_related(1)

                })
                .catch(error => {
                    alert(error.response.data);
                });

        },
        // 获取友情链接
        get_friend_links: function () {
            axios.get(this.host + '/friendlink/', {
                responseType: 'json'
            })
                .then(response => {
                    // console.log(response.data.length);
                    for (var i = 0; i < response.data.length; i++) {
                        if (i > (response.data.length / 2 - 1)) {
                            this.friend_links_list_1.push(response.data[i])
                        } else {
                            this.friend_links_list_2.push(response.data[i])

                        }
                    }
                    // 为 图片添加 详情页面的网址
                    // this.cate_list = response.data;
                    // console.log(response.data)
                })
                .catch(error => {
                    alert(error.response.data);
                });
        },
        // 近日更新 逻辑
        get_movie_by_create_time: function () {

            axios.get(this.host + '/movies/?page=' + 1, {
                responseType: 'json'
            })
                .then(response => {
                    // 为 图片添加 详情页面的网址
                    m = response.data['results'].slice(0, 3);
                    for (var i = 0; i < m.length; i++) {
                        m[i]['m_detail_url'] = 'single.html?mv=' + m[i]['id'];
                        m[i]['m_evaluate_image'] = 'images/star' + Math.round(m[i]['mevaluate']) + '.png';
                    }
                    this.movie_list_news = m;

                    // console.log(this.movie_list)
                })
                .catch(error => {
                    alert(error.response.data);
                });


        },
        // 获取 评价排行 电影列表
        get_evaluate_movie_list: function () {
            axios.get(this.host + '/evaluate/', {
                responseType: 'json'
            })
                .then(response => {
                    // 为 图片添加 详情页面的网址
                    m = response.data['results'];
                    for (var i = 0; i < m.length; i++) {
                        m[i]['m_detail_url'] = 'single.html?mv=' + m[i]['id'];
                        m[i]['m_evaluate_image'] = 'images/star' + Math.round(m[i]['mevaluate']) + '.png';
                    }
                    this.evaluate_movie_list = m;
                })
                .catch(error => {
                    alert(error.response.data);
                });
        },
        // 设置 种类id
        set_cate_id: function (n) {
            // 设置cate_select_id 为 标签的id
            this.cate_select_id = n;
            this.get_cate_movie();
        },
        // 请求 标签
        get_tags_list: function () {
            axios.get(this.host + '/tags/', {
                responseType: 'json'
            })
                .then(response => {
                    // 为 图片添加 详情页面的网址
                    this.tags_list = response.data;
                    // console.log(this.tags_list)
                })
                .catch(error => {
                    alert(error.response.data);
                });
        },
        // 请求 点击排行
        get_click_rank_movie: function () {
            axios.get(this.host + '/clickrank/', {
                responseType: 'json'
            })
                .then(response => {
                    // 为 图片添加 详情页面的网址
                    m = response.data['results'];
                    for (var i = 0; i < m.length; i++) {
                        m[i]['m_detail_url'] = 'single.html?mv=' + m[i]['id']
                    }
                    this.click_rank_list = m;
                    // console.log(this.click_rank_list)
                })
                .catch(error => {
                    alert(error.response.data);
                });
            // 刷新 详情页网址
        },
        // 处理 json
        dispose_movie_list: function (data) {
            m = data;
            for (var i = 0; i < m.length; i++) {
                m[i]['m_detail_url'] = 'single.html?mv=' + m[i]['id']
            }

            this.movie_list = [];
            for (var i = 0; i < 10; i++) {
                if ((i + 1) * 4 < m.length) {
                    this.movie_list['movie_list_' + i] = m.slice(4 * i, 4 * (i + 1));
                } else {
                    this.movie_list['movie_list_' + i] = m.slice(4 * i, m.length);
                }
            }

            // console.log(m)
        },

        fLanguageChange: function () {
            bIsChinese = !(bIsChinese);
            $('.language_select').html(bIsChinese ? '语言选择' : 'Language');
            $('.home_title').html(bIsChinese ? '首 页' : 'HOME');
            $('.contact_title').html(bIsChinese ? '留 言' : 'CONTACT');
            $('.submit_title').val(bIsChinese ? '搜  索' : 'Submit');
            $('#search_button').html(bIsChinese ? '查  询' : 'Search');
            $('.title_title').html(bIsChinese ? '电 影' : 'MOVIE');
            $('.Click_Rank').html(bIsChinese ? '点 击 排 行' : 'Click Rank !');
            $('.tag_title').html(bIsChinese ? '标 签' : 'Tags');
            $('.mark_rank_title').html(bIsChinese ? '评 分 排 行' : 'Mark Rank');
            $('.last_update_title').html(bIsChinese ? '近 日 更 新' : 'Lastest Updates');
            $('.subject_title').html(bIsChinese ? '专 题' : 'SUBJECT');
            $('.area_title').html(bIsChinese ? '地 区' : 'AREA');
            $('.praise_title').html(bIsChinese ? '高 分 电 影' : 'PRAISE FILMs');
            $('.chinese_movie').html(bIsChinese ? '内 陆 电 影' : 'INLAND FILMs');
            $('.occident_movie').html(bIsChinese ? '欧 美 电 影' : 'OCCIDENT FILMs');
            $('.Japan_Korea_movie').html(bIsChinese ? '日 韩 电 影' : 'Japan Korea FILMs');
            $('.related_post_title').html(bIsChinese ? '相 关 推 荐' : 'Related Post');

        },

        get_movie_list: function (page) {
            axios.get(this.host + '/movies/?page=' + page, {
                responseType: 'json'
            })
                .then(response => {
                    // 为 图片添加 详情页面的网址
                    m = response.data['results'];
                    this.dispose_movie_list(m)

                    // console.log(this.movie_list)
                })
                .catch(error => {
                    alert(error.response.data);
                });
            // 刷新 详情页网址
        },

        // 获取 展示在前端的电影种类
        get_cates_list: function () {
            axios.get(this.host + '/cates/', {
                responseType: 'json'
            })
                .then(response => {
                    // 为 图片添加 详情页面的网址
                    this.cate_list = response.data;
                    // console.log(this.cate_list)
                })
                .catch(error => {
                    alert(error.response.data);
                });
        },

        // 获取一类电影
        get_cate_movie: function () {
            cate_id = this.cate_select_id;
            if (cate_id != 'all') {


                axios.get(this.host + '/cates/' + cate_id + '/', {
                    responseType: 'json'
                })
                    .then(response => {
                        // 为 图片添加 详情页面的网址
                        m = response.data['results'];
                        this.dispose_movie_list(m)

                        console.log(m)
                    })
                    .catch(error => {
                        alert(error.response.data);
                    });


            } else {
                location.reload()
            }
        }
    },


    mounted: function () {
        $('.email_address').html(sEmail_address);
        $('.phone_number').html(sPhone_number);
        this.get_movie_list(1);
        this.get_cates_list();
        this.get_click_rank_movie();
        this.get_tags_list();
        this.get_evaluate_movie_list();
        this.get_movie_by_create_time();
        this.get_friend_links();
        this.get_movie_detail();
    }


});