Two Flags Game:

Using ai concepts and algorithm we created a Chess game with only bishops that uses ai algorithms to detirmine its next move.

This project uses a tcp/ip connection to a server and sends the moves to a local server to allow an apponent to play against the ai and also allows a human player to play against the ai with no server needed meaning on the same GUI
Algorthims and Data Structures used :
  * Nega-MinMax
  * Zubrist hash keys and table
  * Evaluation Funcitons 
  * Bitbaords for faster performance 
  * masks for those bitboards for attaks 
  
* Moves were done using bit wise &,XOR,OR,AND operations on the board.
* an improvement on this implementation would be to use Quiesce algorithm that tries all possible "attackes" until it either gets defeated or wins , and then adds a score to the zubrist hash tables .  

* There is an exe file in the repositry with the full game , no need for installation/creating the exe file.
  
GUI :
![image](https://github.com/AbednAboH/Two_Flags_Game/assets/92520508/7408989f-e56a-48fb-a0ce-b04fd0a53c7d)


![image](https://github.com/AbednAboH/Two_Flags_Game/assets/92520508/8d00eae2-a8c5-4294-b37b-65f3efe0e122)


![image](https://github.com/AbednAboH/Two_Flags_Game/assets/92520508/b03ccc7d-f6e4-4794-be00-d31a24fd093a)



