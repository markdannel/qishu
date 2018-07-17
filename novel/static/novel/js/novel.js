$(function () {
    var cssURL = '<link rel="shortcut icon" type="image/png" href="/static/favicon.ico">'
    // 请看清楚，是动态将link标签添加到head里   
    $($('head')[0]).append(cssURL);
})

$('#chapterTab a').click(function (e) {
    e.preventDefault()
    $(this).tab('show')
})

String.prototype.format = function (args) {
    var result = this;
    if (arguments.length > 0) {
        if (arguments.length == 1 && typeof (args) == "object") {
            for (var key in args) {
                if (args[key] != undefined) {
                    var reg = new RegExp("({" + key + "})", "g");
                    result = result.replace(reg, args[key]);
                }
            }
        }
        else {
            for (var i = 0; i < arguments.length; i++) {
                if (arguments[i] != undefined) {
                    var reg = new RegExp("({)" + i + "(})", "g");
                    result = result.replace(reg, arguments[i]);
                }
            }
        }
    }
    return result;
}
Date.prototype.Format = function (fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

function myajax(url, param, csrftoken, callback) {
    jQuery.ajax({
        url: url,
        type: "POST",
        data: param,
        contentType: false,
        processData: false,
        headers: { "X-CSRFToken": csrftoken },
        success: function (data) {
            console.log(data)
            callback(data);
        }
    })
}

$('#nav_search').click(function (e) {
    var kw = $('#kw').val()
    if (kw == '') kw = $('#kw').attr('placeholder')
    console.log(kw)

    window.open('/search/?q=' + kw)
})
