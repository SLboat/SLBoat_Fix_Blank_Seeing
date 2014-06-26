import sublime
import sublime_plugin
import re  # 正则库
from xml.sax.saxutils import unescape
import codecs

# 调试模式 - 很多提醒
DEBUG_MODE = True;

# 取得特定标题的存在
''' 它的逻辑...它的诞生
** 先寻找标题 [<title>鲨鱼哥</title>],获得位置t
** 从t.b开始往下寻找页结束 [</page>],获得位置p
** 用(t.b,p.b)构成区域r
** 取得区域r的中间内容c
** 寻找c中的[<text xml:space="preserve" bytes=".+">[^<]+</text>],是的,它是跨行的!所有位置为ts
** 取得ts中的最后一个位置,取得它的值,保存为内容f,这里f就是所有需要的东西,关于这个标题的了!
'''

def 提取空白标题(view, titleForLooking):
    # 查找标题位置t
    titleTag = '<title>' + titleForLooking + '</title>'
    # 标题Tag
    t_whereTitle = view.find(titleTag, 0)
    # 第一个标题位置,第一个,是的
    if not t_whereTitle:
        print("不存在标题:", titleForLooking)
        return False
        # 放弃死亡
    # 查找page结束标志p
    p_whereThisPageEnd = view.find("</page>", t_whereTitle.b)
    # 放置中间区域r
    r_textInReversion = sublime.Region(t_whereTitle.b, p_whereThisPageEnd.b)
    # 取得内容c
    c_textInReversion = view.substr(r_textInReversion)

    # 在C之中匹配最后的匹配内容
    regexp_matchText = re.compile(
        '<text xml:space="preserve" bytes=".+">([^<]+)</text>')
    found_all_Text = re.findall(regexp_matchText, c_textInReversion)
    if not found_all_Text:
        print("异常!找不到这个标题的任何内容:", titleForLooking)
        return False
    l_found_Text = found_all_Text[len(found_all_Text) - 1]
    # 取得最后一个
    f_textContent = unescape(l_found_Text, {"&apos;": "'", "&quot;": '"'})
    if DEBUG_MODE:
        print("它包含的内容是\n", f_textContent)
    return f_textContent
    # 返回文本
    # 只是展示而已
    # print ("位于的位置将是",t_whereTitle.a,p_whereThisPageEnd.b);
    # print ("它的内容是",c_textInReversion);

