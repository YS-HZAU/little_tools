import java.math.BigInteger;

public class test4 {
    public static BigInteger CombinationPermutations(int sum,int n) {
        BigInteger up = new BigInteger("1");
        BigInteger down = new BigInteger("1");
        for(int i=0; i<n; i++) {
            down = down.multiply(BigInteger.valueOf(i+1));
            up = up.multiply(BigInteger.valueOf(sum-i));
        }
        return up.divide(down);
    }
    public static BigInteger permutations(int sum,int n) {
        BigInteger up = new BigInteger("1");
        for(int i=0; i<n; i++) {
            up = up.multiply(BigInteger.valueOf(sum-i));
        }
        return up;
    }
    public static void main(String[] args) {
        System.out.println(combination(1000,15));
        System.out.println(permutations(1000,15));
    }
}
