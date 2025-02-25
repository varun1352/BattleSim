# BattleSim
Hi everyone, I am still setting up a lot of things, fixing a lot of bugs and waiting for OpenAI to refresh my rate limit for o3-mini-high so I can squash some weird bugs. But heres a conceptual of what I am working on right now. 

**Strategy simulator for Zero-sum Games(Battleship)**
Almost all Zero-sum games have some sort of strategy in play, because at the end of the day, we want to min-max our odds and win. Battleship is one of those z-s games. I aim to develop a system where we can test strategies for such games. I picked battleship because it is comparatively easier to emulate but still more complex than something like tic-tac-toe, where theres a high chance of draws and much lesser randomness. 

The system works with 2 agents(llama3.1-8b) playing each other where the task is to maximize the chance of wining using the strategy mentioned by the user and in the case of no strategy, go with the system prompted strategy(asked llama to write me strategy to win battleship). And with the help of cerebras I can simulate the gameplay, and the interaction between these agents and the game environment where they **Try to Win**

Once again, still a lot of bugs and a lot of issues, but heres the github repo for the code if anybody wants to check it out(will be changed extensively once I make my final commit tonight)
