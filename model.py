import re
import util
import time
import datetime
class ContractInfo():
    def __init__(self,file_path):
        self.CONTRACT_CODE=None
        self.CONTRACT_NAME=None
        self.CONTRACT_EXPIRE_TYPE=None
        self.CONTRACT_START_DATE=None
        self.CONTRACT_END_DATE=None
        self.CONTRACT_TIME_LIMIT=None
        self.PROBATION_ISNOT=None
        self.PROBATION_START=None
        self.PROBATION_END=None
        self.PROBATION_MONEY=None
        self.WORK_CONT=None
        self.WORK_TYPE=None
        self.WORK_ADDR=None
        self.WORK_TIME_TYPE=None
        self.WORK_HOUR_DAY=None
        self.WORK_DAY_WEEK=None
        self.WORK_PERIOD=None
        self.SALARY_TYPE=None
        self.SALARY_BYTIME=None
        self.SALARY_PERIOD=None
        self.SALARY_BYNUM=None
        self.SALARY_DATE=None
        self.CONTRACT_TEXT= util.OCRtext2Text(file_path)
    def ChooseBestInfo(self,results,limit_phrases,find_length):
        '''
        :param results: 候选字段级
        :param limit_phrases: 约束字段集合
        :param find_length:  搜索范围
        :return:    最符合的字段
        '''
        for i in results:
            flag=0
            index=self.CONTRACT_TEXT.find(i)
            if index-find_length<=0:
                sub_text=self.CONTRACT_TEXT[0:index+find_length+len(i)]
            else:
                sub_text = self.CONTRACT_TEXT[index - find_length:index + find_length + len(i)]
            # print(sub_text)
            for k in limit_phrases:
                # print(k)
                for j in k:
                    if j not in sub_text:
                        flag=1
                        break
                if flag==0:
                    return i
        return "none"


    def getPROBATION_MONEY(self):
        '''
        获取试用期工资
        :param strr:
        :return:
        '''
        pattern = re.compile(r"(\d{3,6}元)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            return self.ChooseBestInfo(result, [['工资']], 8)
        else:
            return "none"

    def getSALARY_BYTIME(self):
        '''
        获取计时工资
        :param strr:
        :return:
        '''
        pattern = re.compile(r"(\d{3,6}元)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            return self.ChooseBestInfo(result, [['工资','。']],6 )
        else:
            return "none"

    def getSALARY_DATE(self):
        '''
        获取发工资日期
        :param strr:
        :return:
        '''
        pattern = re.compile(r"(每月\d{1,2}日)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            return self.ChooseBestInfo(result, ['工资'], 30)
        else:
            return "none"

    def getSALARY_TYPE(self):
        '''
        获取工资类型
        :param strr:
        :return:
        '''
        pattern = re.compile(r"(第\d{1}种)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            return self.ChooseBestInfo(result, ['工资'], 5)
        else:
            return "none"

    def getSALARY_PERIOD(self):
        """
        获取计时工资周期
        :return:
        """
        pattern = re.compile(r"甲方于(\D{2})")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            self.SALARY_PERIOD = self.ChooseBestInfo(result, ['日'], 5)
            return self.SALARY_PERIOD
        else:
            return "none"



    def getPROBATION_START(self):
        '''
        获取试用期开始时间
        :param strr:
        :return:
        '''

        pattern = re.compile(r"从(\d{4}年\d{1,2}月\d{1,2}日)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            self.PROBATION_START=self.ChooseBestInfo(result, [['试用期从']], 5)
            return self.PROBATION_START
        else:
            return "none"

    def getPROBATION_END(self):
        '''
        获取是否有试用期
        :param strr:
        :return:
        '''

        pattern = re.compile(r"(\d{4}年\d{1,2}月\d{1,2}日)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            self.PROBATION_END=self.ChooseBestInfo(result, [['止']], 1)
            return self.PROBATION_END
        else:
            return "none"

    def getPROBATION_ISNOT(self):
        '''
        获取是否有试用期
        :param strr:
        :return:
        '''

        if self.PROBATION_START:
            self.PROBATION_ISNOT='有'
            return self.PROBATION_ISNOT
        else:
            return "none"

    def getCONTRACT_EXPIRE_TYPE(self):
        '''
        获取合同期限类型
        :param strr:
        :return:
        '''
        pattern = re.compile(r"(第\d{1}种)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            return self.ChooseBestInfo(result, ['合同期限'], 10)
        else:
            return "none"

    def getCONTRACT_CODE(self): #合同编码
        '''
        获得合同编号
        :return:
        '''
        if self.CONTRACT_TEXT==None:
            return "none"
        pattern = re.compile(r"(?<=编号：)\d+")
        result=re.search(pattern, self.CONTRACT_TEXT)
        if result:
            return self.ChooseBestInfo(result, [['劳动合同']], 10)
        else:
            return "none"


    def getCONTRACT_NAME(self): #劳动合同名称
        '''
        获取劳动合同名称
        :param strr:
        :return:
        '''
        pattern = re.compile(r"(\D{3,4}劳动合同)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            return self.ChooseBestInfo(result, [['甲方']], 10)
        else:
            return "none"


    def getCONTRACT_START_DATE(self): #合同起始日期
        """
        获取年月日
        :param strr:
        :return:
        """
        pattern = re.compile(r"(\d{4}年\d{1,2}月\d{1,2}日)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            self.CONTRACT_START_DATE=self.ChooseBestInfo(result, [['从']], 1)
            return self.CONTRACT_START_DATE
        else:
            return "none"

    def getCONTRACT_END_DATE(self): #合同终止日期
        """
        获取年月日
        :param strr:
        :return:
        """
        pattern = re.compile(r"(\d{4}年\d{1,2}月\d{1,2}日)")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            self.CONTRACT_END_DATE = self.ChooseBestInfo(result, [['止','其中']], 8)
            return self.CONTRACT_END_DATE
        else:
            return "none"
    def getCONTRACT_TIME_LIMIT(self):
        """
        获取合同年限
        :return:
        """

        def datetrans(text):
            dates = time.strptime(text, "%Y年%m月%d日")
            return time.strftime("%Y-%m-%d", dates)
        if self.CONTRACT_START_DATE==None or self.CONTRACT_START_DATE=='none' or self.CONTRACT_END_DATE==None or self.CONTRACT_END_DATE=='none':
            return "none"

        start_time=datetrans(self.CONTRACT_START_DATE)
        end_time=datetrans(self.CONTRACT_END_DATE)
        d1 = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        d2 = datetime.datetime.strptime(end_time, '%Y-%m-%d')
        s_date=d1.year*365+d1.month*30+d1.day
        e_date = d2.year * 365 + d2.month * 30 + d2.day
        delta = e_date - s_date

        year=int(delta/365)
        month=int(delta%365/30)
        day=int(delta%365%30)
        strr=''
        if year!=0:
            strr=strr+str(year)+'年'
        if month!=0:
            strr=strr+str(month)+'月'
        if day!=0:
            strr=strr+str(day)+'日'
        return strr

    def getWORK_CONT(self): #获取工作内容
        """
        获取工作内容
        :param strr:
        :return:
        """
        pattern = re.compile(r"工作内容为([\u4E00-\u9FA5A-Za-z0-9_]+)，|工作岗位是(\D{3,6})，")
        result = pattern.findall(self.CONTRACT_TEXT)
        result=[p for p in result[0] if p!=""]
        print(result)
        if result:
            self.WORK_CONT = self.ChooseBestInfo(result, [['工作内容为','，'],['工作岗位','，']], 8)
            return self.WORK_CONT
        else:
            return "none"

    def getWORK_ADDR(self):  #获取工作地点
        """
        获取工作地点
        :param strr:
        :return:
        """
        pattern = re.compile(r"工作地点为([\u4E00-\u9FA5A-Za-z0-9_]+)。")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            self.WORK_ADDR = self.ChooseBestInfo(result, [['工作地点','。']], 6)
            return self.WORK_ADDR
        else:
            return "none"

    def getWORK_HOUR_DAY(self):  #每日工作时间
        """
        获取每日工作/小时
        :param self:
        :return:
        """
        pattern = re.compile(r"每日工作时间(\d{1}\D{2})")
        result = pattern.findall(self.CONTRACT_TEXT)
        print(result)
        if result:
            self.WORK_HOUR_DAY = self.ChooseBestInfo(result, [['时间','，']], 5)
            return self.WORK_HOUR_DAY
        else:
            return "none"

    def getWORK_DAY_WEEK(self):  #每周工作时间
        """
        获取每周工作/小时
        :return:
        """
        pattern = re.compile(r"每周工作时间(\d{2})")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            self.WORK_DAY_WEEK = self.ChooseBestInfo(result, [['时间', '，']], 5)
            return self.WORK_DAY_WEEK + '小时'
        else:
            return "none"

    def getWORK_TIME_TYPE(self):  #工作时间方式
        """
        获取工作时间方式
        :param strr:
        :return:
        """
        pattern = re.compile(r"按以下第(\d{1})")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result == ['1']:
            return '标准工时制'
        elif result == ['2']:
            return '综合计算工时工作制'
        elif result == ['3']:
            return '不定时工作制'
        else:
            return "none"






    def getWORK_PERIOD(self):  #工作周期
        """
        获取工作周期
        :return:
        """
        pattern = re.compile(r"每周工作时间(\d{2})")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result:
            self.WORK_PERIOD = self.ChooseBestInfo(result, ['时间', '，'], 5)
            return self.WORK_PERIOD + '小时'
        else:
            return "none"



    def getWORK_TYPE(self): #合同约定岗位性质
        """
        获取岗位性质
        :param strr:
        :return:
        """
        pattern = re.compile(r"[\u4E00-\u9FA5A-Za-z0-9_]+")
        result = pattern.findall(self.CONTRACT_TEXT)
        if result :
            self.CONTRACT_END_DATE = self.ChooseBestInfo(result, ['岗位.', ','], 8)
            return self.CONTRACT_END_DATE
        else:
            return "none"





