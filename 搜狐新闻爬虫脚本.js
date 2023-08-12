var array = []

function isValidURL(url) {
    // 创建 URL 正则表达式
    const urlRegex = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
    // 判断字符串是否匹配正则表达式
    return urlRegex.test(url);
}

function traverseElements(element) {
    // 检查当前元素是否具有 href 属性
    if (element.hasAttribute('href')) {
        link = element.getAttribute('href')
        if (isValidURL(link)) {
            // console.log(link);
            array.push(link)
        }
    }
    // 递归遍历当前元素的子元素
    const children = element.children;
    for (let i = 0; i < children.length; i++) {
        traverseElements(children[i]);
    }
}

// 启动遍历，从根元素开始
traverseElements(document.documentElement);
const uniqueArray = [...new Set(array)];
data = []
uniqueArray.forEach(function (url) {
    data.push({"目标地址": url})
})
// 创建一个包含要写入的字符串的 Blob 对象
const content = JSON.stringify(data);
const blob = new Blob([content], {type: 'text/plain'});
// 创建一个下载链接，并设置相关属性
const downloadLink = document.createElement('a');
downloadLink.href = URL.createObjectURL(blob);
// 获取当前时间
const currentDate = new Date();
const timestamp = currentDate.toISOString().replace(/:/g, '-').substring(0, 19);
// 获取网页标题
const pageTitle = document.title;
// 拼接文件名
const fileName = `${pageTitle}_${timestamp}.txt`;
downloadLink.download = fileName;
// 触发下载链接
downloadLink.click();
// 清理创建的 URL 对象
URL.revokeObjectURL(downloadLink.href);