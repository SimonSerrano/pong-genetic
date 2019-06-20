import gym
import sys
import numpy
import cv2
import numpy as np
import math

def detect_props(state, last_bp):
        
        def remove_background(state):
            state[state == 144] = 0
            state[state == 72] = 0
            state[state == 17] = 0
            return state
        
        def crop(state):
            state = state[33:194]
            return state
        
        def paddle_position(state):
            state = state[:, 140:141]
            top, bottom = None, None
            for i in range(160):
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

        def ball_velocity(last_bp, bp):
            bv = 0
            if bp is not None and last_bp is not None:
                bv = math.sqrt(math.pow(bp[0]-last_bp[0],2)+math.pow(bp[1]-last_bp[1], 2))
            return bv

        def enemy_position(state):
            state = state[:, 16:17]
            top, bottom = None, None
            for i in range(160):
                if state[i][0][0] == 213 and top is None:
                    top = i
                elif (state[i][0][0] == 0 or i == 159) and top is not None:
                    bottom = i-1
                    break
            if(top is not None and bottom is not None):
                position = (top+bottom)/2
                return position
            return None


        state = crop(state)
        state = remove_background(state)
        pp = paddle_position(state)
        bp = ball_position(state)
        bv = ball_velocity(last_bp, bp)
        ep = enemy_position(state)
        return bp, pp, bv, ep

if __name__ == "__main__":
    env = gym.make('Pong-v0')
    state = env.reset()
    for t in range(100):
        env.render()
        state, reward, done,  _ = env.step(2)
        np.set_printoptions(threshold=sys.maxsize)
        print(detect_props(state, list([0, 0])))


    