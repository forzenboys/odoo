odoo.define('form_extend', function (require) {
    "use strict";
    var ajax = require('web.ajax');
    var FormController = require('web.FormController');
    var FormRenderer = require('web.FormRenderer');

    //
    var data = []
    var value = []
    var click_hostid
    var click_name
    var controller;
    var renderer;


    var search_renderer_cpu = function () {
         //获取点击时的name ，id
                click_hostid = renderer.state.data.host_id
                click_name  =renderer.state.data.name
            //
        var ctx =renderer.state.getContext();
        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'zabbix_item_data',
            method: 'search_read',
            args: [],
            kwargs: {
                domain: [['hostid','=',click_hostid],['name','=','CPU']],
                order: 'id asc',  /* 正序倒序 */
                fields:[],/* 需要的数据筛选 */
                context: ctx
            }
            }).then(function (respdata) {
                var msg = []
                if (respdata.length > 0) {
                    for (var i = 0 ; i<respdata.length;i++){
                        var ms_time = respdata[i].clock * 1000 //时间戳处理
                        msg.push(parseInt(ms_time))
                        msg.push(parseFloat(respdata[i].value_avg))
                        value.push(parseInt(respdata[i].value_avg))
                        data.push(msg)
                        msg = []
                    }
                }
                cpu()
                data = []
                value = []
            });

    };
    var search_renderer_neicun = function () {
         //获取点击时的name ，id
                click_hostid = renderer.state.data.host_id
                click_name  =renderer.state.data.name
            //
        var ctx =renderer.state.getContext();
        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'zabbix_item_data',
            method: 'search_read',
            args: [],
            kwargs: {
                domain: [['hostid','=',click_hostid],['name','=','内存']],
                order: 'id asc',  /* 正序倒序 */
                fields:[],/* 需要的数据筛选 */
                context: ctx
            }
            }).then(function (respdata) {
                var msg = []
                if (respdata.length > 0) {
                    for (var i = 0 ; i<respdata.length;i++){
                        var ms_time = respdata[i].clock * 1000 //时间戳处理
                        msg.push(parseInt(ms_time))
                        msg.push(parseFloat(respdata[i].value_avg))
                        value.push(parseInt(respdata[i].value_avg))
                        data.push(msg)
                        msg = []
                    }
                }
                neicun()
                data = []
                value = []
            });

    };

    var search_renderer_icmp = function () {
         //获取点击时的name ，id
                click_hostid = renderer.state.data.host_id
                click_name  =renderer.state.data.name
            //
        var ctx =renderer.state.getContext();
        ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'zabbix_item_data',
            method: 'search_read',
            args: [],
            kwargs: {
                domain: [['hostid','=',click_hostid],['name','=','ICMP']],
                order: 'id asc',  /* 正序倒序 */
                fields:[],/* 需要的数据筛选 */
                context: ctx
            }
            }).then(function (respdata) {
                var msg = []
                if (respdata.length > 0) {
                    for (var i = 0 ; i<respdata.length;i++){
                        var ms_time = respdata[i].clock * 1000 //时间戳处理
                        msg.push(parseInt(ms_time))
                        msg.push(parseFloat(respdata[i].value_avg))
                        value.push(parseInt(respdata[i].value_avg))
                        data.push(msg)
                        msg = []
                    }
                }
                icmp()
                jiekou()
                data = []
                value = []
            });

    };
    FormController.include({
        renderPager: function () {
            controller=this;
            return this._super.apply(this, arguments);

        }
    });

 //
    FormRenderer.include({
        _renderView: function () {
            renderer=this;
            var result = this._super.apply(this, arguments);
            if (this.state.model == 'zabbix_host') {
                renderer.$el.children('div').children('div').after(`<h2 style="text-align: center;font-family: cursive">数据展示</h2>`)
                renderer.$el.children('div').children('div').after(`<hr style="border-top:1px solid rgba(0, 0, 0, 0.3)"/>`)
                renderer.$el.children('div').children('h2').after(`
                                                 <div class="king-container clearfix">
                                                    <div class="container-fluid mb0 ">
                                                        <div class="row row1" style="padding-left: 8.5%;">
                                                        </div>
                                                    </div>
                                                    <div class="container-fluid mb0 " style="padding-top: 20px">
                                                        <div class="row row2" style="padding-left: 8.5%">
                                                        </div>
                                                    </div>
                                                </div>`)
                var bootstrp_one = renderer.$el.children('div').children('div.king-container').children('div.container-fluid').children('div.row1')
                var bootstrp_two = renderer.$el.children('div').children('div.king-container').children('div.container-fluid').children('div.row2')
                bootstrp_one.append(`<div id="container" class="col-md-6" style="max-width:800px;height:400px;padding-top: 10px"></div>`)
                bootstrp_one.append(`<div id="container1" class="col-md-6" style="max-width:800px;height:400px;padding-top: 10px"></div>`)
                bootstrp_two.append(`<div id="container2" class="col-md-6" style="max-width:800px;height:400px;padding-top: 10px"></div>`)
                bootstrp_two.append(`<div id="container3" class="col-md-6"  style="max-width:800px;height:400px;padding-top: 10px"></div>`)
                search_renderer_cpu();
                search_renderer_neicun();
                search_renderer_icmp();

            } else {
                this.getParent().$('.o_list_view_categ').remove();
            }
            return result;
        }
    });
      var cpu = function (){
        Highcharts.stockChart('container', {

                    chart: {
                        backgroundColor: '#ffffff',
                        borderRadius:'2em',
                        },
                    credits: {
                        enabled: false
	                    },
                        rangeSelector: {
                            selected: 2
                        },
                        plotOptions: {
                            series: {
                                showInLegend: true
                            }
                        },
                        lang: {
                            noData: '暂无数据,请先关联'
                        },
                        noData:{
                            style:{
                                fontSize:'20px'
                            }
                        },
                        subtitle: {
		                    text: '设备名称 ----- '+ click_name
	                    },
                        title:{
                            text:'cpu数据',
                            style:{
                                fontFamily:'cursive',
                                fontWeight:'bold'
                }
                        },
                        tooltip: {
                        headerFormat: '<small>{point.key}</small><table>',
                            split: false,
                            shared: true
                        },
                        navigation: {
                            buttonOptions: {
                                enabled: true
                            }
                        },

                        yAxis: {
                            title: {
                                text: ''
                            },
                            labels: {//y轴刻度文字标签
                                formatter: function () {
                                    return this.value + '%';//y轴加上%
                                }
                            },
                            plotLines: [{//区域划分线，0刻度
                                value: 0,
                                width: 1,
                                color: '#3582d9'
                            }]
                        },
                        series: [{
                            // type: 'line',
                            id: '000001',
                            name: click_name,
                            data: data,
                            zones: [{
                                value: 50,
                                color: '#009125',
                              }, {
                                value: 80,
                                color: '#fffc2e'
                              }, {
                                color: '#ff3e3e' // 这里设置的颜色会覆盖掉 series 中设置的颜色 'green',最终大于0部分显示为 'red'
                              }]
                        }]
                    });

    };
    var neicun = function(){
                    Highcharts.stockChart('container1', {
                    chart: {
                        backgroundColor: '#ffffff',
                        borderRadius:'2em',

                        },
                    credits: {
                        enabled: false
	                    },
                        rangeSelector: {
                            selected: 2
                        },
                        plotOptions: {
                            series: {
                                showInLegend: true
                            }
                        },
                        title:{
                            text:'内存数据',
                            style:{
                                fontFamily:'cursive',
                                fontWeight:'bold'
                            }
                        },
                        subtitle: {
		                    text: '设备名称 ----- '+ click_name
	                    },
                        yAxis: {
                            title: {
                                text: ''
                            },
                            labels: {//y轴刻度文字标签
                                formatter: function () {
                                    return this.value + '%';//y轴加上%
                                }
                            },
                            plotLines: [{//区域划分线，0刻度
                                value: 0,
                                width: 1,
                                color: '#3582d9'
                            }]
                        },
                        lang: {
                            noData: '暂无数据,请先关联'
                        },
                        noData:{
                            style:{
                                fontSize:'20px'
                            }
                        },
                        tooltip: {
                            split: false,
                            shared: false
                        },
                        navigation: {
                            buttonOptions: {
                                enabled: false
                            }
                        },
                        series: [{
                            // type: 'line',
                            id: '000001',
                            name: click_name,
                            data: data,
                            zones: [{
                                value: 50,
                                color: '#009125',
                              }, {
                                value: 80,
                                color: '#fffc2e'
                              }, {
                                color: '#ff3e3e' // 这里设置的颜色会覆盖掉 series 中设置的颜色 'green',最终大于0部分显示为 'red'
                              }]
                        }]
                    });

    };

    var jiekou = function(){
                    Highcharts.stockChart('container2', {
                    chart: {
                        backgroundColor: '#ffffff',
                        borderRadius:'2em',

                        },
                    credits: {
                        enabled: false
	                    },
                        rangeSelector: {
                            selected: 2
                        },
                        plotOptions: {
                            series: {
                                showInLegend: true
                            }
                        },
                        title:{
                            text:'接口数据',
                            style:{
                                fontFamily:'cursive',
                                fontWeight:'bold'
                            }
                        },
                        subtitle: {
		                    text: '设备名称 ----- '+ click_name
	                    },
                        yAxis: {
                            title: {
                                text: ''
                            },
                            labels: {//y轴刻度文字标签
                                formatter: function () {
                                    return this.value + '%';//y轴加上%
                                }
                            },
                            plotLines: [{//区域划分线，0刻度
                                value: 0,
                                width: 1,
                                color: '#3582d9'
                            }]
                        },
                        lang: {
                            noData: '暂无数据,请先关联',
                        },
                        noData:{
                            style:{
                                fontSize:'20px'
                            }
                        },
                        tooltip: {
                            split: false,
                            shared: false
                        },
                        navigation: {
                            buttonOptions: {
                                enabled: false
                            }
                        },
                        series: [{
                            // type: 'line',
                            id: '000001',
                            name: '',
                            data: [],
                            zones: [{
                                value: 50,
                                color: '#009125',
                              }, {
                                value: 80,
                                color: '#fffc2e'
                              }, {
                                color: '#ff3e3e' // 这里设置的颜色会覆盖掉 series 中设置的颜色 'green',最终大于0部分显示为 'red'
                              }]
                        }]
                    });

    };
    var icmp = function(){
                    Highcharts.stockChart('container3', {
                    chart: {
                        backgroundColor: '#ffffff',
                        borderRadius:'2em',

                        },
                        colors:[
                          '#314555'
                        ],
                    credits: {
                        enabled: false
	                    },
                        rangeSelector: {
                            selected: 2
                        },
                        plotOptions: {
                            series: {
                                showInLegend: true
                            }
                        },
                        title:{
                            text:'icmp延迟数据',
                            style:{
                                fontFamily:'cursive',
                                fontWeight:'bold'
                            }
                        },
                        subtitle: {
		                    text: '设备名称 ----- '+ click_name
	                    },
                        yAxis: {
                            title: {
                                text: ''
                            },
                            labels: {//y轴刻度文字标签
                                // formatter: function () {
                                //     return this.value + '%';//y轴加上%
                                // }
                            },
                            plotLines: [{//区域划分线，0刻度
                                value: 0,
                                width: 1,
                                color: '#3582d9'
                            }]
                        },
                        lang: {
                            noData: '暂无数据,请先关联'
                        },
                        noData:{
                            style:{
                                fontSize:'20px'
                            }
                        },
                        tooltip: {
                            split: false,
                            shared: false
                        },
                        navigation: {
                            buttonOptions: {
                                enabled: false
                            }
                        },
                        series: [{
                            // type: 'line',
                            id: '000001',
                            name: click_name,
                            data: data,
                        }]
                    });

    }
});
