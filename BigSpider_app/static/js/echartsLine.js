var myChart = echarts.init(document.getElementById('polyline'));
		// 指定图表的配置项和数据

var option = {
    tooltip: {
        trigger: 'axis'
    },
    toolbox: {
        feature: {
            dataView: {show: true, readOnly: false},
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
        }
    },
    legend: {
        data:['主节点','从节点1','从节点2','总爬取量']
    },
    xAxis: [
        {
            type: 'category',
            data: ['周一','周二','周三','周四','周五','周六','周日']
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '节点爬取量',
            min: 0,
            max: 1000,
            interval: 100,
            axisLabel: {
                formatter: '{value} xx'
            }
        },
        {
            type: 'value',
            name: '总爬取量',
            min: 0,
            max: 5000,
            interval: 1000,
            axisLabel: {
                formatter: '{value} xx'
            }
        }
    ],
    series: [
        {
            name:'主节点',
            type:'bar',
            data:[20, 49, 70, 232, 256, 767, 135]
        },
        {
            name:'从节点1',
            type:'bar',
            data:[26, 59, 90, 264, 281, 70, 175]
        },
         {
            name:'从节点2',
            type:'bar',
            data:[26, 59, 90, 264, 287, 707, 175]
        },
        {
            name:'总爬取量',
            type:'line',
            yAxisIndex: 1,
            data:[2000, 2020, 3030, 4050, 4030, 4020, 3030]
        }
    ]
};

			// 使用刚指定的配置项和数据显示图表。
			myChart.setOption(option);
