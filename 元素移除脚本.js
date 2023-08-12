/////////////////////////////////////////////
元素 = ""
currentURL = window.location.href
if (currentURL.includes("thepaper")) {
    元素 = "div.index_wrapper__L_zqV"
} else if (currentURL.includes("chinanews")) {
    元素 = "div.content_maincontent_more"
} else if (currentURL.includes("sina")) {
    元素 = "div.article"
} else if (currentURL.includes("news.cn")) {
    元素 = "div#detail"
}
var divElement = document.querySelector(元素);
while (divElement.parentNode) {
    divElement = divElement.parentNode;
    try {
        divElement.setAttribute('doNotRemove', 'true');
    } catch {
        console.log("异常")
    }
}

function isUrl(str) {
    var v = new RegExp('^(?!mailto:)(?:(?:http|https|ftp)://|//)(?:\\S+(?::\\S*)?@)?(?:(?:(?:[1-9]\\d?|1\\d\\d|2[01]\\d|22[0-3])(?:\\.(?:1?\\d{1,2}|2[0-4]\\d|25[0-5])){2}(?:\\.(?:[0-9]\\d?|1\\d\\d|2[0-4]\\d|25[0-4]))|(?:(?:[a-z\\u00a1-\\uffff0-9]+-?)*[a-z\\u00a1-\\uffff0-9]+)(?:\\.(?:[a-z\\u00a1-\\uffff0-9]+-?)*[a-z\\u00a1-\\uffff0-9]+)*(?:\\.(?:[a-z\\u00a1-\\uffff]{2,})))|localhost)(?::\\d{2,5})?(?:(/|\\?|#)[^\\s]*)?$', 'i');
    return v.test(str);
}

function traverseSettingProperties(element) {
    element.setAttribute('doNotRemove', 'true');
    const children = element.children;
    for (let i = 0; i < children.length; i++) {
        traverseSettingProperties(children[i]);
    }
}

traverseSettingProperties(document.querySelector(元素))


var data = []

function trimSpecial(string) {
    //替换字符串中的所有特殊字符（包含空格）
    if (string != "") {
        const pattern = /[`~!@#$^\-&*()=|{}'',\\\[\]\.<>\/?~@#￥……&*（）——|{}【】\s]/g;
        string = string.replace(pattern, "");
    }
    return string
}

function traverseElements(element) {
    var tagName = element.tagName.toLowerCase();
    if (element.children.length === 0 && tagName === "p" && element.hasAttribute("doNotRemove") || tagName.startsWith("h") && tagName.length === 2 && element.hasAttribute("doNotRemove")) {
        text = trimSpecial(element.textContent.trim());
        if (text !== '' && text.length >= 3) {
            data.push({"文本": text})
        }
    } else {
        if (tagName === "img" && element.hasAttribute("doNotRemove")) {
            if (isUrl(element.src)) {
                data.push({"pic": element.src})
            }

        } else {
            // 递归遍历当前元素的子元素
            const children = element.children;
            for (let i = 0; i < children.length; i++) {
                traverseElements(children[i]);
            }
        }

    }
}

// 启动遍历，从根元素开始
traverseElements(document.documentElement);
console.log(data)
