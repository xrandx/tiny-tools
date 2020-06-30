@echo off
 
::--------------------------------------------------------------------------------------------------------用户参数赋值----------------------
 
::是否删除原有任务(注意：如果设为Y后，会删除系统的所有计划任务，请谨慎设定)
set pDelFlag=N
::请设定关机延迟小时数
set pDefHour=1
::请设定关机延迟分钟数
set pDefMinute=0
 
::--------------------------------------------------------------------------------------------------------系统参数赋值----------------------
 
set xpProgName=文件批量改名程序
set xpFileName=ChgName.bat
set xpAuthor=Taoether
set xpProgVer=1.0.0.1
set xpSupport=http://www.taoyoyo.net/ttt/post/458.html
set xpEmail=taoether@gmail.com
set xpMode=A
set xpDebug_Flag=0
::设置颜色方案
::xpColorDef--程序默认颜色配置 3e
::xpColorErr--程序错误时颜色配置 84, e4
::xpColorOth-- 其它颜色，比如帮助，版本信息 3f
::xpColor1，xpColor2--各程序自定义颜色
::默认方案--------3e,84,3f
set xpColorDef=30
set xpColorErr=84
set xpColorOth=3f
set xpColor1=30
set xpColor2=f4
goto lblInitialize 
 
::--------------------------------------------------------------------------------------------------------程序说明-------------------------
::此段为注释：
::批量改名程序，可以批量将文件名修改为文件日期+文件名
::需要加参数：1，文件；2，源目录；3，目标目录；4，是否带原文件名；5，指定文件名 
::不能在同一目录操作，有可能会重复修改……
 
::如：ChgName *.jpg D:\MyTemp\PHOTO d:\photo --将D:\MyTemp\PHOTO下*.jpg修改名字，保存到d:\photo\*.jpg
 
::--------------------------------------------------------------------------------------------------------系统初始化-------------------------
:lblInitialize 
goto lblStart
 
::--------------------------------------------------------------------------------------------------------环境设定子程序--------------------
:prSetDisplay
    ::cls
    color %1
    ::mode con lines=%2 cols=%3
    title 欢迎使用 %xpProgName%/%xpFileName%_V%xpProgVer% [By %xpAuthor%]    
    echo.
    echo     【欢迎使用 %xpProgName%/%xpFileName%_V%xpProgVer% By %xpAuthor%】
    Rem echo 欢迎使用!xpAuthor!编制的!xpProgName!(!xpFileName!) !xpProgName!_V!xpProgVer!
    echo.
    ::echo     当前程序运行模式=[%xpMode%]
goto :eof
 
::--------------------------------------------------------------------------------------------------------程序判断-------------------------
:lblStart
 
    if /I "%1"=="Version" goto lblVer
    if /I "%1"=="Ver" goto lblVer
    if /I "%1"=="V" goto lblVer
    if /I {%1}=={Help} goto lblhelp
    if /I "%1"=="H" goto lblhelp
    if /I {%1}=={H} goto lblhelp
    if /I {%1}=={?} goto lblhelp

    if {%1}=={} goto lblError
    if {%2}=={} goto lblError
    if {%3}=={} goto lblError
    if {%2}=={%3} goto lblError
    if not exist %2 goto lblError
    
goto lblMain
 
::--------------------------------------------------------------------------------------------------------帮助-------------------------
:lblhelp 
    Call :prSetDisplay %xpColorOth% 45 76
    echo.
    echo Help:
    echo -----------------------------------------
    echo  此程序可以批量修改文件名，默认将文件名修改为[文件日期时间+序号]；也可以指定文件名，文件名修改为[指定文件名+序号]；同时，也可保留原文件名。   
   ::批量改名程序，可以批量将文件名修改为文件日期+文件名
   ::需要加参数：1，文件；2，源目录；3，目标目录；4，是否带原文件名【】〖〗
 
    echo.
    echo  【用法】 %xpFileName% [参数1：文件] [参数2：源目录] [参数3：目标目录] [参数4：是否保留原文件名] [参数5：指定文件名]
    echo. 
    echo  【说明】
    echo    参数1：要修改名称的文件，支持通配符，如*.jpg、10*.jpg
    echo    参数2：源目录--要改名文件的所在目录
    echo    参数3：目标目录--改名后文件存放的目录，如果没有此目录，程序会自动创建目录
    echo    参数4：是否保留原文件名--非必要参数：设置此参数=Y时，保留原文件名(此时命名中不加序号)；此参数=N时，不保留原文件名，此时命名中会添加序号。
    echo    参数5：设置特定文件名--非必要参数：设置此参数时，以[参数5+序号/原文件名]命名；不设置时，以[文件的日期时间+序号/原文件名]命名。
    echo.
    echo  【注意】
    echo    1，参数1~3为必填参数，不能为空! 
    echo    2, 目录最后必须带斜杠"\"
    echo    3，源目录和目标目录不能为同一目录
    echo    4, 目标目录如果不存在时，程序会自动创建目录
    echo.
    echo  【此外】
    echo    参数1=Version，显示程序版本   (Version=Ver=V)
    echo    参数1=Help，显示程序帮助      (Help=H=?)
    echo.
    echo  【示例】
    echo     %xpFileName% *.jpg d:\photo\ d:\new\
    echo       处理文件夹d:\photo\中的*.jpg文件，复制到目录d:\new\中，不保留原文件名，按[文件的日期时间+序号]命名。
    echo     %xpFileName% *.jpg d:\photo\ d:\new\ Y
    echo       处理文件夹d:\photo\中的*.jpg文件，复制到目录d:\new\中，保留原文件名，按[文件的日期时间+原文件名]命名。
    echo     %xpFileName% 10*.jpg d:\photo\ d:\new\ N 20100910
    echo       处理文件夹d:\photo\中的10*.jpg文件，复制到目录d:\new\中，不保留原文件名，按[20100910+序号]命名。
    echo     %xpFileName% 10*.jpg d:\photo\ d:\new\ Y 20100910
    echo       处理文件夹d:\photo\中的10*.jpg文件，复制到目录d:\new\中，保留原文件名，按[20100910+原文件名]命名。
    echo.
    echo  【相关说明】 %xpSupport%
    echo  【技术支持】 %xpEmail%
    echo -----------------------------------------
    call :lblAd