# 吸取特定的页面,暂时存放的目录是/Users/sen/tmp_blank/
class 吸取页面(sublime_plugin.TextCommand):

    def run(self, edit):
        view = self.view
        # 要取得页面文件的所有标题们
        array_BlankTitle = ["平淡心", "Openwrt 另类的多拨方式", "鲨鱼哥", "Sunny4836", "Mac 选择文件", "Linux 开启ssh", "Backfire版本", "Sudo权限", "Shell 显示当前路径", "想法:出售神秘盒子", "Lua on openwrt", "Ubuntu 添加在此打开终端", "Luci 系统时间格式修改", "Lcd4Linux", "QQ协议概述", "CSS 调试", "CSS 注释", "Lua 注释", "输出小写扩展", "名人语录扩展", "Lua 标识编码", "随机扑克牌扩展", "牛津汉英翻译扩展", "Kindle 阅读源码", "Kindle 邮件支持格式", "Openwrt 摄像头使用", "OpenWrt 主路由器映射", "Lua 获取系统时间", "DLINK DWR131", "Uboot 模式", "Lua 串口库", "Openwrt 控制舵机", "LED 过流", "Lua 多语句分割符号", "Lua 载入文件", "Lua 解码unicode字符串", "Lua 着色源码html输出", "Lua 作者采访", "Lua 快捷语法手册", "Lua 常见问题回答", "Kloxo 运行分析调试", "Shell 查找文件", "Apache 平均内存查看", "三洋 42CE530LED 液晶电视", "Lua nil", "Linode 缩小有数据磁盘实验", "MySQL 迁移保存目录", "Opkg 异常残留信息", "Lua 库资源", "Lua 进制转换", "Iptables 开放kloxo端口", "Coda lua语法着色", "ITunes Connect 招行收款申报", "Lua 局部代码块", "Lua 通常全局变量", "Lua 包路径操作", "Lua 一种模拟对象", "Minibb 安装", "Itunes提示：无法使用此Iphone", "IOS6 发布会视频", "Gmail 别名规则", "IOS6新功能设备兼容", "Openwrt USB键盘", "Kloxo 更换服务器ip后无法访问", "Pptp 更换服务器IP后无法访问", "效果: 一种能量槽显示", "Mac 执行shell程序", "创建测试用下载文件", "ITunes 转换铃声", "单词:亟", "MySQL Ibdata1", "Shell 带注释表现命令", "Html 指定页面编码", "Js 声明", "Js 判断数字", "Luasocket 访问网页", "VisualStudio 2008概述", "Shell 路径空白字符", "Luasocket下载", "Lua 元表", "Lua 随机数", "单词:Echo", "Openwrt USB开关", "Lua 代码风格建议", "Lua 不定参数", "Lua 序列化", "Lua 类型", "Svn 修改提交备注", "Lua 时间处理", "Mac Photoshop CS5", "Photoshop 建立指示圆圈", "Numbers 初识", "启动水手出现 7-zip SFX错误", "Lua 弱表", "帮助:系统:权限种类", "Kloxo 禁用ftp", "Chrome扩展 原理", "Chrome扩展 复制文本", "JQuery Mobile 扩展", "魔灯固件 概述", "CSS 操作滚动条", "Chrome 下图片文字比例失常", "Chrome扩展 设置图标文字", "JQuery val与text", "Linode 时间到期未关机内存大小", "600D ptp协议", "JQuery和php 混写", "Eye-Fi 传输原理", "唐纳铺 EBay计划", "Eye-Fi 重新激活", "单词:Lead free", "EBay 发货物流选择", "单词:Encapsulate", "Lua 异常处理", "Photoshop 图片隐藏文字", "单词:Excerpt", "Chrome扩展 多语言", "正则表达式 替换图片html地址", "文件:JustCapIt1021.jpg", "Liuwen 0312、改造号883 的WR703 升级Flash和内存", "Js 获取最后一个字符", "单词:Voila", "单词:CHS", "想法:Bot Writer", "唐纳铺 eBay计划结束", "单词:Language", "正则表达式 替换非末尾维基表格", "Excel 转换维基表格", "Mediawiki 优酷扩展", "想法:社会冒险机器人", "想法:活体水印", "单词:Wiki syntax", "想法:外部切换输入法标点按钮", "安富莱Mini-Logic逻辑分析仪扩展板", "DSTWO 盲升", "Php 替换标签", "Nano6 复位", "Rovio Windows安装软件", "Rovio Web端口", "Rovio 外网访问", "IPhone 3GS 再次更换电池", "单词:Hz", "IPhone4 摩米士高清膜", "C 操作硬件", "Eye-Fi 测试热点模式", "Rovio 路径录制", "Avr 定时器稳定", "想法:时刻效验带来的代价", "WinAVR", "想法:权利的游戏", "PayPal 收非美元货币", "想法:两种状态", "TextExpander For IOS", "Excel 强大", "Eye-Fi 直传模式", "CMD 测速", "Eye-Fi Arduino 结合", "想法:森亮号探索者1号", "卡马克", "想法:森亮号纪念牛仔裤", "想法:当越来越多的重合", "想法:事情的原因", "Eye-Fi 不能搜索热点", "Eye-Fi 连接中继服务器", "Eye-Fi 热点切换", "想法:一种小吃档", "单词:Attachment", "想法:胶皮剪辑", "ITunes 您没有权限进行更改", "单词:Frequency", "单词:Bothers", "蓝牙4.0 概述", "想法:一种更快更随意的记录见识", "单词:Proximity", "温度计", "想法:映射与反应", "想法:无限可能性", "单词:Official", "想法:水的张力", "EOS 600D 背带打结", "SMD01 贴片光敏电阻", "想法:泄漏的扩散", "想法:震动的危害", "ECos 与 ucos", "IPhone 3GS 开关键失灵", "IPhone 耳机线", "IPhone 3GS 排线座", "想法:示意图", "PCM-D50", "想法:协议", "唐纳铺 eBay计划航行翻船", "想法:过程", "想法:失控", "想法:一种提前的上传方式", "IPhone 3GS 最小工作", "IPhone 3GS 主板", "想法:实现利益的工具", "想法:谁改变了你", "IPhone 3GS 更换开关排线", "想法:谈话", "Mediawiki API 简单获取内容", "IOS APP 用户数据备份", "想法:幸运的卡鲁卡", "想法:想象力作为材料", "想法:石头出售见识", "IPhone 取卡针", "想法:工作之间", "想法:工作的定义", "想法:人们想要的自由", "想法:最坏的情况", "想法:喜欢与控制", "想法:自信", "想法:选择", "想法:希望", "想法:博弈", "想法:改变与休息", "想法:想着做什么", "想法:自我观察者", "想法:风险", "想法:与自己交谈", "想法:不同主流", "想法:想法就像过路车", "Mediawiki HTML文本", "Js 提取URL中的域名", "Chrome扩展 API变动", "PADS 导入bmp", "想法:古老的方式", "想法:眼光的当下", "想法:飞机的能力", "想法:实事求是", "想法:制造的束缚", "想法:快速的转录", "想法:规则规范的制定", "想法:出发点", "IPad mini 拍摄", "想法:有限制的工作时间", "Mediawiki code代码", "MySQL 安装指引", "MySQL 版本", "MySQL 程序文件", "MySQL 安装", "MySQL 5.0", "单词:Thin", "想法:陷入混乱", "Sublime 概述", "想法:一个目的的迷失", "想法:小的尝试", "单词:Mod", "想法:长时间的坐立", "Mac 带了的MUD游戏", "想法:想和不想", "Flikcr 大改版", "IPhone 3GS 摄像头不工作", "想法:客户的存在", "PCB 清洗", "Mediawiki 快速发布", "MySql 创建数据库", "AppleScript 作为Shell脚本", "Mac OS X 10.9", "想法:改变", "单词:Compatible", "想法:意志力", "HFS+ 文件系统", "NRF51822 SDK 安装", "单词:Brain attick", "想法:想法作为一种影响者", "IPad mini 欧版改机", "Openwrt ImageGenerator", "想法:指甲剪给猫剪指甲", "单词:Timeless", "想法:文艺", "想法:蝴蝶追逐者", "想法:感觉的变化", "单词:国家代号", "想法:文字转录", "想法:概念的流进来", "想法:等待", "想法:当你不得已选择", "想法:直觉", "想法:与压力进行透气", "ILuv iEP322PNK 耳机", "想法:制定规则", "想法:人们是盲目的", "想法:现实涌入", "想法:禅叶林", "想法:硬币的两面", "想法:触觉", "想法:感觉的延续", "想法:没有回头路", "想法:你需要慢下来", "想法:结果不重要", "想法:记录想法", "想法:压力和烦恼", "想法:寻找一种宁静", "想法:深入简单", "想法:观赏的估价", "想法:问题的本身", "想法:庆典的城市", "想法:闻着草香 担心奇怪", "想法:意识制造最初的自我", "想法:计算机可以做最傻的事", "想法:一种有规律的生活", "想法:一种特殊的体验", "想法:在树的另一面", "想法:若以禅的意志", "想法:限制在某些意义上是必须的", "想法:难得糊涂", "想法:阳光之下", "想法:文字输入的显然性做法", "想法:树下面的小世界", "想法:简单", "想法:在城市里", "想法:我们寻找不到方向", "想法:贪心是不好的", "想法:眼睛", "想法:人物的个性", "想法:从天空看下来", "想法:极度的情况下", "想法:最难的总是开头", "想法:怪异本身", "想法:在一定程度后", "想法:早上的起来", "Numbers 打开CSV", "想法:梦在其中醒来", "想法:太劳累了", "想法:清净的思考", "单词:Tail", "想法:压力的出现", "想法:对事物的熟悉", "正则表达式 匹配开头结尾", "想法:梦境的唤醒", "IPad2 游戏没有声音", "想法:更长的构建", "IPhone 5C", "Mac Shell 启动程序", "IPhone 5C 摩米士贴膜", "IPhone 5C 电源适配器", "单词:Affiliated", "想法:散漫的输入法", "想法:投入的状态", "想法:一个鬼影", "想法:过度的使用时间", "Sublime扩展 PhpBeautifier", "想法:一种状态", "想法:通常的充实和消遣", "想法:恐惧的沉淀", "Clozure CL 概述", "想法:他的方式", "IPhone 5C 卡托", "短英语:我的所有担心都离开了", "短英语:我知道答案了", "Mac 安装多个自己", "Numbers 边框"];
        title_now = 0
        # 要几个
        for title in array_BlankTitle:
            contentBlank = 提取空白标题(view, title)
            write_MW(title, contentBlank)
            # if (title_now > 100):
            #     break
            title_now = title_now + 1

