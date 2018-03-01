import java.util.ArrayList;

/**
 * Created by liuyisi on 2017/10/18.
 */

class Player {
    private ChessBoard board;
    private int color;
    private int depth;
    private String heuristic;
    private boolean withAlphaBeta;
    private int[][] temp;

    public int expandedNumber;
    public int[] expandedNumberWithDepth;
    public int moveCount;
    public long timeUsed;


    int winValue = 500000;
    int almostWin = 10000;


    private int[][][] direction = {  { {1,0} , {1,1} , {1,-1} } , { {-1,0} , {-1,1} , {-1,-1} } };

    /**
     * color 1 or 2
     * @param board
     * @param color
     */
    Player(ChessBoard board, int color, int depth, String heuristic, boolean withAlphaBeta){
        this.board = board;
        this.color = color;
        this.depth = depth;
        this.heuristic = heuristic;
        this.withAlphaBeta = withAlphaBeta;
        temp = new int[8][8];
        expandedNumber = 0;
        expandedNumberWithDepth = new int[depth+1];
        moveCount = 0;
        timeUsed = 0;
    }

    public double defensive1(int[][] board ,int colorNow){
        int[] count = new int[3];
        for( int i = 0 ; i < 8 ; i ++ ) {
            for (int j = 0; j < 8; j++) {
                count[board[i][j]] ++;
            }
        }
        return 2 * count[colorNow] + Math.random();
    }

    public double offensive1(int[][] board ,int colorNow){
        int[] count = new int[3];
        for( int i = 0 ; i < 8 ; i ++ ) {
            for (int j = 0; j < 8; j++) {
                count[board[i][j]] ++;
            }
        }
        double value ;
        if (colorNow == 1 ) {
            value = 2 * (30 - count[2]) + Math.random();
        }else {
            value = 2 * (30 - count[1]) + Math.random();
        }
        return value;
    }

    public double valueOfPiece(int[][] board, int i , int j ){
        double value = 0 ;
        if (board[i][j] == 1 ){
            value = Math.pow(2,i);
            if ( i == 7 ){
                value += winValue;
            } else if ( i == 6 ){
                if ((j > 0 && board[7][j-1] != 2 )&&(j < 7 && board[7][j+1] != 2 )) value += almostWin;
            }

            if ( i != 7 && ( (j > 0 && board[i+1][j-1] == 2 ) || (j < 7 && board[i+1][j+1] == 2 ))) {
                int countSelf = 0;
                if ( i - 1 >= 0 && j+1 <= 7 && board[i-1][j+1] == 1 ) countSelf ++;
                if ( i - 1 >= 0 && j-1 >= 0 && board[i-1][j-1] == 1 ) countSelf ++;

                if ( i + 1 <= 7 && j+1 <= 7 && board[i+1][j+1] == 2 ) countSelf --;
                if ( i + 1 <= 7 && j-1 >= 0 && board[i+1][j-1] == 2 ) countSelf --;

                if (countSelf < 0 ) value = 0;
            }
            return value;
        }
        if(board[i][j] == 2 ){
            value = Math.pow(2,7-i);
            if ( i == 0 ){
                value += winValue;
            } else if ( i == 1 ){
                if ((j > 0 && board[0][j-1] != 1 )&&(j < 7 && board[0][j+1] != 1 )) value += almostWin;
            }

            if ( i != 0 && ( (j > 0 && board[i-1][j-1] == 1 ) || (j < 7 && board[i-1][j+1] == 1 ))) {
                int countSelf = 0;
                if ( i - 1 >= 0 && j+1 <= 7 && board[i-1][j+1] == 1 ) countSelf --;
                if ( i - 1 >= 0 && j-1 >= 0 && board[i-1][j-1] == 1 ) countSelf --;

                if ( i + 1 <= 7 && j+1 <= 7 && board[i+1][j+1] == 2 ) countSelf ++;
                if ( i + 1 <= 7 && j-1 >= 0 && board[i+1][j-1] == 2 ) countSelf ++;

                if (countSelf < 0 ) value = 0;
            }
            return value;
        }
        return 0;
    }

    public double valueOfBoard(int[][] board,int colorNow){
        double value = 0 ;
        for (int i = 0 ; i < 8 ; i ++ ){
            for( int j = 0 ; j < 8 ; j ++ ){
                if (board[i][j] == colorNow) value += valueOfPiece(board,i,j);
            }
        }
        return value;
    }

    public double defensive2(int[][] board,int colorNow){
        double value1 = valueOfBoard(board,1);
        double value2 = valueOfBoard(board,2) ;
        if (colorNow == 1 ){
            return value1 - 2 * value2 + Math.random();
        }else {
            return value2 - 2 * value1 + Math.random();
        }

    }

