# 本程序仅供学习测试，请勿用于非法
# 原理
## 以下为正常的手机附着基站流程
![alt text](https://github.com/Qmeimei10086/gsm-mitm/blob/main/Attachment-flow-chart.jpg)  
我们可以看到2G gsm的鉴权是单向鉴权，既手机不会检验基站的安全性，这也给了我们伪基站的机会    
如上图所示，其中IMEI(国际移动设备识别码)并不重要,关键的鉴权步奏是2,3,6,7,这四步的数据来自sim卡 
这也意味着，只要我们拥有IMSI,RAND,SRES这四个数据，即使我们没有sim卡，也可以在真实基站上附着  
想到这里，我们的GSM中间人攻击计划变呼之欲出了  
## 以下为GSM中间人攻击的流程