# 取得所有空白的标题
# 如果要测试它,使用view.run_command("取得空白")
# 可以以一种方式来检测Mediawiki的空白标题
class 取得空白(sublime_plugin.TextCommand):

    def run(self, edit):
        myview = self.view
        all_title = myview.find_all('<title>.+</title>')
        # 全世界的标题...
        found_all = myview.find_all(
            '<text xml:space="preserve" bytes="[1-9]\d*" />')
        blankTitle = ""
        # 所有的空串子集合
        num = 0
        # 记录个数
        for regionBlankOne in found_all:
            # 寻找标题咯
            for regionTitleOne in all_title:
                if regionTitleOne.b > regionBlankOne.a:
                    title_str = myview.substr(last_title_region)
                    title_str = title_str.replace(
                        "<title>", "").replace("</title>", "")
                    blankTitle += title_str + "\n"
                    num = num + 1
                    break
                    # 退出
                else:
                    last_title_region = regionTitleOne
                    # 记住前一次的情况
        print(blankTitle)
        # 直接引用sublime就能工作的,因为这是个全局的库嘛!
        sublime.set_clipboard(blankTitle)
        # 送到剪贴板!再见
        print("船长,已经送到剪贴板!\n共有的空白标题数:", num)

# 写入到mediawiki文件,需要标题和内容即可!
# 接下来就是伟大的txt2wiki了!:)

def write_MW(title, content):
    if (not title or not content):
    	printf("标题或者内容是空的哩!");
    	return False;
    title = title.replace("/","|"); #临时换下来路径符号
    file_path = "/Users/sen/tmp_blank/";
    # 目录,看起来不能~这样的符号
    f = codecs.open(file_path + title + ".mediawiki", 'w', 'utf-8');
    # 打开文件句柄
    f.write(content);
    # 写入内容
    f.close;
    # 关闭文件
    return True;