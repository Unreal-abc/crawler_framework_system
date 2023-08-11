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
const blob = new Blob([content], { type: 'text/plain' });

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