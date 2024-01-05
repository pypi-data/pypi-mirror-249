from BaseNN import nn,pth_info
import torch
import numpy as np
import cv2
import os
from tqdm import tqdm


def load_image_data_mn():

    model = nn()
    # model.set_seed(123465)

    a = model.load_img_data("/home/user/桌面/BaseNN004/dataset/cls/mnist/training_set",
                             data_type='image_folder',color="grayscale",batch_size=60000)
    model.add('Conv2D', size=(1, 6),kernel_size=( 5, 5), activation='ReLU') # 60000 * 3456(6 * 24 * 24)
    model.add('AvgPool', kernel_size=(2,2)) # 60000 * 864(6 * 12 * 12)
    model.add('Conv2D', size=(6, 16), kernel_size=(5, 5), activation='ReLU') # 60000 * 1024(16 * 8 * 8)
    model.add('AvgPool', kernel_size=(2,2)) # 60000 * 256(16 * 4 * 4)
    model.add('Linear', size=(256, 120), activation='ReLU')  # 60000 * 256
    model.add('Linear', size=(120, 84), activation='ReLU') 
    model.add('Linear', size=(84, 10), activation='Softmax')
    model.add(optimizer='SGD')
    model.save_fold = 'new_mn_ckpt'
    model.train(lr=0.01, epochs=2)#, checkpoint="new_mn_ckpt/basenn.pth") # 直接训练
    a = "../../dataset/cls/mnist/val_set/4/85.png"
    b = "../../dataset/cls/mnist/val_set/4"
    result = model.inference(data=a, checkpoint="new_mn_ckpt/basenn.pth")
    print("pth res",result)
    model.print_result()
    model.convert(checkpoint="new_mn_ckpt/basenn.pth", out_file="basenn_mn.onnx",ir_version=3)

def load_image_data_cd():
    from torchvision.transforms import transforms
    model = nn()
    # model.set_seed(123465)
    # tran = transforms.Resize([128,128])
    # classes = {0:"cat", 1:"dog"}
    # d = model.load_img_data("/home/user/桌面/BaseNN004/dataset/cls/cats_dogs_dataset/CatsDogs (1)/CatsDogs/training_set",
    #                          color="RGB",batch_size=2000, transform=tran,classes=classes)
    
    # for x, y in d:
    #     print(x.shape)
    # model.add('Conv2D', size=(3, 6),kernel_size=( 5, 5), activation='ReLU') # 60000 * 3456(6 * 24 * 24)
    # model.add('AvgPool', kernel_size=(2,2)) # 60000 * 864(6 * 12 * 12)
    # model.add('Conv2D', size=(6, 16), kernel_size=(5, 5), activation='ReLU') # 60000 * 1024(16 * 8 * 8)
    # model.add('AvgPool', kernel_size=(2,2)) # 60000 * 256(16 * 4 * 4)
    # model.add('Linear', size=(13456, 120), activation='ReLU')  # 60000 * 256 13456
    # model.add('Linear', size=(120, 10), activation='ReLU') 
    # model.add('Linear', size=(10, 2), activation='Softmax')
    # model.add(optimizer='SGD')
    # model.save_fold = 'new_cd_ckpt'
    # model.train(lr=0.001, epochs=100)# 直接训练
    # test_x, y = read_data("../../dataset/cls/mnist/val_set")
    # print(y[1000:1100])
    a = "/home/user/桌面/BaseNN004/dataset/cls/cats_dogs_dataset/CatsDogs (1)/CatsDogs/val_set/dog"
    b = "/home/user/桌面/BaseNN004/dataset/cls/cats_dogs_dataset/CatsDogs (1)/CatsDogs/val_set/cat/cat1.jpg"
    from PIL import Image
    im = Image.open(b)
    bb = np.array(im)
    result = model.inference(data=b, checkpoint="new_cd_ckpt/basenn.pth")
    print("result",result)
    model.print_result()

    model.convert(checkpoint="new_cd_ckpt/basenn.pth", out_file="basenn_cd.onnx")

