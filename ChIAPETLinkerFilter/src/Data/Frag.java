package Data;

/**
 * @version: V1.0.0
 * @author: huang
 * @className: Frag
 * @date: 2022/3/2 0002 19:16
 * @description:
 */
public class Frag {
    private String seq;
    private int start;
    private int end;
    public Frag(String seq, int start, int end){
        this.seq = seq;
        this.start = start;
        this.end = end;
    }
    public String getSeq() {
        return seq;
    }
    public int getStart() {
        return start;
    }
    public int getEnd() {
        return end;
    }
    public void setSeq(String seq) {
        this.seq = seq;
    }
    public void setStart(int start) {
        this.start = start;
    }
    public void setEnd(int end) {
        this.end = end;
    }
    @Override
    public String toString() {
        return getSeq();
    }
}
