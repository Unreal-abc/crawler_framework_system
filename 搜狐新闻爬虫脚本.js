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
            console.log(link);
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