def load_tab_data_iris():
    import time
    model = nn()
    # 训练数据
    train_path = '../../dataset/iris/iris_training.csv'
    # x = np.loadtxt(train_path, dtype=float, delimiter=',',skiprows=1,usecols=range(0,4)) # [120, 4]
    # y = np.loadtxt(train_path, dtype=int, delimiter=',',skiprows=1,usecols=4)
    model.load_tab_data(train_path, batch_size=200000)

    model.add(layer='Linear',size=(4, 10),activation='ReLU') # [120, 10]
    model.add(layer='Linear',size=(10, 5), activation='ReLU') # [120, 5]
    model.add(layer='Linear', size=(5, 3), activation='Softmax') # [120, 3]
    model.save_fold = 'iris_ckpt'
    # a = time.time()
    model.train(lr=0.01, epochs=100)
    # print(time.time() - a)
    # print(model.device)
    # model.print_model()
    test_path = '../../dataset/iris/iris_test.csv'
    x = np.loadtxt(test_path, dtype=float, delimiter=',',skiprows=1,usecols=range(0,4)) # [120, 4]
    # y = np.loadtxt(test_path, dtype=int, delimiter=',',skiprows=1,usecols=4)
    # # print(y)
    print(x)
    res = model.inference(x,label=True, checkpoint="iris_ckpt/basenn.pth")
    print(res)
    model.convert(checkpoint="iris_ckpt/basenn.pth", out_file="basenn_iris.onnx")

def load_npz_data_action():
    # 读取数据
    X = np.load("/home/user/桌面/BaseNN004/BaseNN/examples/human_action_recognition-main/X1.npy",allow_pickle = True)
    y = np.load("/home/user/桌面/BaseNN004/BaseNN/examples/human_action_recognition-main/y1.npy", allow_pickle = True)    
    X = np.load("./conbined.npz")["data"]
    # print(X,X.shape)
    # print(X.shape)
    # np.savez("conbined.npz", data=X, label=y)
    # a = np.load("conbined.npz")
    # print(a['label'].shape)
    # train_x,train_y = X,y.astype(np.float32)
    test_x, test_y = X[28:38,:,:], y[28:38,:].astype(np.float32)
    # print(X.shape,test_x.shape, test_y.shape,test_y)
    # # 搭建模型
    model = nn()
    model.load_npz_data("./conbined.npz",batch_size=50,classes=["a", "b", "c"])
    # model.add('lstm', size=(132,128))
    # model.add('Dropout',p=0.2)
    model.add('lstm', size=(132,256))
    model.add('Dropout',p=0.2)
    # model.add('unsqueeze')
    model.add('lstm', size=(256,256))
    # model.add('squeeze')
    model.add(dim2())
    model.add('BatchNorm1d', size=256)              
    # model.add('action_model',size=(132,256))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    model.add('linear',  size=(256, 256))
    model.add('Linear',  size=(256, 128))
    model.add('linear',  size=(128, 64))
    model.add('Linear',  size=(64, 3))
    model.add(activation='Softmax')
    model.save_fold = "action_ckpt2"
    model.train(lr=0.01, epochs=10,loss="BCELoss",metrics=[])

    res = model.inference(test_x, checkpoint="action_ckpt2/basenn.pth")
    print(test_y)
    print(res)
    model.print_result()

    model.convert(checkpoint="action_ckpt2/basenn.pth", out_file="basenn_act.onnx")

def load_npz_data_tang():
    # 读取数据
    datas = np.load('tangccc.npz',allow_pickle=True)
    data = datas['data'] 
    print("第一条数据：",data[0]) # 观察第一条数据
    word2ix = datas['word2idx'].item() # 汉字对应的索引
    # print(data.shape)
    # print(word2ix)
    # x, y = data[:,:-1], data[:, 1:]

    # np.savez("tangccc.npz", data=x, label=y, word2idx=word2ix)

    # print("词表:",word2ix) 
    # ix2word = datas['ix2word'].item() # 索引对应的汉字

    model = nn()
    # model.load_dataset(x, y, word2idx=word2ix) # 载入数据
    model.load_npz_data('tangccc.npz', batch_size=128)
    # model.add('em_LSTM', size=(128,256),num_layers=2) 
    # model.save_fold = '111ckpt'
    # model.train(lr=0.005, epochs=1,checkpoint='111ckpt/basenn.pth')

    model.convert(checkpoint="111ckpt/basenn.pth", out_file="basenn_tang.onnx",opset_version=12)


