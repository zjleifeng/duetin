var musicalIdStr = "281206574071742464";
var authoreIdStr = "162768534672953345";

$('.s-head-right,.s-download,.download').click(function(){
    //location.href="http://a.app.qq.com/o/simple.jsp?pkgname=com.zhiliaoapp.musically"
    doVideoApp()
})
var isPlay = false;
var url = window.location.href.split('#')[0];

function isZhCN(pathname) {
    return navigator.language.toLowerCase().indexOf('zh-cn') !== -1;
}
function getBid(id) {
    return btoa('11111'+id).replace(/=/g,"")
}
function isMusemuseUrl(){
    return /musemuse.cn/.test(window.location.host)
}
function testUrl(){
    return /test/.test(window.location.host)
}
function isWeixinBrowser(){
    return /micromessenger/.test(navigator.userAgent.toLowerCase())
}
function isAndroid(){
    return (/android/i).test(navigator.userAgent)
}


function doVideoApp(){
    window.setTimeout(function(){
        goAppStore();
    },2000);
    goVideoApp();
}
function goVideoApp(){
    if(isAndroid()){
        // window.location.href = 'musically://musical?present=1&bid='+getBid(musicalIdStr)+'&id=' + musicalIdStr
        window.location.href="https://play.google.com/store/apps/details?id=music.duetin";

    }
    else{
        window.location.href="https://play.google.com/store/apps/details?id=music.duetin";
    }
}

function doProfileApp (authoreIdStr,e){
    e.stopPropagation();
    window.setTimeout(function(){
        goAppStore();
    },1500);
    goProfileApp(authoreIdStr);
}

function goProfileApp (authoreIdStr){
    if (testUrl()) {
        if(isAndroid()){
            // window.location.href = 'musically://profile?userID='+authoreIdStr
            window.location.href="https://play.google.com/store/apps/details?id=music.duetin";

        }
        else{
            // window.location.href = '//app-test.musemuse.cn/h5/share/usr/'+authoreIdStr+'.html'
            window.location.href="https://play.google.com/store/apps/details?id=music.duetin";

        }
    }else{
        if(isAndroid()){
            // window.location.href = 'musically://profile?userID='+authoreIdStr
            window.location.href="https://play.google.com/store/apps/details?id=music.duetin";

        }
        else{
            if (isMusemuseUrl()) {
                window.location.href="https://play.google.com/store/apps/details?id=music.duetin";

                // window.location.href = '//app.musemuse.cn/h5/share/usr/'+authoreIdStr+'.html'
            }else{
                window.location.href="https://play.google.com/store/apps/details?id=music.duetin";

                // window.location.href = '//app.musemuse.cn/h5/share/usr/'+authoreIdStr+'.html'
            }
        }
    }
}

function goAppStore(){
    if(isZhCN()){
        if(isAndroid()){
            window.location.href = 'https://play.google.com/store/apps/details?id=music.duetin'
        }
        // else{
        //     window.location.href = 'https://itunes.apple.com/cn/app/id835599320'
        // }
    }else{
        window.location.href = 'https://play.google.com/store/apps/details?id=music.duetin'
    }
}
function encodeData (data) {
    if (!data || typeof data != 'object') {
        return '';
    }
    return Object.keys(data).map(function(key) {
        return [ key, data[key] ].map(encodeURIComponent).join("=");
    }).join("&");
}