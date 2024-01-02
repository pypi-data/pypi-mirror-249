![Python与数据分析及可视化](https://imgservice.suning.cn/uimg1/b2c/image/gIH3lXgAHfqhSFy_QvLmpQ.jpg_800w_800h_4e)
# Prof.Li's Python Education Tools

## Author: 道法自然  lilluqun@gmail.com success@shnu.edu.cn

## **模块安装：pip install -U python-education-tools**

* Python Education Tools模块为教材配套工具。模块由作者Prof.Luqun Li团队自主开发 。
* 模块简称“pet工具”。取Python Education Tools 首字母的缩写pet（英文意思：宠物），希望该工具成为大家学习的宠物！。
* 所有工具包的根目录是pet。模块安装后对应的安装包为 pet.datasets.* 、pet.util.*等。
* 该模块提供了教学相关代码工具、数据生成工具，以及所有教学案例等。
* 模块安装后，可使用一行Python代码获取本书教学案例：import pet.textbook1.codes ，即可将教学案例下载到Windows用户桌面。
* 其他教学资源可以参见GitHub：https://github.com/liluqun。
* 作者会对模块不断更新，确保为读者提供最佳的代码工具、教学案例与服务。
* 如果您有好的建议，请发邮件到liluqun@gmail.com联系我。

![hah](https://tse1-mm.cn.bing.net/th/id/OIP-C.1WzofyXU4XlVG1soFYMmpgHaEc?w=273&h=180&c=7&r=0&o=5&dpr=2&pid=1.7)

`````

** Pet相关模块的功能：**

1.提供“编程之道”论述。
      趣谈编程之道（运行以下1行Python代码）：
      import pet.this
      与“晦涩难懂的”Python编程之禅import this对应，本模块从中国传统文化，心，术，道三个层次，引用古文阐述编程之道。
      内容大家自己体会，道法自然，道不简则理不明！！Just for Fun！！！（不笑不足以为道!!)

2.提供教材配套案例下载。
      教材配套的案例下载（运行以下1行Python代码）：
 
      import pet.textbook1.codes
      稍后(一般是瞬间），即可将教学案例下载到Windows桌面，目录为：Python与数据分析及可视化教学案例。
  


3.提供教材涉及的数据集。
    pet模块提供了如下数据集：
    ['ip地址分类', '研究生初试成绩', '上海地铁线路', '北京公交车', '北京地铁线路', 
    '2022年通识课', '2022年优秀毕业论文', '双色球', '2022转专业-报名名单', '2023转专业-报名名单',
     '2023转专业-录取名单', '教务处认定学科竞赛目录', '2023-2024-1上海师范大学课程表', 
     '2023上海市二级程序员大赛名单', 'iris', 
     'Python二级考试大纲', '道德经', '心经', '太乙金华宗旨', '荷塘月色', '微信接龙投票']

  通过调用函数：factory.load_data(key='道德经',prompt=True) 获取DataFrame或文本文件
  xlsx格式返回dataframe, txt格式返回字符串
  
  如：factory.load_data(key='上海地铁线路')
  
4.提供随机伪数据集的生成函数。

    from pet.datasets import factory

    以下2个函数可以分别随机生成Series和DataFrame对象数据。
    
    #生成纯净Series数据：
    df=factory.gen_sample_series() #默认生成Series样本数据 40条，姓名，成绩
    
    #生成带噪声的Series数据：
    df = factory.gen_sample_series(number=30, noise=0.1, repeat=2)
    其中：number 为记录数，noise为随机产生None数据概率，repeat为允许重复数据项的最高次数。
    
    #生成纯净DataFrame数据：
    df=factory.gen_sample_dataframe() #默认生成Series样本数据 40条，姓名，成绩
    
    #生成带噪声的DataFrame数据：
   factory.gen_sample_dataframe(sample_order=sample_order,
                         number: int = 40,
                         dst=f'{pet_home}/generated_sample_dataframe_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.xlsx',
                         noise=0,
                         repeat=1):

    即：按照订单格式产生数据。
    sample_order：订单(字典）
    number：数量
    dst：数据保存的目录
    noise：噪声，增加None数据字段概率
    repeat：产生重复数据
    ------------------

   sample_orde为产生数据订单格式，样本格式如下：
   
    sample_order = {

    '学号.iid': 220151000,
    '考号.i': [151000, 789000],
    '姓名.n': '',  # ""生成默认的随机名字，也可以设置姓名字符串，['赵钱孙李','微甜地平天下'],
    '性别.c': ['男', '女'],
    '日期.d': ['2020-2-24', '2024-12-31'],
    '时间.t': ['00:00:00', '23:59:59'],
    '年龄.i': [18, 24],
    '政治面貌.c': ['党员', '团员', '群众'],
    '专业.c': ['计算机科学与技术', '人工智能', '软件工程', '自动控制', '机械制造', '自动控制'],
    '学校.c': ['清华大学', '北京大学', '复旦大学', '上海交通大学', '上海师范大学', '中国科技大学', '上海大学'],
    '政治.i': [19, 100],
    '英语.i': [29, 100],
    '英语类别.c': ['英语一', '英语二'],
    '高等数学.i': [30, 140],
    '数学类别.c': ['数学一', '数学二', '数学三'],
    '专业课.i': [30, 150],
    '净收入.f': [30.3, 150.55, 3]}
     其中：
        .iid: 代表产生整数学号（字段名称.类型）
        .i:代表整数
        .n: 代表名字
        .c: 代表类别
        .d: 代表日期
        .t: 代表时间
        .f: 代表浮点数
        
   5.其它动态数据。
   提供获取本机操作系统相关的信息到DataFrame中：
    directory_to_dataframe(directory=Path.home(), dst=Path.home() / 'files_info.xlsx')：将某一目录文件信息记录到DataFrame
    pid_info_to_dataframe()：获取进程信息
    pid_details_to_dataframe()：获取进程详细信息
    pid_networkinfo_to_dataframe():获取网络流量信息
    get_local_packages():获取本机安装的模块信息
    get_nic_series()：获取网卡信息
    get_wifi_password_dataframe()：获取登录过的wifi密码
    get_reg_parameters(x, y, data)：获取线性回归模型参数。

`````

![hah](https://pic.qtfm.cn/2018/07/26/partner_72d7e1f09c547f3659b373eff7ae1d4f.jpg!400)