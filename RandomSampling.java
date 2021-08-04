import htsjdk.samtools.util.IntervalTree;
import htsjdk.samtools.util.IntervalTree.Node;

import java.util.Random;

public class RandomSampling {
    public static void main(String[] args) {
        IntervalTree<String> test = new IntervalTree<>();
        test.put(0,99,"anchor1");
        test.put(100,199,"anchor2");
        test.put(200,299,"anchor3");
        test.put(300,399,"anchor4");
        test.put(400,499,"anchor5");
        test.put(500,599,"anchor6");
        test.printTree();
        Random randomgenerator = new Random(100);
        for(int i=0; i<10; i++) {
            int aa = randomgenerator.nextInt(600);
            Node<String> tmp = test.minOverlapper(aa, aa);
            System.out.println(tmp.getValue());
        }
    }
}