def cal_accuracy(y, pred_y):
    res = pred_y.argmax(axis=1)
    print(res, y)
    tp = np.array(y)==np.array(res)
    acc = np.sum(tp)/ y.shape[0]
    return acc

def read_data(path):
    data = []
    label = []
    dir_list = os.listdir(path)

    # 将顺序读取的文件保存到该list中
    for item in dir_list:
        tpath = os.path.join(path,item)

        # print(tpath)
        for i in os.listdir(tpath):
            # print(item)
            img = cv2.imread(os.path.join(tpath,i))
            imGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # print(img)
            data.append(imGray)
            label.append(int(item))
    x = np.array(data)
    y = np.array(label)

    x = np.expand_dims(x, axis=1)
    return x, y

def visual_feature_demo():
    # 读取数据
    train_x, train_y = read_data("../../dataset/cls/mnist/training_set")
    model = nn() #声明模型 
    model.load_dataset(train_x, train_y) # 载入数据
    model.add('Conv2D', size=(1, 6),kernel_size=( 5, 5), activation='ReLU') # 60000 * 3456(6 * 24 * 24)
    model.add('AvgPool', kernel_size=(2,2)) # 60000 * 864(6 * 12 * 12)
    model.add('Conv2D', size=(6, 16), kernel_size=(5, 5), activation='ReLU') # 60000 * 1024(16 * 8 * 8)
    model.add('AvgPool', kernel_size=(2,2)) # 60000 * 256(16 * 4 * 4)
    model.add('Linear', size=(256, 120), activation='ReLU')  # 60000 * 256
    model.add('Linear', size=(120, 84), activation='ReLU') 
    model.add('Linear', size=(84, 10), activation='Softmax')
    model.add(optimizer='SGD')
    model.save_fold = 'mn_ckpt'
    checkpoint = 'mn_ckpt/basenn.pth'
    # model.train(lr=0.1, epochs=30, checkpoint=checkpoint) # 继续训练
    # model.train(lr=0.1, epochs=1) # 直接训练

    img = cv2.imread("/home/user/桌面/pip测试7/dataset/cls/mnist/test_set/0/0.png", cv2.IMREAD_GRAYSCALE)

    model.visual_feature(img, in1img=True)

def extract_feature_demo():
    img = cv2.imread("/home/user/桌面/pip测试7/dataset/cls/mnist/test_set/0/0.png")
    model = nn()
    f1 = model.extract_feature(img, pretrain='resnet34')
    print(f1.shape, f1)
    return f1

class LSTM_model(torch.nn.Module):
    def __init__(self, actions):
        super(LSTM_model, self).__init__()

        self.actions = actions

        self.lstm1 = torch.nn.LSTM(132, 128, batch_first=True, bidirectional=False)
        self.dropout1 = torch.nn.Dropout(0.2)
        self.lstm2 = torch.nn.LSTM(128, 256, batch_first=True, bidirectional=False)
        self.dropout2 = torch.nn.Dropout(0.2)
        self.lstm3 = torch.nn.LSTM(256, 256, batch_first=True, bidirectional=False)
        self.bn = torch.nn.BatchNorm1d(256)
        self.dense1 = torch.nn.Linear(256, 256)
        self.dense2 = torch.nn.Linear(256, 128)
        self.dense3 = torch.nn.Linear(128, 64)
        self.dense4 = torch.nn.Linear(64, actions.shape[0])
        self.softmax = torch.nn.Softmax(dim=1)

    def forward(self, x):
        x, _ = self.lstm1(x)
        x = self.dropout1(x)
        x, _ = self.lstm2(x)
        x = self.dropout2(x)
        x, _ = self.lstm3(x[:, -1, :].unsqueeze(1))
        x = self.bn(x.squeeze())
        x = self.dense1(x)
        x = self.dense2(x)
        x = self.dense3(x)
        x = self.dense4(x)
        x = self.softmax(x)

        return x
