# 思源可变字体切片

基于 [CSS unicode-range](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range) 特性，对 woff2 字体进行切片，以优化网络加载体验。

## 用法

导入 CSS 样式：

```html
<link rel="stylesheet" href="https://source-han-vf-sliced.takwolf.com/css/index.css">
```

然后可以在 CSS 样式中使用：

```css
body {
    font-family: SourceHanSans-CN, sans-serif;
}

h1 {
    font-family: SourceHanSerif-CN, serif;
}
```

全部字体名称如下：

| 字体 | font-family |
|---|---|
| 黑体 - 简体中文 | SourceHanSans-CN |
| 黑体 - 繁体中文 - 香港 | SourceHanSans-HK |
| 黑体 - 繁体中文 - 台湾 | SourceHanSans-TW |
| 黑体 - 日语 | SourceHanSans-JP |
| 黑体 - 韩语 | SourceHanSans-KR |
| 宋体 - 简体中文 | SourceHanSerif-CN |
| 宋体 - 繁体中文 - 香港 | SourceHanSerif-HK |
| 宋体 - 繁体中文 - 台湾 | SourceHanSerif-TW |
| 宋体 - 日语 | SourceHanSerif-JP |
| 宋体 - 韩语 | SourceHanSerif-KR |

## 本地构建

执行 `python -m tools.build` 命令来开始构建。

生成的文件位于 `www` 目录。

## 字体版本

- [思源黑体 - 2.005R](https://github.com/adobe-fonts/source-han-sans/releases/tag/2.005R)
- [思源宋体 - 2.003R](https://github.com/adobe-fonts/source-han-serif/releases/tag/2.003R)

## 程序依赖

- [FontTools](https://github.com/fonttools/fonttools)
- [Unidata Blocks](https://github.com/TakWolf/unidata-blocks)

## 参考资料

- [MDN - CSS unicode-range](https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/unicode-range)
- [FontTools Docs - pyftsubset](https://fonttools.readthedocs.io/en/latest/subset/)

## 许可证

[MIT License](LICENSE)
