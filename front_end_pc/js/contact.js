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

    },
    methods: {
        onSubmit: function () {
            axios.get(this.host + '/contact/?name=' + $('#name').val() + '&email=' + $('#email').val() + '&message=' + $('#message').val()+'/', {
                responseType: 'json'
            })
                .then(response => {
                    // console.log(response.data)
                    alert(response.data['message']);
                    location.reload()
                })
                .catch(error => {
                    alert('发送失败,请检查您的输入或者网络!');
                });

        },
        // 获取友情链接
        get_friend_links: function () {
            axios.get(this.host + '/friendlink/', {
                responseType: 'json'
            })
                .then(response => {
                    console.log(response.data.length);
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
            $('.sendButton').val(bIsChinese ? '提  交' : 'Submit');
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
            $('.contact_name_input').html(bIsChinese ? '请输入你的名字:' : 'Enter your name:');
            $('.contact_email_input').html(bIsChinese ? '请输入你的邮箱:' : 'Enter your email:');
            $('.contact_message_input').html(bIsChinese ? '请输入你的内容:' : 'Your message here:');

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
        // this.get_movie_list(1);
        this.get_click_rank_movie();
        // this.get_tags_list();
        this.get_evaluate_movie_list();
        // this.get_movie_by_create_time();
        this.get_friend_links();
    }


});