    public double offensive2(int[][] board, int colorNow ){
        double value1 = valueOfBoard(board,1);
        double value2 = valueOfBoard(board,2) ;
        if (colorNow == 1 ){
            return 2*value1 - value2 + Math.random();
        }else {
            return 2*value2 - value1 + Math.random();
        }
    }

    /**
     * 评价当前局势
     * @return
     */
    private double evaluate(int[][] board,int colorNow){
        if (this.heuristic.equals("defensive1")) {
            return defensive1(board,colorNow);
        }else if (this.heuristic.equals("offensive1")) {
            return offensive1(board,colorNow);
        }else if (this.heuristic.equals("defensive2")) {
            return defensive2(board,colorNow);
        }else if (this.heuristic.equals("offensive2")){
            return offensive2(board,colorNow);
        }
        else return 0;
    }

    //alpha beta 剪枝的
    private double alphaBetaMax(double alpha, double beta , int depth ){
        expandedNumber ++;

        expandedNumberWithDepth[depth] ++;

        int playerNow = color ;
        if( depth == 0 ) return evaluate(temp,color);
        double max = alpha ;
        int indexi = 0, indexj=0 , move=0;

        boolean firstMove = false;

        for( int i = 0 ; i < 8 ; i ++ ){
            for( int j = 0 ; j < 8 ; j ++ ){
                if( temp[i][j] == playerNow){
                    for ( int d = 0 ; d < 3 ; d ++ ){
                        int di = this.direction[playerNow-1][d][0];
                        int dj = this.direction[playerNow-1][d][1];
                        if( i + di < 8 && i + di >= 0 && j + dj < 8 && j + dj >= 0 && temp[i+di][j+dj] != playerNow ){
                            if (d == 0 && temp[i+di][j+dj] != 0 ) continue; //直走要判断前方有没有落子

                            int origin = temp[i+di][j+dj];
                            temp[i][j] = 0;
                            temp[i+di][j+dj] = playerNow;
                            double v = alphaBetaMin(max,beta,depth-1);

                            if(!firstMove){
                                firstMove = true;
                                indexi = i;
                                indexj = j;
                                move = d;
                            }

                            if( v > max ){
                                max = v;
                                indexi = i;
                                indexj = j;
                                move = d;
                            }
                            temp[i][j] = playerNow;
                            temp[i+di][j+dj] = origin;
                            if( max > beta ){
                                return beta;
                            }
                        }
                    }
                }
            }
        }
        if(depth == this.depth){
            int di = this.direction[playerNow-1][move][0];
            int dj = this.direction[playerNow-1][move][1];

            temp[indexi][indexj] = 0;
            temp[indexi+di][indexj+dj] = playerNow;
        }

        return max;
    }

    private double alphaBetaMin(double alpha, double beta , int depth){
        expandedNumber ++;
        expandedNumberWithDepth[depth] ++;

        int playerNow ;
        if (color == 1 ) playerNow = 2;
        else playerNow = 1;
        if( depth == 0 ) return  evaluate(temp,color);
        double min = beta ;



        boolean firstMove = false;
        int indexi = 0, indexj=0 , move=0;

        for( int i = 0 ; i < 8 ; i ++ ){
            for( int j = 0 ; j < 8 ; j ++ ){
                if( temp[i][j] == playerNow){
                    for ( int d = 0 ; d < 3 ; d ++ ){
                        int di = this.direction[playerNow-1][d][0];
                        int dj = this.direction[playerNow-1][d][1];
                        if( i + di < 8 && i + di >= 0 && j + dj < 8 && j + dj >= 0 && temp[i+di][j+dj] != playerNow ){
                            if (d == 0 && temp[i+di][j+dj] != 0 ) continue; //直走要判断前方有没有落子
                            int origin = temp[i+di][j+dj];
                            temp[i][j] = 0;
                            temp[i+di][j+dj] = playerNow;
                            double v = alphaBetaMax(alpha,min,depth-1);
                            if(!firstMove){
                                firstMove = true;
                                indexi = i;
                                indexj = j;
                                move = d;
                            }
                            if( v < min ){
                                min = v;
                                indexi = i;
                                indexj = j;
                                move = d;
                            }
                            temp[i][j] = playerNow;
                            temp[i+di][j+dj] = origin;
                            if( min < alpha ){
                                return alpha;
                            }
                        }
                    }
                }
            }
        }
        if(depth == this.depth){
            int di = this.direction[playerNow-1][move][0];
            int dj = this.direction[playerNow-1][move][1];

            temp[indexi][indexj] = 0;
            temp[indexi+di][indexj+dj] = playerNow;
        }
        return min;
    }

