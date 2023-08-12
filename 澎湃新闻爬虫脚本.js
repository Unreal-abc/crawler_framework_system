// document
//     .querySelector("div.ant-row")
//     .querySelectorAll("div.ant-col")
//     .forEach(function name(params) {
//         console.log(params)
//     })

var data = []
document
    .querySelectorAll("div.ant-row")
    .forEach(function (a) {
        // console.log(a)
        a.querySelectorAll("div.ant-col")
            .forEach(function (b) {
                // console.log(b)
                link = b.querySelector("a")
                目标地址 = link.href
                pic = link.querySelector("img")
                图片地址 = "null"
                if (pic) {
                    图片地址 = pic.getAttribute("src")
                }
                title = link.querySelector("h2")
                标题 = "null"
                if (title) {
                    标题 = title.textContent
                }
                data.push({
                    "目标地址": 目标地址,
                    "图片地址": 图片地址,
                    "标题": 标题
                })
            })
    })
// console.log(data)
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


/////////////////////////////////////////////////////////////////////////////////


//获取网页文本
// 使用 document.body.innerText
const textContent1 = document.body.innerText;
console.log(textContent1);
// 使用 document.body.textContent
const textContent2 = document.body.textContent;
console.log(textContent2);

////////////////////////
function removeElement() {
    document.querySelectorAll("div.mdCard").forEach(function name(params) {
        params.remove()
    })
    // document.querySelector("div#commentWrapper").remove()
}
function traverseToRemoveElements(element) {
// 检查类名是否包含 "index_content"
    for (const className of element.classList) {
        /////////////////////////
        if (className.includes("index_content")) {
            element.remove();
            continue
        }
        ////////////////
        if (className.includes("index_recommendsWrap")) {
            element.remove();
            continue
        }
        ////////////////
        if (className.includes("commentWrapper")) {
            element.remove();
            continue
        }
        ////////////////
        if (className.includes("index_headerfixed")) {
            element.remove();
            continue
        }
    }
    const children = element.children;
    for (let i = 0; i < children.length; i++) {
        traverseToRemoveElements(children[i]);
    }
}
removeElement()
// 启动遍历，从根元素开始
traverseToRemoveElements(document.documentElement);
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
    if (element.children.length === 0 && tagName === "p" || tagName.startsWith("h") && tagName.length === 2) {
        text = trimSpecial(element.textContent.trim());
        if (text !== '' && text.length >= 3) {
            data.push({"文本": text})
            // console.log('文本:', text);
        }
    } else {
        if (tagName === "img") {
            data.push({"pic": element.src})
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

////////////////////////////
//去除特殊字符~!@#$^-&*()=|{}':;',\[].<>/?~！@#￥……&*（）——|{}【】'；：""'。，、？
function trimSpecial(string) {
    //替换字符串中的所有特殊字符（包含空格）
    if (string != "") {
        const pattern = /[`~!@#$^\-&*()=|{}'',\\\[\]\.<>\/?~@#￥……&*（）——|{}【】\s]/g;
        string = string.replace(pattern, "");
    }
    return string
}

str_ = "这是一个带有非书写符号的字符串！@#它包含&*多个特殊字符。";
console.log(trimSpecial(str_))


///////////////////////////////////////
function removeElement() {
    document.querySelectorAll("div.mdCard").forEach(function name(params) {
        params.remove()
    })
    document.querySelector("div#commentWrapper").remove()
}
function traverseToRemoveElements(element) {
// 检查类名是否包含 "index_content"
    for (const className of element.classList) {
        /////////////////////////
        if (className.includes("index_content")) {
            element.remove();
            continue
        }
        ////////////////
        if (className.includes("index_recommendsWrap")) {
            element.remove();
            continue
        }
        ////////////////
        if (className.includes("commentWrapper")) {
            element.remove();
            continue
        }
        ////////////////
        if (className.includes("index_headerfixed")) {
            element.remove();
            continue
        }
    }
    const children = element.children;
    for (let i = 0; i < children.length; i++) {
        traverseToRemoveElements(children[i]);
    }
}
removeElement()
// 启动遍历，从根元素开始
traverseToRemoveElements(document.documentElement);