def user_defined_demo():
    from BaseNN import nn as bnn
    # 读取数据
    X = np.load("/home/user/桌面/BaseNN004/BaseNN/examples/human_action_recognition-main/X1.npy",allow_pickle = True)
    y = np.load("/home/user/桌面/BaseNN004/BaseNN/examples/human_action_recognition-main/y1.npy", allow_pickle = True)    
    print(y.shape)
    train_x,train_y = X,y.astype(np.float32)
    # 自定义一个mylstm模型
    actions = np.array(["walking","boxing","handwaving"])
    mylstm = LSTM_model(actions)
    # 声明模型
    model = bnn()
    model.load_dataset(train_x, train_y)
    model.add(mylstm)
    model.save_fold = "action_ud"
    model.train(lr=0.01, epochs=200,loss="BCELoss",metrics=[])

class MyUnsqueeze(torch.nn.Module):
    def __init__(self, *args):
        super(MyUnsqueeze, self).__init__()

    def forward(self, x):
        # print("unsqueeze",type(x), type(x[:, -1, :].unsqueeze(1)))
        return x[:, -1, :].unsqueeze(1)
    
class MySqueeze(torch.nn.Module):
    def __init__(self, *args):
        super(MySqueeze, self).__init__()

    def forward(self, x):
        return x.squeeze()

class dim2(torch.nn.Module):
    def __init__(self, *args):
        super(dim2, self).__init__()

    def forward(self, x):
        return  x[:, -1, :]

def data_define_demo():
    # 读取数据
    X = np.load("/home/user/桌面/BaseNN004/BaseNN/examples/human_action_recognition-main/X1.npy",allow_pickle = True)
    y = np.load("/home/user/桌面/BaseNN004/BaseNN/examples/human_action_recognition-main/y1.npy", allow_pickle = True)    

    train_x,train_y = X,y.astype(np.float32)
    test_x, test_y = X[28:38,:,:], y[28:38,:].astype(np.float32)
    # print(X.shape,train_x.shape, train_y.shape)
    # 搭建模型
    model = nn()
    model.load_dataset(train_x, train_y)
    model.add('lstm', size=(132,128))
    model.add('Dropout',p=0.2)
    model.add('lstm', size=(128,256))
    model.add('Dropout',p=0.2)
    model.add(MyUnsqueeze())
    model.add('lstm', size=(256,256))
    model.add(MySqueeze())
    model.add('BatchNorm1d', size=256)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
    model.add('Linear',  size=(256, 256))
    model.add('Linear',  size=(256, 128))
    model.add('linear',  size=(128, 64))
    model.add('Linear',  size=(64, 3))
    model.add(activation='Softmax')
    model.save_fold = "action_ckpt1"
    log = model.train(lr=0.01, epochs=200,loss="BCELoss",metrics=[])
    print(log)

def tang_infer():
    from BaseNN import nn
    model = nn()

    input = '长'
    checkpoint = '111ckpt/basenn.pth'
    output, hidden = model.inference(data=input,checkpoint=checkpoint) # output是多维向量，接下来转化为汉字
    print("output: ",output)
    index = np.argmax(output) # 找到概率最大的字的索引
    w = model.ix2word[index] # 根据索引从词表中找到字
    print("word:",w)

def npz2csv(npz_file,csv_file):
    datas = np.load(npz_file,allow_pickle=True)
    data = datas['data'] 
    word2idx = datas['word2idx'].item() # 汉字对应的索引
    idx2word = dict(zip(word2idx.values(),word2idx.keys()))
    from tqdm import tqdm
    import csv

    with open(csv_file,'w') as f:
        writer = csv.writer(f)
        for line in tqdm(data):
            verse = ""
            for w in line:
                if idx2word[w] not in ['</s>','<START>']:
                    verse += idx2word[w]
            writer.writerow([verse])
    # np.savetxt("tangccc.csv",np.array(content),encoding='utf-8')

