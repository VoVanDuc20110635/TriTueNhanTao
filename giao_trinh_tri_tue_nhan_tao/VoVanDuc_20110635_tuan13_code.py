
import gym 
import numpy as np

import torch 
import torch.nn as nn
import torch.optim as optim 
import time 
from collections import namedtuple


model = 3
if model == 1:
    HIDDEN_SIZE = 128
    BATCH_SIZE = 16
    PERCENTILE = 70

if model == 2:
    HIDDEN_SIZE = 50
    BATCH_SIZE = 10
    PERCENTILE = 80    

if model == 3:
    HIDDEN_SIZE = 10  #la so luong neural trong hidden layer, o day chi su dung 1 hidden layer
    BATCH_SIZE = 10 # khi training tren neural network, mot lan chung se lay ra 16 episode de huan lien
    PERCENTILE = 80    # la ti le episode ma co total reward lon hon total reward cua boundary 

class Net(nn.Module): #dung de xay dung mot mang neural network,
    def __init__(self, obs_size, hidden_size, n_actions):  #nhan vo construction co cac paramater, voi obs_size la so luong observation, hidden_size: so luong neural cua mot hidden layer, n_actions: so luong neural cua output
        super().__init__() #goi lai constructor cua lop nn.Module
        self.net = nn.Sequential(   #sqquential la mang chay tu trai sang phai 
            nn.Linear(obs_size, hidden_size),
            nn.ReLU(),  #la ham activation solution de be cong duong thang
            nn.Linear(hidden_size, n_actions)  #hidden_size trong truong hop nay la so luong neural cua hidden layer; n_actions la so luong neuron o output layer
            )                                   #xac suat khuyen egent nen chon action nao trong ouput layer
    def forward(self, x):   #ham tien hanh tra ve dau ra output layer, la su ket hop cua cac net outcome
        return self.net(x)

Episode = namedtuple('Episode', field_names = ['reward', 'steps'])  #namedtuple giong nhu mot dictionary, thuoc thu vien collection, chua 2 thong tin: reward: diem dat duoc va steps: action, voi moi action se tuong ung voi 1 reward
EpisodeStep = namedtuple('EpisodeStep', field_names = ['observation', 'action'])  #1 step chua 2 thong tin: observation va action


def get_batches(env, net, batch_size):  #ham dung de cho agent chay, dua vao environment, model, batch_size)
    batch = []  #luu lai thong tin cua tung episode, ghi lai thong tin cua cac episode da duoc huan luyen

    episode_reward = 0.0 #thiet lap diem thuong cho episode = 0
    episode_steps = []  #step cho tung episode la rong

    obs = env.reset()  #reset lai environmentt
    sm = nn.Softmax(dim=1) #thiet lap so chieu cua mot softmax
    while True:
        obs_v = torch.FloatTensor([obs]) #ham FloatTensor([obs]) tra ve gia tri co ban chat la mot mang se tra mot mang nhung mang nay chay duoc nhanh hon so voi mang mac dinh
        act_probs_v = sm(net(obs_v)) #tinh ra xac suat cho tung action
        act_probs = act_probs_v.data.numpy()[0] #ep kieu floattensor thanh kieu mang binh thuong
        action = np.random.choice(len(act_probs), p=act_probs) #chon 1 action ngau nhien tu act_probs 

        next_obs, reward, is_done, _ = env.step(action)  #env.step(antion) se tra ve obversation tiep theo, diem thuong da tich duoc va trang thai xem episode ket thuc hay chua

        episode_reward += reward #tong reward cua mot episode bang tong chinh no voi reward moi thu duoc 
        step = EpisodeStep(observation=obs, action=action) 
        episode_steps.append(step)
        
        if is_done: #neu xong roi thi
            e = Episode(reward=episode_reward, steps=episode_steps) #tao ra mot bien episode
            batch.append(e)  # dua bien episode moi tao ra vao viej huan luyen
            
            episode_reward = 0.0  # khoi tao lai episode_rewrd = 0
            episode_steps = []
            next_obs = env.reset()

            if len(batch) == batch_size: #khi chung ta chay xong so luong bench_size episode
                yield batch  #
                batch = []
        obs = next_obs  #neu chua xong thi hang obversation co gia bang observation ma ham next_obs tra ve

