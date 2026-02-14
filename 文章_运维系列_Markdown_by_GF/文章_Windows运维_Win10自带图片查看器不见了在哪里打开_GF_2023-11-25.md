# 文章_Windows运维_Win10自带图片查看器不见了在哪里打开_GF_2023-11-25

Windows 10 系统自带的图片查看器可以帮助我们快速查看电脑的图片，十分方便。

但是有不少用户发现自己 Win10 系统自带的图片查看器功能不见了，导致图片只能在画图或者其他工具里打开，极其麻烦。

其实这是因为用户不小心关闭了图片查看器功能导致的，因此说明一下 Win10 图片查看器在哪里重新进行打开。

## 方法 (1):

```txt
1. 我们鼠标右键点击桌面空白处，然后点击 "新建" -> "文本文档"。

2. 打开刚才新建的文本文档，将如下代码复制粘贴进去:

   Windows Registry Editor Version 5.00
   
   ; Change Extension's File Type [HKEY_CURRENT_USER\Software\Classes\.jpg] @="PhotoViewer.FileAssoc.Tiff"
   
   ; Change Extension's File Type [HKEY_CURRENT_USER\Software\Classes\.jpeg] @="PhotoViewer.FileAssoc.Tiff"
   
   ; Change Extension's File Type [HKEY_CURRENT_USER\Software\Classes\.gif] @="PhotoViewer.FileAssoc.Tiff"
   
   ; Change Extension's File Type [HKEY_CURRENT_USER\Software\Classes\.png] @="PhotoViewer.FileAssoc.Tiff"
   
   ; Change Extension's File Type [HKEY_CURRENT_USER\Software\Classes\.bmp] @="PhotoViewer.FileAssoc.Tiff"
   
   ; Change Extension's File Type [HKEY_CURRENT_USER\Software\Classes\.tiff] @="PhotoViewer.FileAssoc.Tiff"
   
   ; Change Extension's File Type [HKEY_CURRENT_USER\Software\Classes\.ico] @="PhotoViewer.FileAssoc.Tiff"

3. 我们将代码粘贴进去文本文档后，点击页面左上方的 "文件" -> "保存" 即可。

4. 然后我们关闭刚才的文本文档，将该文本文档的文件名更改为 "Windows 照片查看器.REG"，注意后缀名得由 "txt" 更改为 "REG"。

   弹出提醒:
   
       如果改变文件扩展名, 可能导致文件不可用。
       
       确实要更改吗?
   
   我们不用管，点击是即可。

5. 更改后缀名后，该文件就变为注册文件了，我们鼠标双击打开它。

   弹出提醒:
   
       添加信息可能会在无意中更改或删除值并导致组件无法继续正常工作。如果你不信任
       C:\Users\dell\Desktop\Windows 照片查看器.REG 中此信息的来源, 请不要将其添加
       到注册表中。
       
       确定要继续吗?
   
   我们点击确定将改文件添加到注册表中。

6. 我们右键点击选择一个图片文件，就可以看到打开方式中有 "Windows 照片查看器"，我们点击用 "Windows 照片查看器" 打开即可。
```

## 方法 (2):

```txt
1. 按 "Win" + "R" 组合键，打开运行，并输入 "regedit"，确定或回车，打开注册表编辑器。

2. 在注册表编辑器中，依次展开到 HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft 目录。

3. 在 Microsoft 目录下，找到 WindowsPhotoViewer\Capabilities\FileAssociations 目录项，可以看到该目录下的一系列关键文件。

4. 在 FileAssociations 目录下，空白处点击鼠标右键，在打开的菜单项中选择 "新建" -> "字符串值" 选项。

5. 如果想要打开 ".jpg" 后缀的文件，那么 [数值名称] 要填写为 ".jpg"，[数值数据] 填写为 "PhotoViewer.FileAssoc.Tiff"，然后点击 "确定"。

   如果想要打开 ".png" 后缀的文件，那么 [数值名称] 要填写为 ".png"，[数值数据] 填写为 "PhotoViewer.FileAssoc.Tiff"，然后点击 "确定"。

6. 这时候鼠标右键点击需要查看的图片，在菜单项中选择 "打开方式"，就能看到 "Windows 照片查看器" 出现了。
```

## 总结

以上就是关于 Windows运维 Win10自带图片查看器不见了在哪里打开 的全部内容。

更多内容可以访问我的代码仓库:

https://gitee.com/goufeng928/public

https://github.com/goufeng928/public
