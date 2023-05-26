from sympy import *  #tien hanh import cac thu vien syspy va gym de thuc hien duọc cac gym environment AI
import gym

if __name__ == "__main__":
    environment = gym.make("MountainCar-v0")
    # environment = gym.make("Acrobot-v1")
    # environment = gym.make("FrozenLake-v1")     
                                         #tien hanh chon mot gym environment
                                         #tao ra mot constructor tuong ung voi environment ma minh da chon, vi du trong truong hop nay la MountainCar-V0
    observation=environment.reset()   #tien hanh reset lai state ban dau cua enviroment

    total_reward = 0  #khoi tao tong diem thuong bang 0, cu sau moi episode, total reward se duoc cap nhat
    while True:
        rand_action = environment.action_space.sample()  # chon ra 1 action ngau nhien ma agent co the thuc hien
        current_obs, current_reward, state_done, _ = environment.step(rand_action)   #ham env.step se nhan action vua moi duoc chon la input, tra ve 4 gia tri: observation, reward, done, info
                                                # +) observation la trang thai cua environment khi thuc hien action
                                                # +) reward: khi thuc hien xong 1 action thi agent duoc thuong bao nhieu diem
                                                # +) done: co kieu du lieu bool, tra ve true khi episode da ket thuc, bao hieu viec reset lai environment

        print("Action:")  #sau khi thuc hien 1 action, tien hanh ghi lai thuoc tinh cua no cung voi diem thuong va observation sau khi thuc hien xong 1 cation
        print(rand_action)
        print("Reward: %.2f. Observation: " %(current_reward))
        print(current_obs)

        environment.render()   #sau khi thuc hien xong 1 action, 1 cua so se duoc bat len de hien thi action moi duoc thuc hien

        total_reward += current_reward  #tien hanh cap nhat tong diem thuong sau moi lan thuc hien 1 action

        if state_done:           #neu done la true, co nghia episode da ket thuc, thi tien hanh dong environment va thoat khoi vong lap
            environment.close()
            break
    print("Done. Total_reward: ", total_reward)  #in ra tong diem thuong de biet episode do la tot hay xau