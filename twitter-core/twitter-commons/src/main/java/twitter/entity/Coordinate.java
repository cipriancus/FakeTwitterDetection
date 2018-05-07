package twitter.entity;

import javax.persistence.Embeddable;


@Embeddable
public class Coordinate {
    private Long x;
    private Long y;

    public Long getX() {
        return x;
    }

    public void setX(Long x) {
        this.x = x;
    }

    public Long getY() {
        return y;
    }

    public void setY(Long y) {
        this.y = y;
    }
}
