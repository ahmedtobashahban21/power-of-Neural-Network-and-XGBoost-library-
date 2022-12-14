import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns 
from sklearn.preprocessing import StandardScaler  , LabelEncoder 
from sklearn.model_selection import train_test_split  , KFold 
from xgboost import XGBRegressor 
from sklearn.metrics import mean_squared_error


############################
import torch 
import torch.nn  as nn 
import torch.nn.functional as F 
import torch.optim as optim
from torch.utils.data import TensorDataset 
from torch.utils.data import DataLoader 


train_data = pd.read_csv('train.csv')
test_data  = pd.read_csv('test.csv')
sample     = pd.read_csv('sample_submission.csv')

train_data.head()
train_data.info()
train_data.nunique()


# date column 


train_data['date'] = pd.to_datetime(train_data['date'])
train_data['day']  = train_data['date'].dt.day
train_data['month']= train_data['date'].dt.month
train_data['year'] = train_data['date'].dt.year 
###################

test_data['date'] = pd.to_datetime(test_data['date'])
test_data['day']  = test_data['date'].dt.day
test_data['month']= test_data['date'].dt.month
test_data['year'] = test_data['date'].dt.year 
test_data.head()



train_data['year'].value_counts()
test_data['year'].value_counts()

### showing data
plt.figure(figsize=(5,5))
sns.barplot(train_data['year']   , train_data['num_sold']) 
plt.legend()
plt.show()


plt.figure(figsize=(5,5))
sns.barplot(train_data['month']   , train_data['num_sold']) 
plt.legend()
plt.show()


plt.figure(figsize=(10,5))
sns.barplot(train_data['product']   , train_data['num_sold']) 
plt.legend()
plt.show()


train_data.isna().sum()
test_data.isna().sum()

sum(train_data['num_sold'])

###Preprocessing data and Features Engineering


# year and month                             13625659
y17 = train_data[train_data['year']==2017]
y18 = train_data[train_data['year']==2018]
y19 = train_data[train_data['year']==2019]
y20 = train_data[train_data['year']==2020]

sum_17 =sum(y17['num_sold'])           # ------> 3112163  / 13625659 =  0.22 
sum_18 =sum(y18['num_sold'])           #-------> 3425424  / 13625659 =  0.25
sum_19 =sum(y19['num_sold'])           #-------> 3232879  / 13625659 =  0.23
sum_20 =sum(y20['num_sold'])           #-------> 3855193  / 13625659 =  0.30
train_data.groupby('year')
train_data['y_rate']=0
test_data['y_rate']=0

train_data['y_rate'].iloc[:17520]= 0.22
train_data['y_rate'].iloc[17520:35040]= 0.25
train_data['y_rate'].iloc[35040:52560]= 0.23
train_data['y_rate'].iloc[52560:]= 0.30                        
######################                                            
test_data['y_rate'].iloc[:4380]= 0.22
test_data['y_rate'].iloc[4380:8760]= 0.25
test_data['y_rate'].iloc[8760:13140]= 0.23
test_data['y_rate'].iloc[13140:]= 0.30

train_data['M_rate'] = 0
test_data['M_rate'] = 0

train_data.groupby('month')
test_data.groupby('month')


month_1 = train_data[train_data['month']==1]
month_2 = train_data[train_data['month']==2]
month_3 = train_data[train_data['month']==3]
month_4 = train_data[train_data['month']==4]
month_5 = train_data[train_data['month']==5]
month_6 = train_data[train_data['month']==6]
month_7 = train_data[train_data['month']==7]
month_8 = train_data[train_data['month']==8]
month_9 = train_data[train_data['month']==9]
month_10 = train_data[train_data['month']==10]
month_11 = train_data[train_data['month']==11]
month_12 = train_data[train_data['month']==12]


