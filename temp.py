import gym
import sys
import numpy
import cv2
import numpy as np

def remove_background(state):
    state[state == 144] = 0
    state[state == 72] = 0
    state[state == 17] = 0
    return state
        
def crop(state):
    state = state[34:193]
    return state

def paddle_position(state):
    state = state[:, 140:141]
    top, bottom = None, None
    for i in range(158):
        if state[i][0][1] == 186 and top is None:
            top = i
        elif (state[i][0][1] == 0 or i == 159) and top is not None:
            bottom = i-1
            break
    position = (top+bottom)/2
    return position

def ball_position(state):
    state = state[:, 40:140]
    gray_state = cv2.cvtColor(state, cv2.COLOR_BGR2GRAY)
    gray_state = np.float32(gray_state)
    corners = cv2.goodFeaturesToTrack(gray_state, 4, 0.01, 0)
    if(corners is not None and corners.size ==8) :
        tl, tr, bl, br = corners[0], corners[1], corners[2], corners[3]
        return ((br[0,0]+tl[0,0])/2, (br[0,1]+tl[0,1])/2)


if __name__ == "__main__":
    env = gym.make('Pong-v0')
    state = env.reset()
    for t in range(100):
        env.render()
        state, reward, done,  _ = env.step(2)
        np.set_printoptions(threshold=sys.maxsize)
        state = crop(state)
        state = remove_background(state)
        ball_position(state)
        printed = set()
        for i in range (158):
            for j in range(160):
                for k in range(3):
                    if(state[i, j, k] != 0 and i not in printed):
                        pass
                        #print(i)
                        #printed.add(i)
                
        print(paddle_position(state), "- paddle pos")


    