    //普通的
    private double findMax(int depth){
        expandedNumber ++;

        expandedNumberWithDepth[depth] ++;

        int playerNow = color ;
        if( depth == 0 ) return evaluate(temp,color);
        double max = Integer.MIN_VALUE + 1;
        int indexi = 0, indexj= 0 , move=0;

        boolean firstMove = false;

        for( int i = 0 ; i < 8 ; i ++ ){
            for( int j = 0 ; j < 8 ; j ++ ){
                if( temp[i][j] == playerNow){
                    for ( int d = 0 ; d < 3 ; d ++ ){
                        int di = this.direction[playerNow-1][d][0];
                        int dj = this.direction[playerNow-1][d][1];
                        if( i + di < 8 && i + di >= 0 && j + dj < 8 && j + dj >= 0 && temp[i+di][j+dj] != playerNow ){
                            if (d == 0 && temp[i+di][j+dj] != 0 ) continue; //直走要判断前方有没有落子

                            int origin = temp[i+di][j+dj];
                            temp[i][j] = 0;
                            temp[i+di][j+dj] = playerNow;
                            double v = findMin(depth-1);
                            if(!firstMove){
                                firstMove = true;
                                indexi = i;
                                indexj = j;
                                move = d;
                            }
                            if( v > max ){
                                max = v;
                                indexi = i;
                                indexj = j;
                                move = d;
                            }
                            temp[i][j] = playerNow;
                            temp[i+di][j+dj] = origin;
                        }
                    }
                }
            }
        }

        if(depth == this.depth){
            int di = this.direction[playerNow-1][move][0];
            int dj = this.direction[playerNow-1][move][1];

            temp[indexi][indexj] = 0;
            temp[indexi+di][indexj+dj] = playerNow;
        }

        return max;
    }

    private double findMin(int depth){
        expandedNumber ++;

        expandedNumberWithDepth[depth] ++;

        int playerNow ;
        if (color == 1 ) playerNow = 2;
        else playerNow = 1;

        if( depth == 0 ) return  evaluate(temp,color);
        double min = Integer.MAX_VALUE - 1;
        boolean firstMove = false;
        int indexi = 0, indexj= 0 , move=0;



        for( int i = 0 ; i < 8 ; i ++ ){
            for( int j = 0 ; j < 8 ; j ++ ){
                if( temp[i][j] == playerNow){
                    for ( int d = 0 ; d < 3 ; d ++ ){
                        int di = this.direction[playerNow-1][d][0];
                        int dj = this.direction[playerNow-1][d][1];
                        if( i + di < 8 && i + di >= 0 && j + dj < 8 && j + dj >= 0 && temp[i+di][j+dj] != playerNow ){
                            if (d == 0 && temp[i+di][j+dj] != 0 ) continue; //直走要判断前方有没有落子
                            int origin = temp[i+di][j+dj];
                            temp[i][j] = 0;
                            temp[i+di][j+dj] = playerNow;
                            double v = findMax(depth-1);
                            if(!firstMove){
                                firstMove = true;
                                indexi = i;
                                indexj = j;
                                move = d;
                            }
                            if( v < min ){
                                min = v;
                                indexi = i;
                                indexj = j;
                                move = d;
                            }
                            temp[i][j] = playerNow;
                            temp[i+di][j+dj] = origin;
                        }
                    }
                }
            }
        }

        if(depth == this.depth){
            int di = this.direction[playerNow-1][move][0];
            int dj = this.direction[playerNow-1][move][1];

            temp[indexi][indexj] = 0;
            temp[indexi+di][indexj+dj] = playerNow;
        }
        return min;
    }


    public void move(int[][] board){
        moveCount ++;
        long startTime = System.currentTimeMillis();
        for ( int i = 0 ; i < 8 ; i ++ )
            System.arraycopy(board[i], 0, temp[i], 0, 8);

        if( withAlphaBeta ){
            alphaBetaMax(Integer.MIN_VALUE+1,Integer.MAX_VALUE-1,depth);
        }
        else{
            int flag = 0;
            for (int i = 0 ; i < 8 ; i ++ ){
                if ( board[6][i] == 1 ){
                    flag = 1 ;
                    break;
                }
            }
            findMax(depth);
        }

        for ( int i = 0 ; i < 8 ; i ++ )
            System.arraycopy(temp[i], 0, board[i], 0, 8);
        long endTime = System.currentTimeMillis();
        long useTime = endTime - startTime;
        timeUsed += useTime;
    }
}
