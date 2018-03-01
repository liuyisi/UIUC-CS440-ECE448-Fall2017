/**
 * Created by liuyisi on 2017/10/7.
 */
public class ChessBoard {
    public int[][] board ;

    public ChessBoard(){
        board = new int[8][8];
        for( int i = 0 ; i < 2 ; i ++ ){
            for (int j = 0 ; j < 8 ; j ++ ){
                board[i][j] = 1 ;
            }
        }

        for( int i = 6 ; i < 8 ; i ++ ){
            for (int j = 0 ; j < 8 ; j ++ ){
                board[i][j] = 2 ;
            }
        }
    }

    /**
     * 判胜负，返回0是还没有胜负
     * @return
     */
    public int getWinner(){
        int count1 = 0,count2 = 0 ;
        for( int i = 0 ; i < 8 ; i ++ ){
            for( int j = 0 ; j < 8 ; j ++ ){
                if(board[i][j] == 1 ) count1 ++;
                if(board[i][j] == 2 ) count2 ++;
                if( i == 0 && board[i][j] == 2 ) return 2;
                if( i == 7 && board[i][j] == 1 ) return 1;
            }
        }
        if( count1 == 0 ) return 2;
        if( count2 == 0 ) return 1;
        return 0;
    }

    public void printBoard(){
        for( int i = 0 ; i < 8 ; i ++ ){
            for (int j = 0 ; j < 8 ; j ++ ){
                System.out.print( board[i][j]);
            }
            System.out.println();
        }
    }

}