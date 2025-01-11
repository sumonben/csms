console.log('loaded');

function onChangeAppendQs(obj) {
    //window.location.href = "?" + $(obj).attr('name') + "=" + $(obj).val();
    var $name = $(obj).attr('name');
    var $value = $(obj).val();
    addQstoUrl($name, $value);

}

function listSearchClick(obj) {
    var search = $(obj).closest("div.toolbar").find("input[name='q']");
    var $name = search.attr('name');
    var $value = search.val();
    addQstoUrl($name, $value);
}


function addQstoUrl($key, $value) {

    var url = window.location.href;

    if (url.indexOf('?') > -1) {
        url += '&' + $key + "=" + $value
    } else {
        url += '?' + $key + "=" + $value
    }

    window.location.href = url;
}