collection=[]
collection.append( sum(month_1['num_sold']) )  # 1244928 /13625659
collection.append(sum(month_2['num_sold'])  )  # 1086253 /13625659
collection.append(sum(month_3['num_sold'])  )  # 1147079 /13625659
collection.append(sum(month_4['num_sold'])  )  # 1076549 /13625659
collection.append(sum(month_5['num_sold'])  )  # 1142837 /13625659
collection.append(sum(month_6['num_sold'])  )  # 1088330 /13625659
collection.append(sum(month_7['num_sold'])  )  # 1109652 /13625659
collection.append(sum(month_8['num_sold'])  )  # 1115626 /13625659
collection.append( sum(month_9['num_sold']) )  # 1064882 /13625659
collection.append(sum(month_10['num_sold']) )  # 1119781 /13625659
collection.append(sum(month_11['num_sold']) )  # 1130230 /13625659
collection.append(sum(month_12['num_sold']) )  # 1299512 /1362565


month_rate = []
for i in range(12):
    sm = collection[i] /  13625659 
    month_rate.append(sm)
    
    
train_data['M_rate'].iloc[:5952]=0.091
train_data['M_rate'].iloc[5952:511376]=0.079
train_data['M_rate'].iloc[511376:17328]=0.084
train_data['M_rate'].iloc[17328:23088]=0.079
train_data['M_rate'].iloc[23088:29040]=0.083
train_data['M_rate'].iloc[29040:34800]=0.079
train_data['M_rate'].iloc[34800:40752]=0.081
train_data['M_rate'].iloc[40752:46704]=0.081
train_data['M_rate'].iloc[46704:52464]=0.078
train_data['M_rate'].iloc[52464:58416]=0.082
train_data['M_rate'].iloc[58416:64176]=0.082
train_data['M_rate'].iloc[64176:]= 0.095
############ rate is defferent beteween train and test data
test_data['M_rate'].iloc[:1460]=0.091
test_data['M_rate'].iloc[1460:2920]=0.079
test_data['M_rate'].iloc[2920:4380]=0.084
test_data['M_rate'].iloc[4380:5840]=0.079
test_data['M_rate'].iloc[5840:7300]=0.083
test_data['M_rate'].iloc[7300:8760]=0.079
test_data['M_rate'].iloc[8760:10220]=0.081
test_data['M_rate'].iloc[10220:11680]=0.081
test_data['M_rate'].iloc[11680:13140]=0.078
test_data['M_rate'].iloc[13140:14600]=0.082
test_data['M_rate'].iloc[14600:16060]=0.082
test_data['M_rate'].iloc[16060:]= 0.095


for df in [train_data, test_data]:
    for wd in range(7):
        df['wd_{}'.format(wd)] = (df['date'].dt.weekday == wd).astype('int')
    for m in range(1, 12):
        df['m_{}'.format(m)] = (df['date'].dt.month == m).astype('int')
    df['year'] = df['date'].dt.year
    df['sp_day'] = (df['date'].dt.month*100 + df['date'].dt.day).isin([101,1228,1229,1230,1231]).astype(int)
    
    
y = train_data['num_sold']
train_data = train_data.drop(['num_sold' , 'row_id' , 'date'] , axis=1) 
test_data  = test_data.drop(['row_id' , 'date'] , axis=1)
 
labels = ['country' , 'store' ,'product' ]

label_model = LabelEncoder()
for col in labels :
    train_data[col] = label_model.fit_transform(train_data[col])
    
for col in labels :
    test_data[col] = label_model.fit_transform(test_data[col])
        

## model 
X = train_data
X_test = test_data
X_train , X_valid , y_train , y_valid = train_test_split(X ,y ,test_size=0.3 , shuffle=True , random_state=44)


XGB_model  = XGBRegressor(n_estimators=1000,learning_rate=0.1,gamma=0.004 ,
                          reg_alpha=0.004 , reg_lambda=0.04)