def npz2txt(npz_file,txt_file):
    datas = np.load(npz_file,allow_pickle=True)
    data = datas['data'] 
    print(data.shape)
    # print("第一条数据：",data[0]) # 观察第一条数据
    word2idx = datas['word2ix'].item() # 汉字对应的索引
    idx2word = dict(zip(word2idx.values(),word2idx.keys()))
    with open(txt_file,'w',encoding='utf-8') as f:
        for line in tqdm(data):
            verse = ""
            for w in line:
                if idx2word[w] not in ['</s>','<START>']:
                    verse += idx2word[w]
            f.write(verse +'\n')

def txt2npz(txt_file,npz_file, token_size = 125):
    with open(txt_file,'r') as f:
        content = f.readlines()
        content = [i.rstrip('\n') for i in content]
        words = set() # 词表
        for verse in content:
            for w in verse:
                words.add(w)
        word2idx = {w:i for i,w in enumerate(words)}
        start = len(words) + 1
        # eop = len(words) + 2
        s = len(words) +3
        data = []
        for verse in tqdm(content):
            verse_l = [start]
            for w in verse:
                verse_l.append(word2idx[w])
            # v_l.append(eop)
            if len(verse_l) > token_size:
                verse_l = verse_l[:token_size]
            else:
                for _ in range(token_size- len(verse_l)):
                    verse_l.insert(0,s)
            data.append(verse_l)
        x, y = np.array(data)[:,:-1], np.array(data)[:, 1:]
        print("词表大小：",len(words))
        print("数据集大小：",x.shape[0])
        np.savez(npz_file, data=x, label=y, word2idx=word2idx)
        print("转化成功！保存为：",npz_file)

def resnet_mn():
    model = nn()
    # model.set_seed(123465)
    from torchvision.transforms import transforms
    tran = transforms.Resize([224,224])
    a = model.load_img_data("/home/user/桌面/BaseNN004/dataset/cls/mnist/training_set",
                            batch_size=32,transform=tran,num_workers=1)
    # model.add('Conv2D', size=(1, 6),kernel_size=( 5, 5), activation='ReLU') # 60000 * 3456(6 * 24 * 24)
    model.add('Conv2D', size=(3, 64), kernel_size=(7, 7),stride=2,padding=3, activation='ReLU') # 60000 * 1024(16 * 8 * 8)
    model.add('BatchNorm2d', size=64)
    model.add('MaxPool', kernel_size=(3,3),stride=2,padding=1) # 60000 * 256(16 * 4 * 4)

    model.add('Res_Block', size=(64, 64), num_blocks=2,stride=1)
    model.add('Res_Block', size=(64, 128), num_blocks=2,stride=2)
    model.add('Res_Block', size=(128, 256), num_blocks=2,stride=2)
    model.add('Res_Block', size=(256, 512), num_blocks=2,stride=2)



    model.add('AvgPool', kernel_size=(7,7)) # 60000 * 864(6 * 12 * 12)
    model.add('Linear', size=(512, 10), activation='Softmax')

    model.add(optimizer='SGD')
    model.save_fold = 'new_mn_ckpt'
    import time
    a = time.time()
    model.train(lr=0.01, epochs=1) # 直接训练
    print(time.time() - a)
    a = "../../dataset/cls/mnist/val_set/4/85.png"
    b = "../../dataset/cls/mnist/val_set/4"
    result = model.inference(data=a, checkpoint="new_mn_ckpt/basenn.pth")
    print("pth res",result)
    model.print_result()
    # model.convert(checkpoint="new_mn_ckpt/basenn.pth", out_file="basenn_mn.onnx",ir_version=3)

if __name__=="__main__":
    # load_image_data_mn()
    # load_image_data_cd()
    # load_tab_data_iris()
    # load_npz_data_action()
    # load_npz_data_tang()
    resnet_mn()
