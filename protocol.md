# Protocol
## Default rules:
- all commands are upper case ascii
- all commands end in \n
- spaces are used for arguments
- No error codes

## Client commands:
OK //general acceptance of data  
HELLO [username] //initialization of connection
HOLD //tells the server to wait until player sends answer, server should hold completely  
MOVE [move coordinates] //sends move request (for coordinates see below)  
[ ACCEPT / DENY ] //for draw request  
DRAW //requests draw  
DISCONNECT //disconnects. If not after GAMEEND, server disconnects other player automatically

## Server commands:
OK  
ROLE [ WHITE / BLACK ] //assigns the role  
HOLD //client should actually completely hold until next command  
STARTGAME //starts the game  
YOURMOVE //its your move, results in player holding until user inputs move or draw  
BOARD [board layout] //sends the current board as a 8x8 matrix (see below)  
INVALID [reason] //for an invalid move
DRAW //draw request from other player  
GAMEEND [ WHITE / BLACK / DRAW ]  
DISCONNECT //disconnects the game  

## init:
Client: HELLO [username] //initialize handshake  
Server: ROLE [ WHITE / BLACK ] //confirm username and decide whether player is white or black (if player 1 -> white, if player 2 -> black)  
Client: OK  

## waiting:
SERVER: HOLD //waiting, until player 2 is ready or, if user is player, 2 until start of game

## player 2 joined:
Server: STARTGAME //start the game  
Client: OK //confirm (still awake)  
Server: BOARD [board layout, eg. 0010121320212223 … ] //send initial board layout  
Client: OK  

## your move:
Server: YOURMOVE //it’s your move  
Client: OK //waiting until player inputs move  
Client: MOVE [move operation, eg. 32 TO 34 ] //player inputted coordinate x to coordinate y  
Server: [ OK / INVALID ] //either confirms the move or invalidates (if invalid return to YOURMOVE)  
Server: BOARD //sends the updated board  
Client: OK //confirms the board  

## your move (decide to send draw request):
Client: DRAW  
Server: HOLD //sends draw request to other player and asks for draw accept  
Server [ YOURMOVE (denied draw request) / GAMEEND DRAW (accepted draw request) ]  

## enemy move:
Server: HOLD  
Server: BOARD //sends updated board with enemy move  
Client: OK  

## enemy move (draw request):
Server: DRAW  
Client: HOLD //waits for user input  
Client: [ DENY / ACCEPT ]  
Server: [ GAMEEND (if accepted) / HOLD (if denied) ]  

## game end:
Server: GAMEEND [ WHITE /BLACK /DRAW ] //the game ended with either white or black winning  
Client: OK //confirm the game end  

## client disconnects:
Client: DISCONNECT  
//connection closed


## Board layout (initial as example):
(Black side)  
```
[2223242526242322]  
[2121212121212121]  
[0000000000000000]  
[0000000000000000]  
[0000000000000000]  
[0000000000000000]  
[1111111111111111]  
[1213141516141312]  
```
(White side)  

Pieces: 1 byte   
first 4 bits are the player (0 is empty, 1 is white, 2 is black)  
Second 4 bits are the piece (0 is empty, 1 is pawn, 2 is rook, 3 is knight, 4 is bishop, 5 is queen, 6 is king)

## Move layout (moving whites rightmost pawn as example):
MOVE 82 TO 83

## Board coordinates:
(Black side)  
```
[1828384858687888]  
[1727374757677778]  
[1626364656667686]  
[1525354555657585]  
[1424344454647484]  
[1323334353637383]  
[1222324252627282]  
[1121314151617181]
```
(White side)  