# ********  trian and test model with multi learning rate to choise best one
# you can test to hold best one 
Kfold = KFold(n_splits=5 ,shuffle=True)
lr = 0.1
collect =[]
for i in range(3):
    XGB_model.learning_rate=lr
    print('******** session (' ,i+1 , ')***********')
    print('learning rate is : ' ,lr)
    print("\n")
    for epoch , (train_idx ,test_idx) in enumerate(Kfold.split(X ,y)):
        X_tr = X.iloc[train_idx] 
        X_val= X.iloc[test_idx]
        y_tr = y.iloc[train_idx]
        y_val= y.iloc[test_idx] 
        XGB_model.fit(X_tr , y_tr)
        predict = XGB_model.predict(X_val)
        MSE = mean_squared_error(predict , y_val)
        print(f'fold :{epoch+1} , MSE :{MSE}') 
        test_prediction =XGB_model.predict(X_test)
        collect.append(test_prediction)
    lr +=0.3


### Neural Network



X_tr  = torch.tensor(X_train.values , dtype =torch.float32)
X_val = torch.tensor(X_valid.values , dtype =torch.float32)
y_tr  = torch.tensor(y_train.values , dtype =torch.float32) 
y_val = torch.tensor(y_valid.values , dtype =torch.float32)
X_test_tensor = torch.tensor(X_test.values , dtype=torch.float32)
##############
train = TensorDataset(X_tr ,y_tr)
test  = TensorDataset(X_val ,y_val)
##############
train_loader = DataLoader(train ,batch_size=120 ,shuffle=True )
test_loader  = DataLoader(test , batch_size=120 , shuffle=True)


### model NN 
class NN(nn.Module):
    def __init__(self ,len_f):
        super(NN ,self).__init__()
        self.fc1 = nn.Linear(len_f,512)
        self.fc2 = nn.Linear(512 ,256)
        self.fc3 = nn.Linear(256 , 128)
        self.fc4 = nn.Linear(128 ,1)
        self.norm1 = nn.BatchNorm1d(512)
        self.norm2 = nn.BatchNorm1d(256)
        self.norm3 = nn.BatchNorm1d(128)
        #self.drop =  nn.Dropout(0.5)
        
    def forward(self , X):
        out = F.relu(self.norm1(self.fc1(X)))
        out = F.dropout(out ,training=self.training , p=0.5 )
        out = F.relu(self.norm2(self.fc2(out)))
        out = F.dropout(out ,training=self.training , p=0.5 )
        out = F.relu(self.norm3(self.fc3(out)))
        out = F.dropout(out ,training=self.training , p=0.5 )
        out = F.relu(self.fc4(out))
        return out
    
    
len_features = train_data.shape[1]
model = NN(len_features)
model.train()

# optimizer and loss funciton 
n_epochs   = 40 
lr = 0.01
optimizer  =optim.Adam(params=model.parameters() , lr=lr)
ceriterion = nn.MSELoss()


device = 'cuda' if torch.cuda.is_available() else 'cpu' 

## train_model 
for epoch in range(n_epochs):
    acc_total  =0 
    loss_total =0
    
    if epoch in (20 , 50):
        lr=lr/10
        
    optimizer.lr=lr
    # train 
    for data ,label in train_loader :
        data= data.view(-1,27)
        out = model(data).to(device) 
        lab = label.view(-1,1).to(device) 
        loss = ceriterion(out ,lab) 
        
        #### backward 
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        accuracy = ((out.argmax(dim=1)==lab).float().mean())
        acc_total+=accuracy / len(train_loader)
        loss_total+= loss / len(train_loader) 
    print(f'epoch :{epoch} , train_accuracy :{acc_total} , train_loss :{loss_total} , lr :{lr}')
    test_acc=0 
    test_loss =0
    with torch.no_grad():
        for data2 , label2 in test_loader :
            data2 = data2.view(-1 ,27)
            output = model(data2).to(device)
            lab2 = label2.view(-1,1).to(device) 
            loss2 = ceriterion(output , lab2)
            acc = ((output.argmax(dim=1)==lab2).float().mean())
            test_acc+= acc / len(test_loader)
            test_loss += loss /len(test_loader)
            
           
    print(f'epoch :{epoch} , test_accuracy :{test_acc} ,test_loss :{test_loss} , lr :{lr}')
    print('******************************************')
    print('\n')


test_prerdict_2 = model(X_test_tensor).detach().numpy()
test_prerdict_2[:20]







