package Data;

/**
 * @version: V1.0.0
 * @author: huang
 * @className: Linker
 * @date: 2022/3/2 0002 16:40
 * @description:
 */
public class Linker {
    private String seq;
    private int maxErr;
    private int cutoff;

    public Linker(String aa){
        seq = aa;
        maxErr = (int) Math.ceil(seq.length() * 0.1);
        cutoff = (int) Math.ceil(seq.length() * 0.7);
    }

    public int getCutoff() {
        return cutoff;
    }

    public int getMaxErr() {
        return maxErr;
    }

    public String getSeq() {
        return seq;
    }

    @Override
    public String toString() {
        return getSeq();
    }
}