goto lblEnd
 
::--------------------------------------------------------------------------------------------------------版本-------------------------
:lblVer
    Call :prSetDisplay %xpColorOth% 45 76
    echo.
    rem 重要声明：
    rem 本程序由陶永利编写，您可以任意传播，但请不要删除以下信息!
    rem 如用于商业用途，请与作者联系。
    echo     Version:
    echo     ------------------------------
    echo        Program: %xpProgName% / %xpFileName%
    echo        Author: %xpAuthor%
    echo        Version: %xpProgVer%
    echo        IssueTime: 20100526
    echo        UpdateTime: 
    echo        Email: %xpEmail%
    echo        Blog: http://www.taoyoyo.net/ttt/
    echo        HomePage: http://www.taoyoyo.net/
    echo     ------------------------------
    echo.
    echo     Version Log:
    echo     -----------------------------------------
    echo      Ver.   Date.     Log.
    echo     -----------------------------------------
    echo     V1000  20100526  New program issue.
    echo     V1001  20101010  Optimize program
    echo. 
    echo     ...
    echo     -----------------------------------------
    echo 相关说明：%xpSupport%
    echo 技术支持：%xpEmail%
    Call :lblAd
goto lblEnd
 
::--------------------------------------------------------------------------------------------------------错误处理-------------------------
:lblError
    Call :prSetDisplay %xpColorErr% 15 76
    echo.
        ::echo  【相关说明】 %xpSupport%
        ::echo  【技术支持】 %xpEmail%
        ::echo    --相关说明: %xpSupport%  技术支持: %xpEmail% 
        ::echo    --相关说明: %xpSupport%  技术支持: %xpEmail% 
    echo  【程序错误】
    echo.
    if {%1}=={} (
        echo    参数不足!
        echo.
        echo    此命令需要三个必选参数：
        echo        [参数1：文件]
        echo        [参数2：源目录]
        echo        [参数3：目标目录]
        echo    还有一个选填参数：
        echo        [参数4：是否保留原文件名]
        echo        [参数5：指定文件名]
        echo.
        echo    请键入[%xpFileName% H]查看帮助信息
        echo.        
        echo    --相关说明: %xpSupport%
        echo    --技术支持: %xpEmail% 
        goto lblEnd
        )
    if {%2}=={} (
        echo    参数不足!
        echo.
        echo    此命令需要三个必选参数：
        echo        [参数1：文件]
        echo        [参数2：源目录]
        echo        [参数3：目标目录]
        echo    还有一个选填参数：
        echo        [参数4：是否保留原文件名]
        echo        [参数5：指定文件名]
        echo.
        echo    请键入[%xpFileName% H]查看帮助信息
        echo.
        echo    --相关说明: %xpSupport%
        echo    --技术支持: %xpEmail% 
        goto lblEnd
        )
    if {%3}=={} (
        echo    参数不足!
        echo.
        echo    此命令需要三个必选参数：
        echo        [参数1：文件]
        echo        [参数2：源目录]
        echo        [参数3：目标目录]
        echo    还有一个选填参数：
        echo        [参数4：是否保留原文件名]
        echo        [参数5：指定文件名]
        echo.
        echo    请键入[%xpFileName% H]查看帮助信息
        echo.
        echo    --相关说明: %xpSupport%
        echo    --技术支持: %xpEmail% 
        goto lblEnd
        )
    if /I {%2}=={%3} (
        echo    参数错误!
        echo.
        echo    源目录和目标目录相同，这样会导致重复命名，请修改参数。
        echo.
        echo    请键入[%xpFileName% H]查看帮助信息
        echo.
        echo    --相关说明: %xpSupport%
        echo    --技术支持: %xpEmail% 
        goto lblEnd
        )
    if not exist %2 (
        echo    源目录错误!
        echo.
        echo    源目录[%2]不存在，请检查后重新输入。
        echo.
        echo    请键入[%xpFileName% H]查看帮助信息
        echo.
        echo    --相关说明: %xpSupport%
        echo    --技术支持: %xpEmail%
        goto lblEnd
        )
    )    
           
    echo.
    
