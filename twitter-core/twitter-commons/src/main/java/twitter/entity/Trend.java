package twitter.entity;

import javax.persistence.*;
import java.io.Serializable;


@Entity(name = "TRENDS")
public class Trend extends SocialNetworkPostEntity implements Serializable {


    @Column(name = "query")
    private String query;


    public Trend() {
    }

    public String getQuery() {
        return query;
    }

    public void setQuery(String query) {
        this.query = query;
    }
}