def filter_batch(batch, percentile):
    rewards = list(map(lambda s: s.reward, batch)) #batch - reward, map: lay tung ra tung phan t
    reward_bound = np.percentile(rewards, percentile) # lien he weraed va percontuile
    
    reward_mean = float(np.mean(rewards)) #sau moi chay, ghi lai ket qua

    #chieu du lieu open va change 
    train_obs = []
    train_act = []
    for reward, steps in batch:
        if reward < reward_bound:  #tien hanh bo nhung episode co total reward < boundry
            continue
        train_obs.extend(map(lambda step: step.observation, steps)) #lay tung step, lay ra abservatio va dua vao train_obs
        train_act.extend(map(lambda step: step.action, steps))  #lay ra het action thuoc ting step

    train_obs_v = torch.FloatTensor(train_obs)
    train_act_v = torch.LongTensor(train_act)
    return train_obs_v, train_act_v, reward_bound, reward_mean


if __name__ == "__main__":
    #env = gym.make("CartPole-v1")  
    env = gym.make("MountainCar-v0")  #tao ra environment
    
    #train_mode = True
    train_mode = False
    if train_mode:
        obs_size = env.observation_space.shape[0] 
        n_actions = env.action_space.n
        net = Net(obs_size, HIDDEN_SIZE, n_actions) #tao mot mang net
        
        objective = nn.CrossEntropyLoss() #chi hinh 1 ham CrossEntroyLoss de giai thich thuat toan
        optimizer = optim.Adam(params=net.parameters(), lr=0.01) #
        
        for iter_no, batch in enumerate(get_batches(env, net, BATCH_SIZE)):  #iter_no la so luong episode   
            obs_v, acts_v, reward_b, reward_m = filter_batch(batch, PERCENTILE)  #lay duoc cac obvation toat, actions tot, reward tot
            
            optimizer.zero_grad()   #khoi tao 
            action_scores_v = net(obs_v)  #input la observaton cho ham network va tra ve  xac suat bai toan chpon action do
            loss_v = objective(action_scores_v, acts_v)  #diem diem sac xuat va action tuong ung da lam, khi gop 2 cai nay thi thuat toan dung bao nhieu sai bao nhieu
            loss_v.backward() #bat dau huan lien
            optimizer.step()

            print("%d: loss=%.3f, reward_mean=%.1f, reward_bound=%.1f" % (iter_no, loss_v.item(), reward_m, reward_b))
        
            if reward_m > 499: # neu reward < 499 thi bao toan chua duoc giai
                torch.save(net,'trained_net_' + str(HIDDEN_SIZE) + 'neurons.pt') # qNOTE: save ONLY 1 var/file
                print("Solved! Saved the model.")
                break

    else: # use the trained network
        env = gym.wrappers.Monitor(env, directory="solved_cartpole", force=True)
        obs = env.reset()

        #net = torch.load('trained_net_' + str(HIDDEN_SIZE) + 'neurons.pt')
        net = torch.load('trained_net_LunarLander-v2_20neurons.pt')
       
        sm = nn.Softmax(dim=1)
        total_reward = 0
        while True:
            obs_v = torch.FloatTensor([obs])
            act_probs_v = sm(net(obs_v)) 
            act_probs = act_probs_v.data.numpy()[0]
            action = np.random.choice(len(act_probs), p=act_probs)

            obs, reward, done, _ = env.step(action)
            
            env.render()
            #time.sleep(0.01)
            total_reward += reward

            if done:
                env.close()
                break

        print("Model %d (%d neurons). Total reward: %.2f" % (model, HIDDEN_SIZE, total_reward))