goto lblEnd
 
::--------------------------------------------------------------------------------------------------------广告-------------------------
:lblAd
    echo.
    ::echo ----------
    echo 【一点广告】
    ::echo ----------
    echo     本资料由悠悠网, TTT BLOG提供，欢迎访问!
    echo     [悠悠网] http://www.taoyoyo.net/
    echo     [TTT BLOG] http://www.taoyoyo.net/ttt/
    echo     联系我们：taoether@gmail.com
goto :eof
 
======下面是广告时间~~======
 
本资料由悠悠网提供，欢迎访问悠悠网：http://www.taoyoyo.net/
 
悠悠网，精心为大家收集整理精品网络资源!
 
欢迎进入--
　　[猫腻小说] http://www.taoyoyo.net/maoni/ 
 　　 专门收集整理猫腻的作品，保证原汁原味，有前后题记，更新时间，全部手工编辑整理，便于阅读和收藏，并开通wap功能(手机阅读)，以及邮件，RSS订
 
阅功能!
　　[猫腻论坛] http://www.taoyoyo.net/mao/ 
 　　 这里是猫腻书迷的家，是由猫腻书迷自发组织的论坛，专门讨论猫腻的小说，并收集猫大的各种新闻，作品!
　　[经典小游戏] http://www.taoyoyo.net/mgame/
　　  收集整理经典的小游戏，绝对经典，不经典不收集，可以下载，可以在线玩，并有游戏说明，攻略，心得!
　　[我的资源] http://www.taoyoyo.net/cpost/res/res_home.ASP
　　  收集整理经典的小说、学习资料、精品软件等。
　　[TTT BLOG] http://www.taoyoyo.net/ttt/ 
　　  我的博客，生活点滴，心得体会，希望与更多的朋友分享!(关注oracle,delphi,java,Linux,unix,以及网站知识!)
　　[YOYO BLOG] http://www.taoyoyo.net/yoyo/ 
 　　 女儿的博客，记录我的宝贝女儿的生活点滴，瞬间，留下美好的回忆!
 
　　[悠悠文摘] http://www.taoyoyo.net/lib/ 
　　  悠悠周刊网站，精心收集整理精品文摘，并发行免费电子杂志<悠悠周刊>
 
联系我们：taoether@gmail.com

::--------------------------------------------------------------------------------------------------------临时保存代码-------------------------
    ::保留原文件名
    ::copy %%i %3!pFNewName!_%%~nxi
    ::不保留原文件名 
    ::copy %%i %3!pFNewName!%%~xi
for /r %2 %%i in (%1) do (
    set pFTime=%%~ti  
    set pFNewName=!pFTime:~0,4!!pFTime:~5,2!!pFTime:~8,2!_!pFTime:~11,2!!pFTime:~14,2!
    set /a pNo=!pNo!+1
    if /I "%4"=="Y" (
        copy %%i %3!pFNewName!_%%~nxi
        echo !pNo! %%~nxi - %%~ti 更名为 !pFNewName!_%%~nxi
       )
    if /I not "%4"=="Y" (
        copy %%i %3!pFNewName!_!pNo!%%~xi
        echo !pNo! %%~nxi - %%~ti 更名为 !pFNewName!_!pNo!%%~xi
       )    
) 

::--------------------------------------------------------------------------------------------------------主程序-------------------------
:lblMain
 
  Call :prSetDisplay %xpColorDef%  
 
@echo off
setlocal enabledelayedexpansion
echo.
::echo    参数：%1 ，%2 ，%3 , %4
echo    将目录[%2]中的文件%1，复制到目录[%3]中，并修改文件名……
echo.
echo ---处理如下---
echo.
::如果目标目录不存在时，创建
if not exist %3 (
    echo    目标目录[%3]不存在，正在创建……
    md %3 
    echo    --目标目录创建成功!
    echo.
)    
set pNo=0
for /r %2 %%i in (%1) do (
    set pFTime=%%~ti
    if /I {%5}=={} (
        ::以文件的日期时间命名
        set pFNewName=!pFTime:~0,4!!pFTime:~5,2!!pFTime:~8,2!_!pFTime:~11,2!!pFTime:~14,2!
    ) else (
        ::以任意名称命名
        set pFNewName=%5
    )
    set /a pNo=!pNo!+1
    if /I "%4"=="Y" (
        copy %%i %3!pFNewName!_%%~nxi
        echo !pNo! %%~nxi - %%~ti 更名为 !pFNewName!_%%~nxi
    ) else (
        copy %%i %3!pFNewName!_!pNo!%%~xi
        echo !pNo! %%~nxi - %%~ti 更名为 !pFNewName!_!pNo!%%~xi
    )    
)
 
goto lblEnd
 

::--------------------------------------------------------------------------------------------------------程序结束------------------------- 
:lblEnd
echo.
pause
