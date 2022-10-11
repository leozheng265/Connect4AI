# Connect 4 AI

## Introduction

This project implemented two AI agents with minimax and alpha-beta pruning algorithms that is able to play Connect 4. 

An AI player that chooses moves randomly and an AI player based on monte carlo tree search are also included for testing purposes.

## Running Instructions

- -p1 Agent that will be playing as player 1. Default human.
- -p2 Agent that will be playing as player 2. Default human.
- -seed seed for stochastic elements. Default 0.
- -w Rows of gameboard. Default 6.
- -l Columns of gameboard. Default 7.
- -visualize enable visualization of the game. Default True.
- -verbose print the gameboard to terminal. Default False.
- -time_limit time limit to make a move. Default 0.5, 0.5.
- -limit_players apply time limit to players. Default 1, 2.
- To let two AIs play against each other:
    
    ```bash
    python3 main.py -p1 minimaxAI -p2 montecarloAI
    ```
    
- To play against an AI player:
    
    ```bash
    python3 main.py -p1 minimaxAI -limit_players 1 -visualize True
    ```

## Demo video:

https://youtu.be/cYOIS4imYS0
