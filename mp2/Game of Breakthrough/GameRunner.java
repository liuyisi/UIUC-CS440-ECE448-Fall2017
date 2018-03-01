import java.util.Scanner;
/**
 * Created by liuyisi on 2017/10/21.
 */
public class GameRunner {
    public class GameRunner {
    public static void main(String[] args){
        ChessBoard chessBoard = new ChessBoard();
        System.out.println("start status");
        chessBoard.printBoard();
        System.out.println();

        int[] winnerCount = new int[3];

        for (int i = 0 ; i < 1 ; i ++ ){
            System.out.println("Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)");
            chessBoard = new ChessBoard();
            Player player1 = new Player(chessBoard,1,3,"offensive1",false);
            Player player2 = new Player(chessBoard,2,3,"offensive2",true);
            int winner = run(player1,player2,chessBoard);
            winnerCount[winner] ++;
        }

        System.out.println( "player 1 win : " + winnerCount[1] + " ,time");
        System.out.println( "player 2 win : " + winnerCount[2] + " ,time");

//        chessBoard = new ChessBoard();
//        System.out.println("Minimax (Offensive Heuristic 1) vs Alpha-beta (Offensive Heuristic 1)");
//        Player player1 = new Player(chessBoard,1,3,"offensive1",true);
//        Player player2 = new Player(chessBoard,2,3,"defensive1",true);
//        run(player1,player2,chessBoard);

//        System.out.println( "Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)" );
//        chessBoard = new ChessBoard();
//        player1 = new Player(chessBoard,1,3,"defensive1",true);
//        player2 = new Player(chessBoard,2,3,"defensive1",true);
//        run(player1,player2,chessBoard);

//        System.out.println( "Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)" );
//        chessBoard = new ChessBoard();
//        player1 = new Player(chessBoard,1,3,"defensive1",true);
//        player2 = new Player(chessBoard,2,3,"defensive1",true);
//        run(player1,player2,chessBoard);
//
//        System.out.println( "Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Offensive Heuristic 1)" );
//        chessBoard = new ChessBoard();
//        player1 = new Player(chessBoard,1,3,"defensive1",true);
//        player2 = new Player(chessBoard,2,3,"defensive1",true);
//        run(player1,player2,chessBoard);
//
//        System.out.println( "Alpha-beta (Defensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 1)" );
//        chessBoard = new ChessBoard();
//        player1 = new Player(chessBoard,1,3,"defensive1",true);
//        player2 = new Player(chessBoard,2,3,"defensive1",true);
//        run(player1,player2,chessBoard);
//
//        System.out.println( "Alpha-beta (Offensive Heuristic 2) vs Alpha-beta (Defensive Heuristic 2)" );
//        chessBoard = new ChessBoard();
//        player1 = new Player(chessBoard,1,3,"defensive1",true);
//        player2 = new Player(chessBoard,2,3,"defensive1",true);
//        run(player1,player2,chessBoard);
    }

    public static int run( Player player1 , Player player2 , ChessBoard chessBoard){
        int count = 0;
        int winner ;
        while ( (winner = chessBoard.getWinner()) == 0 ){
            count ++ ;
            if( count % 2 == 1 ){
                player1.move(chessBoard.board);
            }else {
                player2.move(chessBoard.board);
            }
//            chessBoard.printBoard();
//            System.out.println();
        }

        System.out.println("Winner is player:" + winner);
        System.out.println("move count: " + count);
        System.out.println("player 1:");
        System.out.println("expanded nodes: " + player1.expandedNumber + ", average number of nodes expanded per move: " + ( ((double)player1.expandedNumber) / player1.moveCount) + ", average amount of time to make a move:" + ( ((double)player1.timeUsed) / player1.moveCount) + " milliseconds" );

        for ( int i = 0 ; i < player1.expandedNumberWithDepth.length ; i ++ ){
            System.out.println( "level " + i +  " expanded nodes:" + (((double)player1.expandedNumberWithDepth[i])/player1.moveCount) );
        }

        System.out.println();
        System.out.println("player 2:");
        System.out.println("expanded nodes: " + player2.expandedNumber + ", average number of nodes expanded per move: " + ( ((double)player2.expandedNumber) / player2.moveCount) + ", average amount of time to make a move:" + ( ((double)player2.timeUsed) / player2.moveCount) + " milliseconds");
        for ( int i = 0 ; i < player2.expandedNumberWithDepth.length ; i ++ ){
            System.out.println( "level " + i +  " expanded nodes:" + (((double)player2.expandedNumberWithDepth[i])/player2.moveCount) );
        }
        System.out.println();
        chessBoard.printBoard();
        System.out.println();
        System.out.println();
        return winner;
    }
}