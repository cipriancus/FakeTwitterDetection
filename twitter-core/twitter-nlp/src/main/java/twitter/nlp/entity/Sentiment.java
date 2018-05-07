package twitter.nlp.entity;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Sentiment {
    @JsonProperty("results")
    public Results results;

    public class Results {
        @JsonProperty("text")
        public String text;

        @JsonProperty("polarity")
        public int polarity;

        @JsonProperty("query")
        public String query;
    }
}
