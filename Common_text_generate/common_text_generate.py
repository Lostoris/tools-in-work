import sys
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QFile
import pyperclip
import os
import operator

Data_Path = r'D:/Code/respository/tools-in-work/Common_text_generate/generate_data/file.txt'
Template_Path = r'D:/Code/respository/tools-in-work/Common_text_generate/generate_data/Template'
Ui_Path = r'D:/Code/respository/tools-in-work/Common_text_generate/generate_form.ui'
class Main_Win:
    def __init__(self):
        self.ui = QUiLoader().load(Ui_Path)
        self.Obj_Connect()
        self.Val_Init()
        self.ischanged_text = False

        self.test()
        self.ui.show()


    #变量初始化
    def Val_Init(self):
        self.static_text = ''
        self.variable_text = ''
        self.copy_text = ''

        self.variable_text_list = []
        self.row =0
        self.each_rown = []
        self.all_case = 1
        self.cnt = 0
        self.case_now = []
        self.dic_now = {}
        self.file_count = 1


    #处理函数
    def deal_variable_text(self):
        text_temp = self.variable_text.split('\n')
        for i,line in enumerate(text_temp):
            if operator.eq(line,''):
                continue
            line_list = line.split(' ')
            self.variable_text_list.append(line_list)
            self.row+=1
            self.each_rown.append(len(line_list))
        self.all_case = 1
        self.test_print()
        for i in range(self.row):
            self.all_case *= self.each_rown[i]


            
    
    def get_case_now(self): #更新目前序列
        self.case_now = []
        cnt =  self.cnt
        for i in range(self.row):
            self.case_now.append(cnt%self.each_rown[i])
            cnt = int(cnt/self.each_rown[i])
    
    def get_dic_now(self): #更新目前变量字典
        self.dic_now = {}
        self.get_case_now()
        for i in range(self.row):
            self.dic_now['<'+str(i+1)+'>'] = self.variable_text_list[i][self.case_now[i]]
    
    def get_copy_text(self): #更新目前生成的文本
        self.get_dic_now()
        self.copy_text = self.static_text
        for i in range(self.row):
            temp = '<'+str(self.row-i)+'>'
            self.copy_text = self.copy_text.replace(temp,self.dic_now[temp])
        pass

    def generate_copy(self):
        self.get_copy_text()
        pyperclip.copy(self.copy_text)


    #链接控件
    def Obj_Connect(self):
        self.ui.Copy_Next_Bt.clicked.connect(self.Copy_Next)
        self.ui.Copy_Pre_Bt.clicked.connect(self.Copy_Pre)
        self.ui.Generate_Bt.clicked.connect(self.Generate_file)
        self.ui.Select_Template_Bt.clicked.connect(self.Select_Template)
        self.ui.Save_Template_Bt.clicked.connect(self.Save_Template)
        self.ui.Delete_Template_Bt.clicked.connect(self.Delete_Template)
        self.ui.Static_Text.textChanged.connect(self.Text_Changed)
        # self.ui.Template_comboBox.currentIndexChanged.connect(self.load_template)
    
    #响应函数
    def Copy_Next(self):
        self.cnt+=1
        if self.cnt >= self.all_case:
            self.cnt = 0
        self.generate_copy()
        self.ui.Static_Text.setPlainText(self.copy_text)
        self.ui.Info_Text.setPlainText("已复制到剪切板：当前为第"+str(self.cnt+1)+"个\n")
        self.test_print()

    
    def Copy_Pre(self):
        self.cnt-=1
        if self.cnt < 0:
            self.cnt = self.all_case - 1
        self.generate_copy()
        self.ui.Static_Text.setPlainText(self.copy_text)
        self.ui.Info_Text.setPlainText("已复制到剪切板：当前为第"+str(self.cnt+1)+"个\n")

    def Generate_file(self):
        temp = self.cnt
        self.cnt = 0
        f = open(Data_Path,'w+')
        for i in range(self.all_case):
            self.cnt = i
            self.get_copy_text()
            f.write(self.copy_text)
            self.ui.Info_Text.setPlainText("已生成"+str(i+1)+"份")
        
        self.ui.Info_Text.setPlainText("已完成, 共"+str(self.all_case)+"份")
        self.cnt = temp


    def Save_Template(self):
        fname = os.path.join(Template_Path,'Template'+str(self.file_count)+'.txt')
        f = open(fname,'w+')
        f.write(self.ui.Static_Text.toPlainText())
        f.write('￥')
        f.write(self.ui.Variable_Text.toPlainText())
        f.close()
        self.ui.Info_Text.setPlainText("保存成功")

    def Delete_Template(self):
        pass
    def Select_Template(self):
        if self.ui.Static_Text.isEnabled()==True:
            self.Val_Init()
            self.ui.Static_Text.setEnabled(False)
            self.ui.Variable_Text.setEnabled(False)
            print(self.ischanged_text)
            if self.ischanged_text==True:
                self.static_text = self.ui.Static_Text.toPlainText()
                self.variable_text = self.ui.Variable_Text.toPlainText()
                self.deal_variable_text()
                print("this way")
                self.test_print()
            else:
                self.load_template()
            self.test_print()
            self.ui.Generate_Bt.setEnabled(True)
            self.ui.Copy_Next_Bt.setEnabled(True)
            self.ui.Copy_Pre_Bt.setEnabled(True)

        else:
            self.ui.Static_Text.setEnabled(True)
            self.ui.Static_Text.clear()
            self.ui.Variable_Text.setEnabled(True)
            self.ui.Variable_Text.clear()
            self.ischanged_text = False

            self.ui.Generate_Bt.setEnabled(False)
            self.ui.Copy_Next_Bt.setEnabled(False)
            self.ui.Copy_Pre_Bt.setEnabled(False)
        pass
    def Text_Changed(self):
        self.ischanged_text = True
        print("文本修改")
    
    #文件相关
    def load_template(self):
        self.Val_Init()
        name = self.ui.Template_comboBox.currentText()
        fname = 'Template'+name+'.txt'
        fname = os.path.join(Template_Path,fname)
        f = open(fname,'r')
        text = f.read()
        text_list = text.split('￥')
        self.static_text = text_list[0]
        self.variable_text = text_list[1]
        self.text_uadata()
        self.deal_variable_text()
        f.close()



    def get_template_list(self):
        for fname in os.listdir(Template_Path):
            if operator.eq(fname[-4:],'.txt') == False:
                continue
            name = fname[8:-4]
            self.ui.Template_comboBox.addItem(name)
        
    #显示相关
    def text_uadata(self):
        self.ui.Static_Text.setPlainText(self.static_text)
        self.ui.Variable_Text.setPlainText(self.variable_text)

    #测试函数
    def test(self):
        self.get_template_list()
        # self.load_template()
    def test_print(self):
        # print(self.cnt-1)
        # print(self.case_now)
        # print(self.dic_now)
        print(self.static_text)
        print(self.variable_text_list)
        print(self.each_rown)


        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwin = Main_Win()
    sys.exit(app.exec_())
    

