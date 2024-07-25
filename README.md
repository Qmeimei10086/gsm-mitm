# 本程序仅供学习测试，请勿用于非法
# 指路
## gsm中间人攻击的伪基站部分 
https://github.com/Qmeimei10086/OpenBTS-gsm-mitm  
## gsm中间人攻击的攻击手机部分
https://github.com/Qmeimei10086/mobile-gsm-mitm  
# 原理
## 以下为正常的手机附着基站流程
![alt text](https://github.com/Qmeimei10086/gsm-mitm/blob/main/Attachment-flow-chart.jpg)  
我们可以看到2G gsm的鉴权是单向鉴权，既手机不会检验基站的安全性，这也给了我们伪基站的机会    
如上图所示，其中IMEI(国际移动设备识别码)并不重要,关键的鉴权步奏是2,3,6,7,这四步的数据来自sim卡 
这也意味着，只要我们拥有IMSI,RAND,SRES这四个数据，即使我们没有sim卡，也可以在真实基站上附着  
想到这里，我们的GSM中间人攻击计划变呼之欲出了  
## 以下为GSM中间人攻击的流程
![alt text](https://github.com/Qmeimei10086/gsm-mitm/blob/main/gsm-mitm-flow-chart.jpg)
如图所示，我们巧妙的运用伪基站，获取了鉴权所需的所有信息  
现在，我们可以完美的替代真正的手机在真实基站上注册，可以用它的身份干任何它能干的事，代替他发短信，接电话等等  
相当于没有碰到他去悄无声息的把他的sim卡给偷了
# 配置
## 注意请尽可能使用实体机而不是虚拟机，因为gsm对有时间及其严格的要求，使用虚拟机可能有延迟，产生意想不到的错误
## 推荐编译环境：Ubuntu16.04 推荐直接运行可执行文件环境：Ubuntu20.04   以上两个版本已经多次提供实验
请确保你已经完美安装了上文所说的OpenBTS和mobile 
接下来，你需要替换OpenBTS可执行文件的目录下的server.py文件  
在该目录下创建open_mitm文件或者在OpenBTS已运行的情况下运行OpenBTSCLI，并执行mitm_open命令  
参考: https://github.com/Qmeimei10086/OpenBTS-gsm-mitm  
# 运行
开三个终端分别OpenBTS,sipauthserse和server.py，这是伪基站的部分  
```javascript
./OpenBTS
./sipauthserse
python3 server.py
```
此时等待手机附着在我们的伪基站上  
当有设备附着时server.py会有信息提示  
此时在server.py的终端下输入tmsis指令可以查看附着的设备  
此时使用set imsi [你所需要攻击的imsi] 设置目标imsi  
或者直接编辑server.py将IMSI的值改为你所需要攻击的imsi  
设置完之后，运行攻击手机 开两个终端
```javascript
cd osmocom-bb/src/host/osmocon
./osmocon -m c123xor -p /dev/ttyUSB0 -c ../../target/firmware/board/compal_e88/layer1.highram.bin

cd osmocom-bb/src/host/layer23/src/mobile
./mobile -c default.cfg
```
此时不出意外的攻击手机已经在搜索并附着在基站上了  



